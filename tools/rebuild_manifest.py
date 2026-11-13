#!/usr/bin/env python3
"""Rebuild content inventory; excludes locators and inventory self hashes."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
CONTROL={'manifest.json','SHA256SUMS.txt','config/knowledge-locator.json'}
def files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and not any(
        part in {'.git','__pycache__','node_modules'} for part in p.relative_to(ROOT).parts)
        and p.suffix!='.pyc' and p.relative_to(ROOT).as_posix() not in CONTROL)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    old=json.loads((ROOT/'manifest.json').read_text())
    previous={x['path']:x for x in old['assets']}
    index=json.loads((ROOT/'catalog/layout-index.json').read_text())
    dep={'catalog/layout-index.json':['catalog/layout-family-taxonomy.json','covers.json'],
         'START.html':['covers.json']+[e[k]['path'] for e in index['entries'] for k in ['image','thumbnail']],
         'src/render.cjs':['covers.json']+[f'assets/photo{i}.png' for i in range(1,7)]+[f'fonts/{s}.otf' for s in ['sans','sansBold','serif','serifBold','mono']],
         'src/check.cjs':['covers.json','START.html','QA.json'],
         'tools/retrieve.py':['catalog/layout-index.json','catalog/layout-family-taxonomy.json','cover-components.json','hooks/candidates.json','titles/candidates.json','formulas/core-formulas.json']}
    assets=[]
    for p in files():
        rel=p.relative_to(ROOT).as_posix();item=dict(previous.get(rel,{}))
        group=rel.split('/')[0] if '/' in rel else 'registry'
        if rel.startswith(('covers/','thumbs/','assets/')):status='synthetic_visual_example'
        elif rel.startswith('sources/'):status='source_material_or_import_provenance'
        elif rel.startswith(('hooks/','titles/','marketing/','presets/','body/','formulas/')):status='candidate_not_effect_evidence'
        elif rel.startswith('catalog/'):status='retrieval_index_or_classification'
        else:status=item.get('status','protocol_or_reference')
        item.update({'id':item.get('id',rel.replace('/','--').replace('.','-')),
         'path':rel,'tags':sorted(set(item.get('tags',[])+[group,status])),
         'source':item.get('source','user_uploaded_cover64_package' if group in ['covers','thumbs','assets','fonts','src'] else 'repository_maintenance'),
         'license':item.get('license','see_fonts_OFL' if group=='fonts' else 'user_supplied_no_general_reuse_license_granted'),
         'ref':'manifest_commit','sha256':sha(p),'status':status,'dependencies':dep.get(rel,item.get('dependencies',[]))})
        assets.append(item)
    new=dict(old)
    new.update({'schema_version':'1.3.0','updated_at':'2026-11-14','status':'active',
     'counts':dict(old['counts'],cover_png=64,cover_jpeg=64,semantic_structures=17,geometry_families=8,structures_with_visual_examples=8),
     'entrypoints':{'cover_design':'workflow/workflow.md','knowledge_routing':'workflow/knowledge.md',
      'asset_groups':'catalog/asset-groups.json','cover_catalog':'catalog/layout-index.json','cover_specs':'covers.json',
      'structure_taxonomy':'catalog/layout-family-taxonomy.json','decision_components':'cover-components.json',
      'hooks':'hooks/candidates.json','titles':'titles/candidates.json','formulas':'formulas/core-formulas.json',
      'source_rules':'sources.json','platform_audit':'platform-audit.json','integrity':'tools/validate_assets.py'},
     'assets':assets,'control_files_excluded_from_inventory':sorted(CONTROL),
     'integrity_note':'Manifest hashes all indexed content, not itself or control locators. File integrity is separate from platform-client and performance validation.',
     'activation_verification':{'checked_at':'2026-11-14','visibility':'public','public_approved_by_user':True,
      'scope':'full indexed file SHA256 plus 64 PNG decode/dimensions, 64 JPEG decode, HTML local paths and retrieval tests',
      'platform_client_verified':False,'marketing_effect_verified':False}})
    (ROOT/'manifest.json').write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n')
    checks=[f"{sha(ROOT/a['path'])}  {a['path']}" for a in assets]
    checks.append(f"{sha(ROOT/'manifest.json')}  manifest.json")
    (ROOT/'SHA256SUMS.txt').write_text('\n'.join(checks)+'\n')
    print(json.dumps({'assets':len(assets),'manifest_sha256':sha(ROOT/'manifest.json')}))
if __name__=='__main__':main()
