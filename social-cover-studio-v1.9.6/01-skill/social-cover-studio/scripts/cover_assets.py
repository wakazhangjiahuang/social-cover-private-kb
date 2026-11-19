#!/usr/bin/env python3
"""Scoped metadata lookup; actual source presets and images load separately."""
import argparse,hashlib,json,re,sys,urllib.request,os,tempfile
from collections import Counter
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from candidate_filter import select
PLATFORMS={'A':'douyin','B':'channels','C':'xhs'}
def read(rel):return json.loads((ROOT/rel).read_text())
def validate(index,taxonomy):
 rows=index['entries'];expected={f'{f}{n:02}' for f in 'ABCDEFGH' for n in range(1,9)}
 if len(rows)!=64 or {r['id'] for r in rows}!=expected:raise ValueError('Expected 64 unique IDs')
 structures={r['id'] for r in taxonomy['families']}
 if len(structures)!=17:raise ValueError('Expected 17 information structures')
 for row in rows:
  if row['geometry_family']!=row['id'][0] or not set(row['structure_ids'])<=structures:raise ValueError('Invalid structure/geometry')
  if row['source_platform'] not in PLATFORMS.values() or row['evidence_nature']!='AI_SYNTHETIC':raise ValueError('Source scope changed')
  for rec in [row['image'],row['thumbnail']]:
   path=PurePosixPath(rec['path'])
   if path.is_absolute() or '..' in path.parts or not re.fullmatch('[0-9a-f]{64}',rec['sha256']):raise ValueError('Invalid image reference')
 return {'status':'PASS','records':64,'geometry_families':dict(Counter(r['geometry_family'] for r in rows)),
   'information_structures':17,'structures_with_examples':index['structures_with_visual_examples'],
   'scope':'index integrity; does not load source PNG bytes'}
def fixed_url(path):
 loc=read('assets/knowledge-locator.json')
 return 'https://raw.githubusercontent.com/'+loc['repository']+'/'+loc['manifest_ref']+'/'+path
def query(index,platform,structure=None,family=None,limit=6,require_image=False,id=None,primary_only=False,nature=None):
 if not 1<=limit<=64:raise ValueError('limit must be 1..64')
 rows=[r for r in index['entries'] if (not structure or structure in r['structure_ids']) and (not family or r['geometry_family']==family) and (not id or r['id']==id.upper()) and (not primary_only or r['source_platform']==PLATFORMS[platform]) and (not nature or r['evidence_nature']==nature)]
 rows.sort(key=lambda r:(r['source_platform']!=PLATFORMS[platform],r['id']))
 result=[dict(r,png_url=fixed_url(r['image']['path'])) for r in rows[:limit]]
 return {'status':'INDEXED_IMAGE_REFERENCES' if rows else 'NO_MATCH','platform_mode':platform,'matching_records':len(rows),
  'candidates':result,'image_bytes_loaded':False,'image_request':'Load selected bytes and verify SHA256' if require_image else 'metadata only',
  'fallback':'Use task assets and original layout for uncovered structures; never relabel AI images as real proof'}
def style_query(id=None,search=None,limit=6):
 rows=read('assets/style-index.json')['entries']
 def match(r):
  text=json.dumps({k:r[k] for k in ['id','name','tags']},ensure_ascii=False).casefold()
  return (not id or r['id']==id) and all(t.casefold() in text for t in (search or '').split())
 found=[r for r in rows if match(r)]
 selected=[dict(r,image_url=fixed_url(r['image']['path']),preset_url=fixed_url(r['preset_path'])) for r in found[:limit]]
 return {'status':'INDEXED_STYLE_REFERENCES' if found else 'NO_MATCH','matching_records':len(found),'candidates':selected,
  'source_prompt_loaded':False,'image_bytes_loaded':False,'scope':'visual reference only; task facts and platform adapter take precedence'}
def joint(index,style_id,platform,structure,limit=3):
 visual=style_query(style_id,limit=1);composition=query(index,platform,structure,limit=limit)
 return {'status':'PLANNING_REFERENCE_PAIR' if visual['matching_records'] and composition['matching_records'] else 'PARTIAL_OR_NO_MATCH',
  'style':visual,'layouts':composition,'premade_combined_image':False,'image_bytes_loaded':False}
def validate_bundles():
 loc=read('assets/knowledge-locator.json')
 for rel,key in [('assets/cover-64-index.json','catalog_index_sha256'),('assets/style-index.json','style_index_sha256')]:
  if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=loc[key]:raise ValueError('Stale bundled index '+rel)
 styles=read('assets/style-index.json')['entries']
 if len(styles)!=18 or len({r['id'] for r in styles})!=18:raise ValueError('Expected 18 unique styles')
 if any(r['metadata_status']!='INFERRED_EDITOR_HINTS' for r in styles):raise ValueError('Source hint scope changed')
 return 18
def safe_path(path):
 p=PurePosixPath(path)
 if p.is_absolute() or '..' in p.parts or '\\' in path:raise ValueError('Unsafe asset path')
 return p
def download(path,expected,limit=100*1024*1024):
 safe_path(path)
 if not re.fullmatch('[0-9a-f]{64}',expected):raise ValueError('Invalid SHA256')
 url=fixed_url(path)
 with urllib.request.urlopen(url,timeout=35) as response:
  if response.geturl()!=url:raise ValueError('Unexpected asset redirect')
  raw=response.read(limit+1)
 if len(raw)>limit:raise ValueError('Asset exceeds size bound')
 if hashlib.sha256(raw).hexdigest()!=expected:raise ValueError('Remote SHA256 mismatch: '+path)
 return raw
def verified_manifest():
 loc=read('assets/knowledge-locator.json')
 if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',loc['repository']) or not re.fullmatch('[0-9a-f]{40}',loc['manifest_ref']):
  raise ValueError('Repository and full immutable ref required')
 return json.loads(download(loc['manifest_path'],loc['manifest_sha256'],3*1024*1024))
def remote_bytes(path):
 manifest=verified_manifest()
 rows=[r for r in manifest['assets'] if r['path']==path]
 if len(rows)!=1:raise ValueError('Selected path is not in fixed execution manifest')
 row=rows[0];return download(path,row['sha256']),row
def fetch_asset(index,id,kind,asset,destination):
 if kind=='layout':
  rows=[r for r in index['entries'] if r['id']==id.upper()]
  if asset not in {'image','thumbnail'}:raise ValueError('Layout supports image/thumbnail')
 elif kind=='style':
  rows=[r for r in read('assets/style-index.json')['entries'] if r['id']==id]
  if asset not in {'image','preset'}:raise ValueError('Style supports image/preset')
 else:raise ValueError('fetch kind must be layout or style')
 if len(rows)!=1:raise ValueError('Unknown selected asset ID')
 row=rows[0];path=row['preset_path'] if asset=='preset' else row[asset]['path']
 raw,entry=remote_bytes(path)
 if asset=='preset':json.loads(raw)
 else:
  import io
  from PIL import Image
  with Image.open(io.BytesIO(raw)) as im:im.load()
  if hashlib.sha256(raw).hexdigest()!=row[asset]['sha256']:raise ValueError('Bundled image hash differs from manifest')
 target=Path(destination).resolve()/safe_path(path)
 target.parent.mkdir(parents=True,exist_ok=True)
 # Reject an existing symlink anywhere under the requested output root.
 root=Path(destination).resolve()
 current=root
 for part in safe_path(path).parts:
  current=current/part
  if current.is_symlink():raise ValueError('Symlink in output path')
 fd,tmp=tempfile.mkstemp(prefix='.asset-',dir=target.parent)
 try:
  with os.fdopen(fd,'wb') as out:out.write(raw)
  os.replace(tmp,target)
 finally:
  if Path(tmp).exists():Path(tmp).unlink()
 return {'status':'FILE_VERIFIED','kind':kind,'id':id,'file':str(target),
  'source_url':fixed_url(path),'sha256':entry['sha256'],'bytes':len(raw),
  'manifest_verified':True,'image_bytes_loaded':asset!='preset','source_prompt_loaded':asset=='preset',
  'scope':'selected source bytes only; not task truth, visual quality or platform effect'}
def candidate_records(kind,**filters):
 mapping={'title':('titles/candidates.json',None),'hook':('hooks/candidates.json','items'),'formula':('formulas/core-formulas.json','formulas')}
 if kind not in mapping:raise ValueError('record kind must be title/hook/formula')
 path,key=mapping[kind];raw,_=remote_bytes(path);rows=json.loads(raw)
 if key:rows=rows[key]
 if kind=='formula':
  if any(filters.get(k) for k in ['platform','surface','industry','motive','evidence','include_unverified']):raise ValueError('Formula does not declare candidate applicability')
  found=[r for r in rows if (not filters['id'] or r['id']==filters['id']) and all(t.casefold() in json.dumps(r,ensure_ascii=False).casefold() for t in (filters['query'] or '').split())]
  result={'status':'MATCH' if found else 'NO_MATCH','total':len(found),'records':found[:filters['limit']]}
 else:result=select(rows,**filters)
 return dict(result,kind=kind,source_path=path,source_bytes_verified=True)
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('command',choices=['validate','query','style','joint','verify-remote','fetch','record'])
 p.add_argument('--platform',choices=PLATFORMS);p.add_argument('--structure',choices=[f'L{i:02}' for i in range(1,18)])
 p.add_argument('--family',choices=list('ABCDEFGH'));p.add_argument('--id');p.add_argument('--search');p.add_argument('--limit',type=int,default=6)
 p.add_argument('--require-image',action='store_true');p.add_argument('--primary-only',action='store_true')
 p.add_argument('--nature',choices=['AI_SYNTHETIC','REAL_PHOTO','ILLUSTRATION'])
 p.add_argument('--kind',choices=['layout','style','title','hook','formula'])
 p.add_argument('--asset',choices=['image','thumbnail','preset'],default='image');p.add_argument('--destination')
 p.add_argument('--surface',choices=['cover_main_title','cover_subtitle','platform_title'])
 p.add_argument('--industry');p.add_argument('--motive');p.add_argument('--evidence',nargs='*')
 p.add_argument('--include-unverified',action='store_true')
 args=p.parse_args()
 if not 1<=args.limit<=500:p.error('--limit must be 1..500')
 if args.command in ['query','joint'] and args.limit>64:p.error('layout limit must be <=64')
 if args.primary_only and not args.platform:p.error('--primary-only requires --platform')
 if args.command in ['query','joint'] and not args.platform:p.error('--platform is required')
 if args.command=='joint' and (not args.id or not args.structure):p.error('joint requires --id style-id and --structure')
 if args.command=='fetch' and not all([args.id,args.kind,args.destination]):p.error('fetch requires --id --kind --destination')
 if args.command=='record' and args.kind not in {'title','hook','formula'}:p.error('record requires title/hook/formula kind')
 try:
  index=read('assets/cover-64-index.json');summary=validate(index,read('references/layout-family-taxonomy.json'));summary['visual_styles']=validate_bundles()
  if args.command=='validate':result=summary
  elif args.command=='verify-remote':
   manifest=verified_manifest();result={'status':'MANIFEST_VERIFIED','assets':len(manifest['assets']),'ref':read('assets/knowledge-locator.json')['manifest_ref'],'scope':'manifest bytes only'}
  elif args.command=='fetch':result=fetch_asset(index,args.id,args.kind,args.asset,args.destination)
  elif args.command=='record':result=candidate_records(args.kind,id=args.id,query=args.search,limit=args.limit,platform=args.platform,surface=args.surface,industry=args.industry,motive=args.motive,evidence=args.evidence,include_unverified=args.include_unverified)
  elif args.command=='style':result=style_query(args.id,args.search,args.limit)
  elif args.command=='joint':result=joint(index,args.id,args.platform,args.structure,args.limit)
  else:result=query(index,args.platform,args.structure,args.family,args.limit,args.require_image,args.id,args.primary_only,args.nature)
 except Exception as exc:
  print(json.dumps({'status':'BLOCKED','error':str(exc)},ensure_ascii=False));raise SystemExit(1)
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
