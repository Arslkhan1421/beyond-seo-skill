"""Bounded local imports; URL identity preserves path and query variants."""
import csv, gzip, io, json, math
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, urljoin
MAX_BYTES=20*1024*1024
def read_text(path):
    path=Path(path)
    with (gzip.open(path,'rb') if path.suffix.lower()=='.gz' else open(path,'rb')) as f: raw=f.read(MAX_BYTES+1)
    if len(raw)>MAX_BYTES: raise ValueError('Input exceeds 20 MiB decompressed limit')
    return raw.decode('utf-8-sig')
def read_json(path): return json.loads(read_text(path))
def csv_rows(path):
    text=read_text(path)
    try: dialect=csv.Sniffer().sniff(text[:8192],delimiters=',;\t')
    except csv.Error: dialect=csv.excel
    reader=csv.DictReader(io.StringIO(text),dialect=dialect)
    if not reader.fieldnames or len(set(reader.fieldnames))!=len(reader.fieldnames): raise ValueError('Missing or duplicate CSV headers')
    rows=list(reader)
    if any(None in r or any(v is None for v in r.values()) for r in rows): raise ValueError('Malformed CSV row')
    return rows
def url_key(value,base=None):
    p=urlsplit(urljoin(base,value) if base else value)
    if p.scheme not in {'http','https'} or not p.hostname or p.username or p.password: raise ValueError('Absolute HTTP(S) URL without credentials required')
    return urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path or '/',p.query,''))
def number(value):
    result=float(value)
    if not math.isfinite(result) or result<0: raise ValueError('Finite nonnegative number required')
    return result
def write_json(path,data):
    from audit_quality import sanitize_artifact
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(sanitize_artifact(data),indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
