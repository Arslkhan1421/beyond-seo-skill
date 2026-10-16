"""Classify page purpose heuristically from CSV URLs and optional title/H1."""
import argparse,re
from urllib.parse import urlsplit
from data_io import csv_rows,write_json
def classify(url,title='',h1=''):
    p=urlsplit(url); path=p.path.lower()
    signals=[
      ('Legal / policy',r'/(privacy|terms|cookies|accessibility|legal)(/|$)','support'),
      ('Transaction / account',r'/(cart|checkout|account|my-account)(/|$)','transaction'),
      ('Product',r'/(products?|shop)/[^/]+','money'),
      ('Collection / category',r'/(collections?|categories|product-category)(/|$)','money'),
      ('Local landing page',r'/(locations?|areas-we-serve|service-areas?)(/|$)','money'),
      ('Archive / pagination',r'/(tags?|authors?|page)/|[?&](page|paged)=','support'),
      ('Contact',r'/contact(/|$)','conversion'),('About',r'/about(/|$)','trust'),
      ('Editorial',r'/(blog|articles?|guides?|resources)(/|$)','support'),
      ('Service / offer',r'/(services?|courses?)(/|$)','money'),
      ('Case study',r'/(work|case-studies|portfolio)(/|$)','trust')]
    kind,role=('Homepage','mixed') if path in {'','/'} else ('Unclassified','Not verified')
    basis='URL pattern'
    for label,pattern,purpose in signals:
        if re.search(pattern,path+('?' + p.query if p.query else '')): kind,role=label,purpose; break
    if kind=='Unclassified' and re.search(r'\b(development|agency|consulting|services?|solutions?)\b',title+' '+h1,re.I):
        kind,role,basis='Possible service / offer','money','Title/H1 language'
    return {'url':url,'page_type':kind,'page_role':role,'path_depth':len([s for s in path.split('/') if s]),'label':'Inferred','basis':basis,'action':'Confirm page purpose before indexing or consolidation changes.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--input',required=True); p.add_argument('--output',required=True); a=p.parse_args()
    write_json(a.output,[classify(r.get('url') or r.get('URL') or r.get('Address') or '',r.get('title',''),r.get('h1','')) for r in csv_rows(a.input)])
