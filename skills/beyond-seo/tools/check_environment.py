"""Report configured capabilities without network calls or credential disclosure."""
import argparse,importlib.util,json,os
from pathlib import Path
def inspect(native_browse=False,native_search=False,files=()):
    exports=[str(p) for p in files if Path(p).is_file()]
    apify=bool(os.getenv('APIFY_API_TOKEN'))
    first_party=any(os.getenv(k) and Path(os.getenv(k)).is_file() for k in ('GSC_EXPORT_PATH','GA4_EXPORT_PATH'))
    mode='Full Intelligence' if first_party and (apify or (native_browse and native_search)) else 'Apify Intelligence' if apify else 'Native Agent Scraping' if native_browse else 'File Analysis' if exports or first_party else 'Advisory'
    return {'suggested_mode':mode,'native_browse_declared':native_browse,'native_search_declared':native_search,'local_file_count':len(exports),'apify_token_configured':apify,'first_party_export_configured':first_party,'dependencies':{name:importlib.util.find_spec(name) is not None for name in ('requests','bs4','reportlab','pypdf')},'limitations':'Configuration only; authentication, network, source completeness and quality are not tested.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--native-browse',action='store_true'); p.add_argument('--native-search',action='store_true'); p.add_argument('--files',nargs='*',default=[]); a=p.parse_args(); print(json.dumps(inspect(a.native_browse,a.native_search,a.files),indent=2))
