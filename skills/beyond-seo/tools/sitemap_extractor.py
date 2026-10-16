"""Extract bounded XML/gzip sitemap trees locally or via the guarded crawler."""
import argparse
from collections import deque
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET
from data_io import read_text,read_json,write_json,url_key
def extract_file(path,max_sitemaps=25,max_urls=10000):
    root_path=Path(path).resolve(); base=root_path.parent
    queue=deque([root_path]); seen=set(); urls=set(); issues=[]
    while queue and len(seen)<max_sitemaps and len(urls)<max_urls:
        current=queue.popleft()
        if current in seen: continue
        if not current.is_relative_to(base): issues.append('Local child outside input directory'); continue
        seen.add(current)
        try:
            text=read_text(current)
            if '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper(): raise ValueError('DTD/entity declarations unsupported')
            tree=ET.fromstring(text); kind=tree.tag.rsplit('}',1)[-1]
            if kind not in {'sitemapindex','urlset'}: raise ValueError('Not a sitemap')
            locations=[c.text.strip() for e in tree for c in e if c.tag.rsplit('}',1)[-1]=='loc' and c.text]
            for loc in locations:
                if kind=='sitemapindex':
                    # Offline indexes must use relative filenames. Never fetch URLs implicitly.
                    if urlsplit(loc).scheme or urlsplit(loc).netloc: issues.append('Remote child not fetched offline: '+loc)
                    else: queue.append((current.parent/loc).resolve())
                else:
                    urls.add(url_key(loc))
                    if len(urls)>=max_urls: break
        except (OSError,ValueError,ET.ParseError) as e: issues.append(str(e))
    if queue or len(urls)>=max_urls: issues.append('Traversal or URL limit reached')
    return {'urls':sorted(urls),'complete':not issues,'issues':issues,'sitemaps_attempted':len(seen)}
def compare(urls,pages):
    by_url={url_key(p['url']):p for p in pages}
    return {'not_crawled':[u for u in urls if u not in by_url],'non_200':[{'url':u,'status':by_url[u].get('status')} for u in urls if u in by_url and by_url[u].get('status') not in (None,200)],'status_unknown':[u for u in urls if u in by_url and by_url[u].get('status') is None],'limitations':'Not crawled is not orphaned. Sitemap listing does not prove indexation.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--input',required=True); p.add_argument('--output',required=True); p.add_argument('--crawl-json'); p.add_argument('--max-sitemaps',type=int,default=25); p.add_argument('--max-urls',type=int,default=10000); a=p.parse_args()
    if not 1<=a.max_sitemaps<=100 or not 1<=a.max_urls<=50000: p.error('Invalid limits')
    if a.input.startswith(('http://','https://')):
        from audit_runner import collect_sitemap_urls
        meta={}; status,urls=collect_sitemap_urls(a.input,urlsplit(a.input).hostname,max_sitemaps=a.max_sitemaps,metadata=meta,max_urls=a.max_urls)
        result={**meta,'status':status,'urls':urls}
    else: result=extract_file(a.input,a.max_sitemaps,a.max_urls)
    if a.crawl_json:
        rows=read_json(a.crawl_json); result['comparison']=compare(result['urls'],rows if isinstance(rows,list) else rows['pages'])
    write_json(a.output,result)
