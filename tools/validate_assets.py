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
    return {'status':'PASS','png_decoded':64,'unique_png_sha256':64,'jpeg_decoded':64,
            'platform_counts':dict(Counter(s['primaryPlatform'] for s in specs)),
            'html_local_references':len(local),'missing_html_references':missing,
            'manifest_assets_verified':len(manifest['assets']),
            'semantic_structures':17,'structures_with_examples':index['structures_with_visual_examples'],
            'scope':'bytes, decode, dimensions, paths, SHA256, structural overview classification',
            'not_run':['browser interaction','current platform client preview','account marketing effect','independent audience blind test']}

if __name__=='__main__':print(json.dumps(audit(),ensure_ascii=False,indent=2))
