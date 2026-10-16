"""Hreflang code, reciprocity and canonical checks within observed HTML samples."""
import argparse
from urllib.parse import urljoin
import pycountry
from data_io import read_json,url_key,write_json
def valid_code(code):
    if not isinstance(code,str): return False
    if code.lower()=='x-default': return True
    parts=code.split('-')
    if not parts or len(parts[0])!=2 or pycountry.languages.get(alpha_2=parts[0].lower()) is None: return False
    rest=parts[1:]
    if rest and len(rest[0])==4:
        if pycountry.scripts.get(alpha_4=rest.pop(0).title()) is None: return False
    return not rest or (len(rest)==1 and len(rest[0])==2 and pycountry.countries.get(alpha_2=rest[0].upper()) is not None)
def analyze(pages):
    by_url={url_key(p.get('final_url') or p['url']):p for p in pages}; issues=[]
    def add(url,check,detail,label='Confirmed'): issues.append({'url':url,'check':check,'detail':detail,'label':label})
    for url,page in by_url.items():
        tags=page.get('hreflang',[])
        if not tags: continue
        destinations=set(); codes={}
        for tag in tags:
            code=tag.get('language',''); href=tag.get('url','')
            if not valid_code(code): add(url,'hreflang-code',f'Unsupported language/region/script code: {code}')
            try:
                destination=url_key(href)
            except ValueError: add(url,'hreflang-url','Absolute HTTP(S) alternate URL required'); continue
            destinations.add(destination)
            if code.lower() in codes and codes[code.lower()]!=destination: add(url,'hreflang-conflict',f'Multiple destinations for {code}')
            codes[code.lower()]=destination
            target=by_url.get(destination)
            if target is None:
                add(url,'hreflang-return',f'Target not sampled: {destination}; return link Not verified','Not verified'); continue
            if target.get('status') != 200 or not target.get('is_html'):
                add(url,'hreflang-return',f'Target response not successfully observed as HTML: {destination}; return link Not verified','Not verified'); continue
            if destination!=url and not any(urljoin(destination,t.get('url',''))==url for t in target.get('hreflang',[])): add(url,'hreflang-return',f'Observed target lacks return link: {destination}')
            canonical=target.get('canonical')
            if canonical:
                try:
                    if url_key(urljoin(destination,canonical))!=destination: add(url,'hreflang-canonical',f'Alternate canonicalizes elsewhere: {destination}','Inferred')
                except ValueError: add(url,'hreflang-canonical',f'Invalid alternate canonical URL: {destination}','Inferred')
            if target.get('noindex'): add(url,'hreflang-noindex',f'Alternate has noindex: {destination}','Inferred')
        if url not in destinations: add(url,'hreflang-self','Self-referencing alternate absent')
        if 'x-default' not in codes: add(url,'hreflang-default','Consider x-default for unmatched languages; optional, not an error','Inferred')
    return {'pages_sampled':len(pages),'issues':issues,'limitations':'Observed HTML alternate tags only; HTTP Link headers and sitemap annotations need separate review. Missing languages are not automatically errors. x-default is optional.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--input',required=True); p.add_argument('--output',required=True); a=p.parse_args(); data=read_json(a.input); write_json(a.output,analyze(data if isinstance(data,list) else data['pages']))
