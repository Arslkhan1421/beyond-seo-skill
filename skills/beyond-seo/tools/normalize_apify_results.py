"""Normalize saved Apify crawl items; never grant verification from an actor name."""
import argparse,json,sys
from data_io import read_json,write_json
def normalize(item):
    if not isinstance(item,dict): raise ValueError('Every item must be an object')
    return {'url':item.get('url') or item.get('link') or item.get('finalUrl'),'title':item.get('title') or item.get('headline'),'text':item.get('text') or item.get('markdown') or item.get('description'),'source':item.get('source') or item.get('actorId'),'evidence_label':'Directional','limitations':'Normalization only; retain raw actor output and collection/provenance metadata.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--input'); p.add_argument('--output'); a=p.parse_args()
    data=read_json(a.input) if a.input else json.load(sys.stdin); items=data if isinstance(data,list) else data.get('items',[])
    if not isinstance(items,list): raise ValueError('items must be an array')
    rows=[normalize(x) for x in items]
    if a.output: write_json(a.output,rows)
    else:
        from audit_quality import sanitize_artifact
        print(json.dumps(sanitize_artifact(rows),indent=2))
