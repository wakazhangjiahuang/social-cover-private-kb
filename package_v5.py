from pathlib import Path
from lxml import html
import json,hashlib,zipfile,re,shutil

ROOT=Path(__file__).resolve().parent
P=ROOT/'project'
doc=html.fromstring((ROOT/'START.html').read_text())
assert not doc.xpath('//script[@src]')
assert len(doc.xpath('//*[@id]/@id'))==len(set(doc.xpath('//*[@id]/@id')))
data=json.loads(doc.get_element_by_id('scs-offline-data').text)
assert len(data['assets'])==18
assert json.loads((P/'package.json').read_text())['version']=='5.0.3-rebuilt'
assert 'project_id' not in json.loads((P/'.openai/hosting.json').read_text())
tests=(ROOT/'test-results.txt').read_text()
assert 'pass 25' in tests and 'fail 0' in tests and 'skipped 3' in tests
native=json.loads((ROOT/'native-export-verification.json').read_text());assert native['status']=='PASS'
assert all(x['title_region_ink_pixels']>20000 for x in native['outputs'])
report={'version':'5.0.3-rebuilt','date':'2026-11-07','overall':'PARTIAL_EXTERNAL_VALIDATION_PENDING','reconstruction':'rebuilt from saved V4 source and confirmed V5 requirements, not byte-identical recovery','unit_integration':{'pass':25,'fail':0,'skipped':3,'skip_reason':'historical hosted archive tests do not apply to a separate external source delivery ZIP'},'native_canvas_adapter':native,'offline_HTML':{'external_scripts':0,'embedded_original_content_thumbnails':18,'professional_fonts':'7 actual font files in complete source; offline HTML uses system fonts','original_large_previews':'18 unaltered upstream JPEG files in relative project folder'},'browser_interaction':'NOT_RUN','responsive_real_devices':'NOT_RUN','live_image_generation':'NOT_RUN_NOT_CONFIGURED','pixel_OCR':'NOT_RUN','official_platform_live_crop':'NOT_RUN','independent_design_review':'NOT_RUN','account_metrics':'NOT_PROVIDED','missing_original':'social-cover-studio_小红书封面.html not available; uiData/source_spec mapping of that source not verified','Sites_deployment':'NOT_DEPLOYED_PENDING_USER_REVIEW'}
(ROOT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
run={'task':'V5 rebuilt deliverable','version':'5.0.3-rebuilt','baseline_SHA256':'76bd71933a0e17d64f395b63d3c4f19588f84a8e78d011d82a932a02991fb38c','upstream_commit':'25a7279ff36931fc4eab069999adb1ad988b5d27','changes':['restore 18 original presets and JPEG previews','canvas-first product UI with copy/visual controls','preplanned case with exact source references','preserve six-to-three and separate same-style queue','exact-font and main-title rendering repair','standalone HTML and complete independent source package'],'approval':'preview/package only; no Site deployment','source_secrets':'no actual credentials included'}
(ROOT/'run-record.json').write_text(json.dumps(run,ensure_ascii=False,indent=2))
root_names=['START.html','README.md','verification.json','run-record.json','native-export-verification.json','original-images.json','style-sources.json','test-results.txt','build_offline.py','verify_native_export.mjs','package_v5.py']
files=[ROOT/n for n in root_names]
files += [x for folder in ['project','examples'] for x in (ROOT/folder).rglob('*') if x.is_file() and not any(v in x.relative_to(ROOT).parts for v in ['node_modules','.git','.next','.wrangler','runtime-data','__pycache__']) and (x.name!='.env' or x.name=='.env.example')]
assert all(f.is_file() for f in files)
for p in files:
 if p.suffix in ['.js','.mjs','.ts','.tsx','.json','.html','.md','.py','.yml']:
  text=p.read_text(errors='replace')
  assert not re.search(r'\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}',text),str(p)
  if p.name!='package_v5.py':assert 'siwc_bypass_bearer_token' not in text,str(p)
manifest=[{'path':str(f.relative_to(ROOT)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(set(files))]
(ROOT/'manifest.json').write_text(json.dumps({'version':'5.0.3-rebuilt','files':manifest},ensure_ascii=False,indent=2))
archive=ROOT.parent/'Social_Cover_Studio_V5_Complete.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in sorted(set(files))+[ROOT/'manifest.json']:z.write(f,str(f.relative_to(ROOT)))
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for f in manifest:assert hashlib.sha256(z.read(f['path'])).hexdigest()==f['sha256'],f['path']
 assert z.read('START.html')==(ROOT/'START.html').read_bytes()
release={'file':str(archive),'version':'5.0.3-rebuilt','bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'entries':len(manifest)+1,'CRC':'PASS','per_file_SHA256':'PASS','HTML':'START.html'}
(ROOT/'release.json').write_text(json.dumps(release,indent=2))
print(json.dumps(release,ensure_ascii=False))
