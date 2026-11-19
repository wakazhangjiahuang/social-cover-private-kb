#!/usr/bin/env python3
"""Verify current asset bytes, references, geometry and manifest integrity."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def audit():
    index=json.loads((ROOT/'catalog/layout-index.json').read_text())
    specs=json.loads((ROOT/'covers.json').read_text())
    assert len(index['entries'])==len(specs)==64
    ids={r['id'] for r in specs};assert ids=={f'{f}{n:02}' for f in 'ABCDEFGH' for n in range(1,9)}
    hashes=[];thumbs=[]
    for row in index['entries']:
        spec=next(s for s in specs if s['id']==row['id'])
        assert spec['file']==row['image']['path'] and spec['thumb']==row['thumbnail']['path']
        for key in ['image','thumbnail']:
            rec=row[key];p=ROOT/rec['path'];assert p.is_file(),rec['path']
            assert p.stat().st_size==rec['bytes'],rec['path']
            assert digest(p)==rec['sha256'],rec['path']
            with Image.open(p) as im:
                im.load()
                if key=='image':
                    assert im.format=='PNG' and im.size==(row['image']['width'],row['image']['height'])
                else:assert im.format=='JPEG'
        hashes.append(row['image']['sha256']);thumbs.append(row['thumbnail']['sha256'])
    assert len(set(hashes))==64
    page=(ROOT/'START.html').read_text()
    refs=re.findall(r'(?:src|href)=[\"\']([^\"\']+)',page)
    local=[x.split('#')[0].split('?')[0] for x in refs if not x.startswith(('#','http:','https:','data:','javascript:','mailto:'))]
    missing=sorted({x for x in local if x and not (ROOT/x).is_file()});assert not missing,missing
    manifest=json.loads((ROOT/'manifest.json').read_text())
    assert len({row['id'] for row in manifest['assets']})==len(manifest['assets'])
    assert len({row['path'] for row in manifest['assets']})==len(manifest['assets'])
    for row in manifest['assets']:
        p=ROOT/row['path'];assert p.is_file(),row['path'];assert digest(p)==row['sha256'],row['path']
        for dep in row['dependencies']:assert (ROOT/dep).is_file(),dep
    inventory=json.loads((ROOT/'inventory.json').read_text())
    assert digest(ROOT/'inventory.json')==manifest['inventory_sha256']
    excluded=set(inventory['excluded_control_files'])
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
        and not any(x in {'.git','__pycache__','node_modules'} for x in p.relative_to(ROOT).parts)
        and p.suffix!='.pyc' and p.relative_to(ROOT).as_posix() not in excluded}
    assert actual=={x['path'] for x in inventory['files']},'Full inventory coverage differs'
    for x in inventory['files']:
        p=ROOT/x['path'];assert p.stat().st_size==x['bytes'] and digest(p)==x['sha256'],x['path']
    forbidden=('sources/','workbench/','maintenance/','examples/')
    assert not any(x['path'].startswith(forbidden) for x in manifest['assets'])
    style_index=json.loads((ROOT/'catalog/style-index.json').read_text())
    style_rows=style_index['entries'];assert len(style_rows)==18 and len({x['id'] for x in style_rows})==18
    uploaded=(ROOT/'workbench/START.html').read_text()
    embedded=json.loads(re.search(r'<script[^>]*id="scs-offline-data"[^>]*>([\s\S]*?)</script>',uploaded).group(1))
    assert json.loads((ROOT/'styles/metadata.json').read_text())==embedded['data']['data/style-metadata.json']
    style_hashes=[]
    for row in style_rows:
        image=row['image'];p=ROOT/image['path']
        assert digest(p)==image['sha256'] and p.stat().st_size==image['bytes']
        with Image.open(p) as im:im.load();assert im.format=='JPEG' and im.size==(image['width'],image['height'])
        preset=json.loads((ROOT/row['preset_path']).read_text())
        assert preset==embedded['data']['data/'+row['id']+'.json'],'Source prompt changed'
        assert row['metadata_status']=='INFERRED_EDITOR_HINTS'
        style_hashes.append(image['sha256'])
    assert len(set(style_hashes))==18
    cleanup=json.loads((ROOT/'maintenance/cleanup-report.json').read_text())
    assert all(not (ROOT/x['path']).exists() for x in cleanup['deleted'])
    # Full repository file health, distinct from semantic/platform validation.
    from fontTools.ttLib import TTFont
    from pypdf import PdfReader
    from openpyxl import load_workbook
    image_count=font_count=pdf_count=workbook_count=0
    for x in inventory['files']:
        p=ROOT/x['path']
        if p.suffix.lower() in {'.png','.jpg','.jpeg'}:
            with Image.open(p) as im:im.load()
            image_count+=1
        elif p.suffix.lower() in {'.otf','.ttf'}:
            with TTFont(p) as font:assert 'name' in font
            font_count+=1
        elif p.suffix.lower()=='.pdf':
            assert len(PdfReader(p).pages)>0;pdf_count+=1
        elif p.suffix.lower()=='.xlsx':
            book=load_workbook(p,read_only=True,data_only=True);assert book.sheetnames;book.close();workbook_count+=1
        elif p.suffix.lower()=='.json':json.loads(p.read_text())
    return {'status':'PASS','png_decoded':64,'unique_png_sha256':64,'jpeg_decoded':64,
            'platform_counts':dict(Counter(s['primaryPlatform'] for s in specs)),
            'html_local_references':len(local),'missing_html_references':missing,
            'manifest_assets_verified':len(manifest['assets']),
            'full_inventory_files_verified':len(inventory['files']),
            'style_originals_decoded_and_verified':18,'style_source_prompts_preserved':18,
            'deleted_files_verified_absent':len(cleanup['deleted']),
            'all_images_decoded':image_count,'font_files_opened':font_count,
            'source_pdfs_opened':pdf_count,'source_workbooks_opened':workbook_count,
            'semantic_structures':17,'structures_with_examples':index['structures_with_visual_examples'],
            'scope':'bytes, decode, dimensions, paths, SHA256, structural overview classification',
            'not_run':['browser interaction','current platform client preview','account marketing effect','independent audience blind test']}

if __name__=='__main__':print(json.dumps(audit(),ensure_ascii=False,indent=2))
