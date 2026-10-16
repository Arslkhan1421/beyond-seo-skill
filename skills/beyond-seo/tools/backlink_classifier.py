"""Review backlink export patterns; no toxicity, penalty or disavow verdicts."""
import argparse,csv
from collections import Counter
from urllib.parse import urlsplit
from data_io import csv_rows,write_json,url_key
def classify(rows,terms=(),sitewide_threshold=10,source='Unknown',provenance='unknown'):
    aliases={'source_url':['source url','referring page url','source','linking page'],'target_url':['target url','target','target page'],'anchor':['anchor','anchor text','link anchor text'],'placement':['placement','link placement','link position']}
    normalized=[]
    for index,row in enumerate(rows,1):
        clean={k.lower().strip().replace('_',' '):v for k,v in row.items()}
        item={key:next((clean[a] for a in names if clean.get(a)),'') for key,names in aliases.items()}
        if not item['source_url'] or not item['target_url']: raise ValueError(f'Row {index}: map source and target URL columns explicitly')
        item['source_url'],item['target_url']=url_key(item['source_url']),url_key(item['target_url'])
        item.update(row=index,source=source,provenance=provenance); normalized.append(item)
    counts=Counter((urlsplit(r['source_url']).hostname,r['target_url']) for r in normalized)
    for row in normalized:
        flags=[]
        if counts[(urlsplit(row['source_url']).hostname,row['target_url'])]>=sitewide_threshold: flags.append('Repeated domain-to-target pattern; possible sitewide links or duplicate exports')
        if any(w in row['placement'].lower() for w in ('footer','sidebar','sitewide')): flags.append('Template placement reported by export')
        if any(w in (row['source_url']+' '+row['anchor']).lower() for w in ('buy links','link exchange','backlink package')): flags.append('Commercial link wording; inspect context, not proof of a link farm')
        matches=sum(term.lower() in (row['source_url']+' '+row['anchor']).lower() for term in terms)
        row.update(review_flags=flags,relevance_term_matches=matches if terms else None,relevance_label='Directional' if terms else 'Not verified',risk_label='Directional',verdict='Manual review' if flags else 'No configured pattern observed; quality Not verified')
    return normalized
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--input',required=True); p.add_argument('--output',required=True); p.add_argument('--csv-output'); p.add_argument('--terms',nargs='*',default=[]); p.add_argument('--source',choices=['ahrefs','semrush','moz'],required=True); p.add_argument('--provenance',choices=['owner_export','authenticated_api','unknown'],default='unknown'); p.add_argument('--sitewide-threshold',type=int,default=10); a=p.parse_args()
    if a.sitewide_threshold<2: p.error('sitewide threshold must be at least 2')
    rows=classify(csv_rows(a.input),a.terms,a.sitewide_threshold,a.source,a.provenance)
    write_json(a.output,{'rows':rows,'limitations':'Lexical relevance and export patterns only. No paid metrics fabricated, penalties inferred, or disavow actions recommended.'})
    if a.csv_output:
        from audit_quality import sanitize_artifact
        from pathlib import Path
        Path(a.csv_output).parent.mkdir(parents=True,exist_ok=True)
        with open(a.csv_output,'w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ['source_url','target_url']); writer.writeheader(); writer.writerows(sanitize_artifact(rows))
