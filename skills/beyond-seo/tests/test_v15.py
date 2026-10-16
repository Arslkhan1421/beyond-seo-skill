import csv,gzip,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from audit_runner import run,parse_page,fetch
from schema_validator import validate
from international_checks import valid_code,analyze as international
from cannibalization_check import analyze as overlap
from backlink_classifier import classify as backlinks
from url_classifier import classify as classify_url
from sitemap_extractor import extract_file,compare
from snapshot_io import crawl_snapshot,serp_snapshot
from funnel_joiner import join
from data_io import url_key
from check_environment import inspect
STAMP='2026-10-15T09:00:00Z'
def page(url='https://example.com/',html='<title>Example</title><h1>Example</h1>',status=200):
    return {'url':url,'status':status,'html':html,'collected_at':STAMP,'source_url':url,'method':'Host saved HTML','headers':{'Content-Type':'text/html'}}
class UpgradeTests(unittest.TestCase):
    def test_offline_pipeline_blocks_all_network_and_builds_pdf(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); snapshot=root/'pages.json'; serp=root/'serp.json'
            snapshot.write_text(json.dumps({'pages':[page()]}))
            serp.write_text(json.dumps({'queries':[{'query':'example','country':'GB','language':'en','device':'mobile','collected_at':STAMP,'source_url':'https://google.com/search?q=example','method':'Native organic sample','organic_results':[{'url':'https://example.com/','title':'Example'}]}]}))
            with patch('socket.socket',side_effect=AssertionError('Offline pipeline opened socket')),patch('audit_runner.run_apify_serp',side_effect=AssertionError('Apify called')):
                result=run({'website_url':'https://example.com/'},root/'out',crawl_snapshot_path=snapshot,serp_snapshot_path=serp)
            audit=json.loads(Path(result['audit']).read_text())
            self.assertEqual(audit['rank_baseline'][0]['country'],'GB')
            self.assertEqual(audit['rank_baseline'][0]['source'],'Host-agent SERP observation')
            self.assertEqual(audit['rank_baseline'][0]['observed_position'],1)
            self.assertEqual(audit['evidence_records'][-1]['provenance'],'live_observation')
            self.assertTrue(audit['coverage']['partial']); self.assertTrue(Path(result['pdf']).is_file())
    def test_snapshot_unknown_status_not_200(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'pages.json'; p.write_text(json.dumps({'pages':[page(status=None)]}))
            pages,_,_=crawl_snapshot(p,{'website_url':'https://example.com/'})
            self.assertIsNone(pages[0]['status']); self.assertNotIn('http-availability',pages[0]['checks_performed'])
    def test_snapshot_requires_time_and_scope(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'pages.json'; row=page(); row['collected_at']='2026-10-15'
            p.write_text(json.dumps({'pages':[row]}))
            with self.assertRaises(ValueError): crawl_snapshot(p,{'website_url':'https://example.com/'})
            row=page(url='https://evil.example/')
            p.write_text(json.dumps({'pages':[row]}))
            with self.assertRaises(ValueError): crawl_snapshot(p,{'website_url':'https://example.com/'})
    def test_duplicate_snapshot_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'pages.json'; p.write_text(json.dumps({'pages':[page(),page()]}))
            with self.assertRaises(ValueError): crawl_snapshot(p,{'website_url':'https://example.com/'})
    def test_schema_graph_faq_reference_and_parity(self):
        data={'@graph':[{'@id':'q','@type':'Question','name':'What is included?','acceptedAnswer':{'@id':'a'}},{'@id':'a','@type':'Answer','text':'Setup and support.'},{'@type':'FAQPage','mainEntity':[{'@id':'q'}]}]}
        result=validate('<script type="application/ld+json">'+json.dumps(data)+'</script>','What is included? Setup and support.')
        self.assertFalse(result['issues']); self.assertEqual(result['eligibility'],'Not verified')
    def test_schema_hidden_faq_is_review_not_hallucination_proof(self):
        data={'@type':'FAQPage','mainEntity':[{'name':'Question?','acceptedAnswer':{'text':'Answer'}}]}
        result=validate('<script type="application/ld+json">'+json.dumps(data)+'</script>','Other copy')
        self.assertTrue(any(i['check']=='faq-parity' and i['label']=='Inferred' for i in result['issues']))
    def test_schema_numeric_boundary_and_malformed(self):
        result=validate('<script type="application/ld+json">{"@type":"Product","name":"Book","offers":{"price":9}}</script><script type="application/ld+json">{bad</script>','Book costs 19')
        self.assertTrue(any(i['check']=='numeric-parity' for i in result['issues']))
        self.assertTrue(any(i['check']=='json-ld-parse' for i in result['issues']))
    def test_schema_nonfinite_price_currency_and_article_date(self):
        data=[{'@type':'Product','name':'Book','offers':{'price':'NaN','priceCurrency':'ZZZ'}},{'@type':'Article','headline':'Guide','author':'Author','datePublished':'someday'}]
        result=validate('<script type="application/ld+json">'+json.dumps(data)+'</script>','Book Guide Author')
        self.assertTrue({'numeric-shape','currency-profile','date-format'}.issubset({i['check'] for i in result['issues']}))
    def test_all_supported_schema_types(self):
        for kind in ('Organization','LocalBusiness','Service','Product','FAQPage','Article','Person'):
            with self.subTest(kind=kind):
                result=validate('<script type="application/ld+json">'+json.dumps({'@type':kind})+'</script>','')
                self.assertTrue(result['issues']); self.assertEqual(result['eligibility'],'Not verified')
    def test_hreflang_iso_scripts_and_bad_regions(self):
        for code in ('en','en-GB','zh-Hant','zh-Hans-US','x-default'): self.assertTrue(valid_code(code),code)
        for code in ('en-UK','es-419','en-EU','US','zz-ZZ','zh-Abcd'): self.assertFalse(valid_code(code),code)
    def test_hreflang_unsampled_not_missing_return(self):
        result=international([{'url':'https://example.com/en','hreflang':[{'language':'en','url':'https://example.com/en'},{'language':'fr','url':'https://example.fr/'}]}])
        returns=[i for i in result['issues'] if i['check']=='hreflang-return']
        self.assertEqual(returns[0]['label'],'Not verified')
    def test_hreflang_return_and_canonical_conflict(self):
        result=international([{'url':'https://example.com/en','status':200,'is_html':True,'hreflang':[{'language':'en','url':'https://example.com/en'},{'language':'fr','url':'https://example.com/fr'}]},{'url':'https://example.com/fr','canonical':'https://example.com/en','status':200,'is_html':True,'hreflang':[]}])
        self.assertTrue(any(i['check']=='hreflang-return' and i['label']=='Confirmed' for i in result['issues']))
        self.assertTrue(any(i['check']=='hreflang-canonical' for i in result['issues']))
    def test_cannibalization_is_review_and_keeps_query_variants(self):
        rows=[{'query':'CRM','page':'https://example.com/a','clicks':'2','impressions':'10'},{'query':'crm','page':'https://example.com/a?region=gb','clicks':'3','impressions':'20'}]
        result=overlap(rows)
        self.assertEqual(len(result['query_candidates']),1)
        self.assertIn('no automatic redirects',result['query_candidates'][0]['action'])
        self.assertEqual(result['query_candidates'][0]['pages'][0]['impression_share'],1/3)
    def test_overlap_duplicates_rejected(self):
        row={'query':'x','page':'https://example.com/','clicks':'1','impressions':'10'}
        with self.assertRaises(ValueError): overlap([row,row])
    def test_crawl_only_similar_metadata_and_graph(self):
        pages=[{'url':'https://example.com/a','title':'Custom CRM software development company for small businesses','h1':['Custom CRM software services'],'internal_links':['https://example.com/b']},{'url':'https://example.com/b','title':'Custom CRM software development company for large businesses','h1':['Custom CRM software services'],'priority':True}]
        result=overlap([],pages,0.7)
        self.assertEqual(len(result['similar_metadata_candidates']),1)
        self.assertEqual(result['link_graph']['incoming_pages']['https://example.com/b'],1)
    def test_url_roles(self):
        for path,kind in [('/products/book','Product'),('/collections/books','Collection / category'),('/cart','Transaction / account'),('/locations/dubai','Local landing page'),('/privacy','Legal / policy'),('/tag/books','Archive / pagination')]:
            self.assertEqual(classify_url('https://example.com'+path)['page_type'],kind)
        self.assertEqual(classify_url('https://example.com/custom-crm','CRM development')['page_role'],'money')
    def test_backlink_aliases_and_patterns(self):
        rows=[{'Referring Page URL':'https://source.example/a','Target URL':'https://example.com/','Anchor':'CRM','Link Placement':'footer'},{'Source URL':'https://source.example/b','Target URL':'https://example.com/','Anchor':'CRM'}]
        result=backlinks(rows,['CRM'],2,'ahrefs','owner_export')
        self.assertTrue(result[0]['review_flags']); self.assertEqual(result[0]['relevance_term_matches'],1)
        self.assertEqual(result[0]['risk_label'],'Directional')
    def test_backlink_missing_columns(self):
        with self.assertRaises(ValueError): backlinks([{'URL':'https://example.com/'}])
    def test_local_gzip_sitemap_and_comparison(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'index.xml').write_text('<sitemapindex><sitemap><loc>child.xml.gz</loc></sitemap></sitemapindex>')
            with gzip.open(root/'child.xml.gz','wb') as f: f.write(b'<urlset><url><loc>https://example.com/?x=1&amp;y=2</loc></url></urlset>')
            result=extract_file(root/'index.xml')
            self.assertTrue(result['complete']); self.assertEqual(result['urls'],['https://example.com/?x=1&y=2'])
            compared=compare(result['urls'],[{'url':result['urls'][0],'status':404}])
            self.assertEqual(compared['non_200'][0]['status'],404)
    def test_local_sitemap_traversal_and_remote_no_fetch(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'index.xml').write_text('<sitemapindex><sitemap><loc>../outside.xml</loc></sitemap><sitemap><loc>https://evil.example/map.xml</loc></sitemap></sitemapindex>')
            result=extract_file(root/'index.xml'); self.assertFalse(result['complete']); self.assertEqual(len(result['issues']),2)
    def test_gzip_http_decoding_and_bomb_limit(self):
        from unittest.mock import Mock
        from urllib.parse import urlparse
        raw=gzip.compress(b'<urlset><url><loc>https://example.com/</loc></url></urlset>')
        connection=Mock(); response=Mock(status=200)
        response.getheaders.return_value=[('Content-Type','application/xml')]
        response.read.side_effect=[raw,b'']
        with patch('audit_runner.resolve_network_target',return_value=(urlparse('https://example.com/map.xml.gz'),'93.184.216.34')),patch('audit_runner.open_pinned_response',return_value=(connection,response)):
            result=fetch('https://example.com/map.xml.gz')
        self.assertIn('<urlset>',result['text'])
        response.read.side_effect=[gzip.compress(b'x'*5000),b'']
        with patch('audit_runner.resolve_network_target',return_value=(urlparse('https://example.com/map.xml.gz'),'93.184.216.34')),patch('audit_runner.open_pinned_response',return_value=(connection,response)):
            result=fetch('https://example.com/map.xml.gz',max_bytes=1000)
        self.assertIsNone(result['status']); self.assertIn('Decompressed',result['error'])
    def test_url_identity_preserves_slash_scheme_and_query(self):
        self.assertNotEqual(url_key('https://EXAMPLE.com/a'),url_key('https://example.com/a/'))
        self.assertEqual(url_key('/a?q=1#x','https://example.com/'),'https://example.com/a?q=1')
    def test_environment_detection_does_not_claim_auth(self):
        with patch.dict('os.environ',{},clear=True):
            self.assertEqual(inspect()['suggested_mode'],'Advisory')
            self.assertEqual(inspect(True,True)['suggested_mode'],'Native Agent Scraping')
    def make_funnel(self,root):
        def write(name,fields,rows):
            with (root/name).open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
        write('gsc.csv',['page','clicks','impressions','ctr','position'],[{'page':'https://example.com/a','clicks':10,'impressions':1000,'ctr':0.01,'position':7}])
        write('ga4.csv',['page','sessions','key_events'],[{'page':'/a','sessions':100,'key_events':8}])
        write('clarity.csv',['page','sessions','quick_back_sessions','rage_click_sessions','dead_click_sessions'],[{'page':'/a','sessions':30,'quick_back_sessions':3,'rage_click_sessions':1,'dead_click_sessions':2}])
        sources={}
        for name in ('gsc','ga4','clarity'):
            meta={'source':name,'property':'https://example.com/' if name=='gsc' else 'owned-'+name,'website_url':'https://example.com/','provenance':'owner_export','retrieved_at':STAMP,'start_date':'2026-10-10','end_date':'2026-10-12','timezone':'UTC','dimensions':['page'],'filters':{},'join_scope':{'country':'US','device':'all'}}
            if name=='ga4': meta.update(key_event_definition='form_submit',filters={'channel':'Organic Search'})
            if name=='gsc': meta['search_type']='web'
            if name=='clarity': meta['organic_source_mapping']='Owner-exported organic-search segment'
            sources[name]={'csv':name+'.csv','metadata':meta}
        return {'website_url':'https://example.com/','sources':sources}
    def test_funnel_compatible_rates_and_candidates(self):
        with tempfile.TemporaryDirectory() as d:
            spec=self.make_funnel(Path(d)); result=join(spec,Path(d))
            self.assertEqual(result['status'],'Compatible supplied aggregates')
            self.assertEqual(result['rows'][0]['key_events_per_session'],0.08)
            self.assertEqual(result['rows'][0]['max_friction_session_rate'],0.1)
            self.assertEqual(len(result['rows'][0]['review_candidates']),2)
    def test_funnel_incompatible_window_returns_no_diagnosis(self):
        with tempfile.TemporaryDirectory() as d:
            spec=self.make_funnel(Path(d)); spec['sources']['clarity']['metadata']['start_date']='2026-10-11'
            result=join(spec,Path(d)); self.assertEqual(result['status'],'Not comparable'); self.assertEqual(result['rows'],[])
    def test_funnel_channel_and_missing_provenance(self):
        with tempfile.TemporaryDirectory() as d:
            spec=self.make_funnel(Path(d)); spec['sources']['ga4']['metadata']['filters']={}; spec['sources']['clarity']['metadata'].pop('organic_source_mapping')
            self.assertEqual(join(spec,Path(d))['status'],'Not comparable')
    def test_funnel_zero_denominator_and_missing_rows(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); spec=self.make_funnel(root)
            (root/'ga4.csv').write_text('page,sessions,key_events\n/a,0,0\n')
            (root/'clarity.csv').write_text('page,sessions,quick_back_sessions,rage_click_sessions,dead_click_sessions\n/other,0,0,0,0\n')
            result=join(spec,root); a=next(r for r in result['rows'] if r['url'].endswith('/a'))
            self.assertIsNone(a['key_events_per_session']); self.assertIsNone(a['clarity']); self.assertIn('clarity',a['missing_sources'])
    def test_funnel_impossible_clarity_sessions_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); spec=self.make_funnel(root)
            (root/'clarity.csv').write_text('page,sessions,quick_back_sessions,rage_click_sessions,dead_click_sessions\n/a,1,2,0,0\n')
            with self.assertRaises(ValueError): join(spec,root)
if __name__=='__main__': unittest.main()
