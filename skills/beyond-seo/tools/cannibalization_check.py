"""Find shared-query/metadata review candidates and sample internal-link coverage."""
import argparse,re
from collections import defaultdict
from data_io import csv_rows,read_json,write_json,url_key,number
def analyze(rows,pages=(),similarity_threshold=0.85):
    if not 0.5 <= similarity_threshold <= 1: raise ValueError('Similarity threshold must be 0.5 to 1')
    if len(pages)>500: raise ValueError('Limit metadata similarity review to 500 sampled pages')
    groups=defaultdict(dict); seen=set()
    for row in rows:
        query=' '.join(row['query'].casefold().split()); url=url_key(row.get('page') or row.get('url'))
        dimensions=tuple(sorted((k,str(v)) for k,v in row.items() if k not in {'clicks','impressions','ctr','position'}))
        if dimensions in seen: raise ValueError('Duplicate query/page dimension row; reconcile exports')
        seen.add(dimensions)
        item=groups[query].setdefault(url,{'impressions':0,'clicks':0})
        clicks,impressions=number(row['clicks']),number(row['impressions'])
        if clicks>impressions: raise ValueError('Clicks exceed impressions')
        item['impressions']+=impressions; item['clicks']+=clicks
    candidates=[]
    for query,urls in groups.items():
        if len(urls)>1:
            total=sum(v['impressions'] for v in urls.values())
            candidates.append({'query':query,'label':'Inferred','pages':[{'url':url,**v,'impression_share':v['impressions']/total if total else None} for url,v in urls.items()],'action':'Review intent, canonical variants and time-series switching. Consider re-angling or hub-and-spoke links. Consolidate + 301 only after equivalent intent, owner evidence, backlink/traffic review and a tested mapping; no automatic redirects.'})
    identical=defaultdict(list)
    signatures=[]
    for page in pages:
        h1=page.get('h1',[]); h1=' '.join(h1) if isinstance(h1,list) else h1
        signature=(' '.join(page.get('title','').casefold().split()),' '.join(h1.casefold().split()))
        if all(signature): identical[signature].append(page['url'])
        if all(signature): signatures.append((page['url'],set(re.findall(r'\w+',' '.join(signature)))))
    from itertools import combinations
    near=[]
    for (first,a),(second,b) in combinations(signatures,2):
        similarity=len(a & b)/len(a | b) if a | b else 0
        if similarity_threshold<=similarity<1:
            near.append({'urls':[first,second],'token_jaccard':round(similarity,4),'label':'Inferred','action':'Review page intent; template wording or regional variants may legitimately overlap.'})
    from site_checks import analyze as links
    return {'query_candidates':candidates,'identical_metadata_groups':[urls for urls in identical.values() if len(urls)>1],'similar_metadata_candidates':near,'similarity_threshold':similarity_threshold,'link_graph':links([{'url':p['url'],'links':p.get('internal_links',[]),'priority':p.get('priority',False)} for p in pages]),'limitations':'Query overlap and metadata similarity do not establish harmful cannibalization. Use normalized, nonoverlapping exports for one property/window/segment; CSV alone cannot verify provenance. No causal or ranking-loss claims.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--input'); p.add_argument('--crawl-json'); p.add_argument('--similarity-threshold',type=float,default=0.85); p.add_argument('--output',required=True); a=p.parse_args()
    if not a.input and not a.crawl_json: p.error('Supply --input query CSV and/or --crawl-json')
    pages=read_json(a.crawl_json) if a.crawl_json else []; pages=pages if isinstance(pages,list) else pages['pages']
    write_json(a.output,analyze(csv_rows(a.input) if a.input else [],pages,a.similarity_threshold))
