"""JSON-LD shape and visible-text parity review; not a Google eligibility validator."""
import argparse,html,json,re
from bs4 import BeautifulSoup
from data_io import read_text,write_json
from data_io import number
PROFILES={'Organization':['name','url'],'LocalBusiness':['name','address'],'Service':['name','provider'],'Product':['name'],'FAQPage':['mainEntity'],'Article':['headline','author','datePublished'],'Person':['name']}
def flatten(value):
    if isinstance(value,dict):
        yield value
        for child in value.values(): yield from flatten(child)
    elif isinstance(value,list):
        for child in value: yield from flatten(child)
def norm(value): return ' '.join(html.unescape(str(value)).casefold().split())
def visible_contains(text,value,numeric=False):
    token=norm(value)
    if numeric:
        return bool(re.search(r'(?<![\d.])'+re.escape(token)+r'(?![\d.])',norm(text).replace(',','')))
    return bool(token) and token in norm(text)
def validate(markup,visible_text=None):
    soup=BeautifulSoup(markup,'html.parser')
    blocks=[s.get_text() for s in soup.find_all('script',attrs={'type':re.compile(r'^application/ld\+json$',re.I)})]
    if visible_text is None:
        for node in soup.find_all(['script','style','head','template']): node.decompose()
        for node in soup.select('[hidden], [aria-hidden="true"]'): node.decompose()
        visible_text=soup.get_text(' ',strip=True); method='Fetched HTML text; CSS/JavaScript visibility Not verified'
    else: method='Caller-supplied rendered visible text; preserve browser collection evidence separately'
    nodes=[]; issues=[]
    def add(check,detail,label='Inferred'): issues.append({'check':check,'detail':detail,'label':label})
    for index,block in enumerate(blocks):
        try:
            value=json.loads(block)
            if not isinstance(value,(dict,list)): raise ValueError()
            nodes.extend(flatten(value))
        except (ValueError,TypeError): add('json-ld-parse',f'Block {index}: malformed JSON-LD object/array','Confirmed')
    registry={}
    for n in nodes:
        if isinstance(n.get('@id'),str) and len(n)>len(registry.get(n['@id'],{})):
            registry[n['@id']]=n
    def resolve(value): return registry.get(value.get('@id'),value) if isinstance(value,dict) else value
    for node in nodes:
        kinds=node.get('@type',[]); kinds=[kinds] if isinstance(kinds,str) else kinds
        if not isinstance(kinds,list): add('type-shape','@type must be a string or array','Confirmed'); continue
        for kind in kinds:
            if kind not in PROFILES: continue
            for prop in PROFILES[kind]:
                if not node.get(prop): add('profile-property',f'{kind}: review absent {prop}; local review profile, not a universal required property','Confirmed')
            if kind=='Article' and node.get('datePublished'):
                from datetime import datetime
                try: datetime.fromisoformat(str(node['datePublished']).replace('Z','+00:00'))
                except ValueError: add('date-format','Article.datePublished is not an ISO date/datetime','Confirmed')
            for prop in ('name','headline','telephone'):
                if node.get(prop) and not visible_contains(visible_text,node[prop]): add('visible-parity',f'{kind}.{prop}: value not matched in supplied text; inspect formatting and page context')
            address=resolve(node.get('address',{}))
            if isinstance(address,str): address={'address':address}
            if isinstance(address,dict):
                for prop in ('address','streetAddress','addressLocality','postalCode'):
                    if address.get(prop) and not visible_contains(visible_text,address[prop]): add('visible-parity',f'{kind}.address.{prop}: not matched')
            if kind=='FAQPage':
                entities=node.get('mainEntity',[]); entities=entities if isinstance(entities,list) else [entities]
                if not entities: add('faq-shape','FAQPage needs question entities','Confirmed')
                for entity in entities:
                    entity=resolve(entity)
                    if not isinstance(entity,dict): add('faq-shape','Question must be an object','Confirmed'); continue
                    answer=resolve(entity.get('acceptedAnswer',{}))
                    if not entity.get('name') or not isinstance(answer,dict) or not answer.get('text'): add('faq-shape','Question needs name and acceptedAnswer.text','Confirmed'); continue
                    for value in (entity['name'],answer['text']):
                        plain=BeautifulSoup(str(value),'html.parser').get_text(' ',strip=True)
                        if not visible_contains(visible_text,plain): add('faq-parity','Question/answer not matched; check expandable content in browser')
            for field in ('offers','aggregateRating'):
                values=node.get(field,[]); values=values if isinstance(values,list) else [values]
                for value in values:
                    value=resolve(value)
                    if not isinstance(value,dict): add('property-shape',f'{kind}.{field}: object expected','Confirmed'); continue
                    for prop in ('price','lowPrice','highPrice','ratingValue','ratingCount','reviewCount'):
                        if prop in value:
                            try: number(value[prop])
                            except (ValueError,TypeError): add('numeric-shape',f'{kind}.{field}.{prop}: finite nonnegative number expected','Confirmed')
                            if not visible_contains(visible_text,value[prop],True): add('numeric-parity',f'{kind}.{field}.{prop}: not matched; verify currency, units and visible context')
                    if field=='offers' and any(key in value for key in ('price','lowPrice','highPrice')):
                        import pycountry
                        currency=value.get('priceCurrency')
                        if not isinstance(currency,str) or pycountry.currencies.get(alpha_3=currency.upper()) is None:
                            add('currency-profile',f'{kind}.offers: review absent/invalid ISO currency; verify applicable feature requirements','Confirmed')
            if kind=='Product' and not any(node.get(k) for k in ('offers','review','aggregateRating')): add('product-snippet-profile','Review current Google product-snippet requirements: offers/review/aggregateRating branch absent','Confirmed')
    return {'blocks':len(blocks),'typed_entities':sum('@type' in n for n in nodes),'issues':issues,'visibility_method':method,'eligibility':'Not verified','limitations':'Local profiles and text matching only. References are resolved within this document. No remote contexts fetched, legal truth verified, or rich results promised.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--html',required=True); p.add_argument('--visible-text'); p.add_argument('--output',required=True); a=p.parse_args()
    write_json(a.output,validate(read_text(a.html),read_text(a.visible_text) if a.visible_text else None))
