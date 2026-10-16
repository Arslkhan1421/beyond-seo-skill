"""Join compatible URL-level first-party exports into review candidates, never causal diagnoses."""
import argparse
from datetime import date
from pathlib import Path
from data_io import read_json,csv_rows,write_json,url_key,number
from first_party_quality import validate_export
from snapshot_io import timestamp
def join(spec,base_dir=Path('.')):
    required={'gsc','ga4','clarity'}
    if set(spec.get('sources',{}))!=required: raise ValueError('Exactly gsc, ga4 and clarity source descriptors required')
    website=url_key(spec['website_url']); sources={}; errors=[]
    thresholds={'min_impressions':100,'low_ctr':0.02,'min_clicks':20,'min_sessions':20,'friction_rate':0.1,'low_events_per_session':0.01,'high_events_per_session':0.05,**spec.get('thresholds',{})}
    thresholds={k:number(v) for k,v in thresholds.items()}
    reference=None; artifacts=[]
    for name,desc in spec['sources'].items():
        path=base_dir/desc['csv']; meta=desc['metadata']
        import hashlib
        artifacts.append({'source':name,'file':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'metadata':meta})
        if meta.get('source')!=name: errors.append(name+': metadata source mismatch')
        if meta.get('provenance') not in {'owner_export','authenticated_api'}: errors.append(name+': source provenance required')
        if not isinstance(meta.get('join_scope'),dict) or not meta['join_scope']: errors.append(name+': explicit shared join_scope required')
        comparable={k:meta.get(k) for k in ('start_date','end_date','timezone','join_scope')}
        if reference is None: reference=comparable
        elif comparable!=reference: errors.append(name+': incompatible windows/timezone/segment')
        try:
            if date.fromisoformat(meta['start_date'])>date.fromisoformat(meta['end_date']): raise ValueError()
            timestamp(meta.get('retrieved_at'))
            from zoneinfo import ZoneInfo
            ZoneInfo(meta['timezone'])
            if meta['retrieved_at'][:10]<meta['end_date']: raise ValueError()
        except (KeyError,ValueError): errors.append(name+': invalid measurement dates/provenance time')
        if name in {'gsc','ga4'}:
            quality=validate_export(path,meta,website)
            errors.extend(name+': '+e for e in quality['errors'])
            if 'page' not in meta.get('dimensions',[]): errors.append(name+': normalized page dimension required')
            if name=='ga4' and meta.get('filters',{}).get('channel')!='Organic Search': errors.append('ga4: explicit Organic Search channel filter required')
            if name=='ga4' and meta.get('dimensions')!=['page']: errors.append('ga4: nonoverlapping page-level session aggregates required')
            if name=='gsc' and meta.get('search_type')!='web': errors.append('gsc: explicit web search_type required')
        else:
            if not meta.get('organic_source_mapping'): errors.append('clarity: organic segment mapping required; all-channel behavior cannot diagnose organic traffic')
            if url_key(meta.get('website_url',''))!=website: errors.append('clarity: website mapping mismatch')
            if meta.get('dimensions')!=['page']: errors.append('clarity: page-level nonoverlapping aggregate rows required')
        rows=csv_rows(path); aggregate={}
        if not rows: errors.append(name+': empty data is not zero performance')
        for index,row in enumerate(rows,1):
            url=url_key(row['page'],website)
            if url.split('/')[2]!=website.split('/')[2]: raise ValueError(name+': row outside website host')
            metrics=['clicks','impressions','position'] if name=='gsc' else ['sessions','key_events'] if name=='ga4' else ['sessions','quick_back_sessions','rage_click_sessions','dead_click_sessions']
            values={k:number(row[k]) for k in metrics}
            if name=='clarity' and any(values[k]>values['sessions'] for k in metrics[1:]): raise ValueError('Clarity affected sessions exceed total sessions')
            if name=='clarity' and url in aggregate: raise ValueError('Duplicate Clarity page key; reconcile overlapping rows')
            target=aggregate.setdefault(url,{k:0.0 for k in metrics})
            if name=='gsc':
                target['position']+=values['position']*values['impressions']
                for k in ('clicks','impressions'): target[k]+=values[k]
            else:
                for k in metrics: target[k]+=values[k]
        if name=='gsc':
            for values in aggregate.values():
                values['position']=values['position']/values['impressions'] if values['impressions'] else None
                values['ctr']=values['clicks']/values['impressions'] if values['impressions'] else None
        sources[name]=aggregate
    if errors: return {'status':'Not comparable','errors':errors,'rows':[]}
    output=[]
    for url in sorted(set().union(*(s.keys() for s in sources.values()))):
        g=sources['gsc'].get(url); a=sources['ga4'].get(url); c=sources['clarity'].get(url)
        notes=[]
        event_rate=a['key_events']/a['sessions'] if a and a['sessions'] else None
        # No adding overlapping friction categories together.
        friction=max(c[k]/c['sessions'] for k in ('quick_back_sessions','rage_click_sessions','dead_click_sessions')) if c and c['sessions'] else None
        if g and g['ctr'] is not None and g['impressions']>=thresholds['min_impressions'] and g['ctr']<thresholds['low_ctr']: notes.append('Review SERP snippet, query mix, position and intent; low CTR does not establish a title problem.')
        if g and a and c and g['clicks']>=thresholds['min_clicks'] and a['sessions']>=thresholds['min_sessions'] and friction is not None and friction>=thresholds['friction_rate'] and event_rate is not None and event_rate<thresholds['low_events_per_session']: notes.append('Review landing-page intent, UX/CTA friction, consent and event tracking; cause Not verified.')
        if g and a and a['sessions']>=thresholds['min_sessions'] and event_rate is not None and event_rate>=thresholds['high_events_per_session'] and g['position'] is not None and 4<=g['position']<=15: notes.append('Review internal links and content refresh for an engaged converting page. ROI and rank gains Not verified.')
        output.append({'url':url,'gsc':g,'ga4':a,'clarity':c,'key_events_per_session':event_rate,'max_friction_session_rate':friction,'review_candidates':notes,'missing_sources':[n for n in sources if url not in sources[n]],'label':'Inferred'})
    return {'status':'Compatible supplied aggregates','source_artifacts':artifacts,'thresholds':thresholds,'rows':output,'limitations':'Not a user-level funnel. GSC clicks, GA4 sessions and Clarity sessions differ in attribution, consent and coverage; GSC query rows may be incomplete. Do not divide metrics across sources. key_events/session is not session conversion rate or qualified leads. Thresholds are configurable heuristics, not industry benchmarks or ROI predictions.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--input',required=True); p.add_argument('--output',required=True); a=p.parse_args()
    write_json(a.output,join(read_json(a.input),Path(a.input).resolve().parent))
