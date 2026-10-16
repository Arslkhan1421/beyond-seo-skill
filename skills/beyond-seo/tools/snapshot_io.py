"""Validate host-agent observations without opening sockets."""
from datetime import datetime
import hashlib
from urllib.parse import urlsplit
from data_io import read_json,url_key,write_json
def timestamp(value):
    try:
        parsed=datetime.fromisoformat(value.replace('Z','+00:00'))
        if parsed.tzinfo is None: raise ValueError()
    except (AttributeError,TypeError,ValueError) as e: raise ValueError('Collection timestamp with timezone required') from e
    return value
def crawl_snapshot(path,config):
    from audit_runner import parse_page
    data=read_json(path)
    if not isinstance(data,dict) or not isinstance(data.get('pages'),list) or not data['pages']: raise ValueError('Crawl snapshot needs nonempty pages array')
    host=urlsplit(config['website_url']).hostname.lower().removeprefix('www.')
    if len(data['pages'])>config.get('max_crawl_pages',100): raise ValueError('Snapshot exceeds max_crawl_pages')
    pages=[]; seen=set()
    for row in data['pages']:
        url=url_key(row['url']); final=url_key(row.get('final_url') or url)
        if any(urlsplit(u).hostname.lower().removeprefix('www.')!=host for u in (url,final)): raise ValueError('Snapshot page outside target host')
        if url in seen: raise ValueError('Duplicate snapshot URL')
        seen.add(url)
        status=row.get('status')
        if status is not None and (isinstance(status,bool) or not isinstance(status,int) or not 100<=status<=599): raise ValueError('Invalid HTTP status')
        timestamp(row.get('collected_at'))
        if not row.get('method') or not row.get('source_url'): raise ValueError('Snapshot requires method and source_url')
        text=row.get('html')
        if not isinstance(text,str): raise ValueError('Snapshot needs html (saved fetched or serialized DOM); do not pass prose as HTML')
        # Browser tool success is not proof of HTTP 200. Missing status stays unknown.
        result={'url':url,'final_url':final,'status':status,'text':text,'headers':row.get('headers',{}),'collected_at':row['collected_at'],'response_sha256':hashlib.sha256(text.encode()).hexdigest()}
        page=parse_page(result,host)
        page.update(collection_method=row['method'],snapshot_source_url=row['source_url'],rendered=row.get('rendered') is True)
        pages.append(page)
    supplied=data.get('coverage',{})
    coverage={**supplied,'attempted_urls':len(pages),'successful_urls':sum(p['status']==200 for p in pages),'rendered_urls':sum(p['rendered'] for p in pages),'discovered_urls':max(len(pages),supplied.get('discovered_urls',len(pages))),'partial':True,'stopping_reason':'Host-agent snapshot; discovery completeness Not verified','limitations':'Saved host observations only; Google indexation and complete site coverage Not verified.'}
    sitemap=data.get('sitemap',{'complete':False,'urls':[]})
    if sitemap.get('complete') and not (sitemap.get('source_url') and sitemap.get('collected_at') and sitemap.get('status') == 200): raise ValueError('Complete sitemap snapshot requires successful status, source_url and collected_at')
    if sitemap.get('collected_at'): timestamp(sitemap['collected_at'])
    sitemap={**sitemap,'urls':[url_key(u) for u in sitemap.get('urls',[])]}
    robots={'coverage':coverage,'status':None,'content':'Not verified in snapshot'}
    return pages,robots,sitemap
def serp_snapshot(path,host,config,output):
    from audit_runner import normalize_serps
    data=read_json(path)
    rows=data.get('queries') if isinstance(data,dict) else None
    if not isinstance(rows,list): raise ValueError('SERP snapshot requires queries array')
    baseline=[]; candidates=[]
    if len(rows)>config.get('max_serp_queries',20): raise ValueError('SERP snapshot exceeds query budget')
    for index,row in enumerate(rows):
        timestamp(row.get('collected_at'))
        for key in ('query','country','language','device','source_url','method'):
            if not isinstance(row.get(key),str) or not row[key]: raise ValueError(f'SERP snapshot missing {key}')
        results=row.get('organic_results')
        if not isinstance(results,list) or any(not isinstance(r,dict) or not r.get('url') for r in results): raise ValueError('Explicit ordered organic_results array required')
        for r in results: url_key(r['url'])
        context={**config,'target_country':row['country'],'country_code':row['country'],'language_code':row['language'],'device':row['device']}
        b,c=normalize_serps([{'query':row['query'],'organicResults':results}],host,context,row['collected_at'])
        for entry in b+c:
            entry.update(source='Host-agent SERP observation',source_url=row['source_url'],collection_method=row['method'],artifact_index=index,provenance='live_observation',collected_at=row['collected_at'])
        baseline+=b; candidates+=c
    write_json(output/'host-serp-snapshot.json',data)
    return baseline,candidates
