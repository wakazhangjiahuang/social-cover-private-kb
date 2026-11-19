#!/usr/bin/env python3
"""Build separate execution index and complete integrity inventory."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
CONTROL={'manifest.json','inventory.json','SHA256SUMS.txt','config/knowledge-locator.json'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def files():
 return sorted(p for p in ROOT.rglob('*') if p.is_file() and not any(part in {'.git','__pycache__','node_modules'} for part in p.relative_to(ROOT).parts) and p.suffix!='.pyc' and p.relative_to(ROOT).as_posix() not in CONTROL)
def active(rel):
 return rel.startswith(('covers/','thumbs/','styles/','catalog/','workflow/','hooks/','titles/','formulas/')) or rel in {'cover-components.json','covers.json','config/cover-spec.schema.json','config/integration-status.json','tools/core.mjs','tools/cover_core.mjs','tools/retrieve.py','tools/candidate_filter.py'}
def role(rel):
 if rel.startswith(('covers/','thumbs/')):return 'synthetic_composition_example'
 if rel.startswith('styles/'):return 'visual_style_reference_not_task_evidence'
 if rel.startswith('catalog/'):return 'retrieval_index'
 if rel.startswith(('hooks/','titles/','formulas/')):return 'candidate_requires_task_evidence'
 if rel.startswith(('sources/','research/')) or rel in {'sources.json','platform-audit.json','research-sources.json'}:return 'reference_only_source_not_current_rule'
 return 'execution_protocol' if active(rel) else 'maintenance_or_offline_view_only'
def main():
 paths=files()
 inventory=[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p),'role':role(p.relative_to(ROOT).as_posix()),'default_retrieval':active(p.relative_to(ROOT).as_posix())} for p in paths]
 (ROOT/'inventory.json').write_text(json.dumps({'schema_version':'1.0.0','purpose':'full_file_integrity_not_execution_knowledge','excluded_control_files':sorted(CONTROL),'files':inventory},ensure_ascii=False,indent=2)+'\n')
 deps={'catalog/layout-index.json':['catalog/layout-family-taxonomy.json','covers.json'],'catalog/style-index.json':['styles/metadata.json','styles/provenance.json'],'tools/retrieve.py':['tools/candidate_filter.py','catalog/style-index.json','catalog/layout-index.json','cover-components.json','titles/candidates.json','hooks/candidates.json','formulas/core-formulas.json']}
 assets=[]
 for x in inventory:
  if not x['default_retrieval']:continue
  rel=x['path'];assets.append({'id':rel.replace('/','--').replace('.','-'),'path':rel,'sha256':x['sha256'],'tags':[x['role'],rel.split('/')[0]],'source':'user_supplied_and_repository_maintenance','license':'source_specific_no_general_reuse_license_inferred','ref':'manifest_commit','status':x['role'],'dependencies':deps.get(rel,[])})
 references=[x for x in inventory if x['role']=='reference_only_source_not_current_rule']
 manifest={'schema_version':'1.4.0','status':'active','repository':'wakazhangjiahuang/social-cover-private-kb','updated_at':'2026-11-14','counts':{'visual_styles':18,'cover_png':64,'cover_jpeg':64,'semantic_structures':17,'geometry_families':8,'structures_with_visual_examples':8,'components':18,'decision_fields':179,'title_candidates':225,'hooks':225,'original_core_formulas':10},'entrypoints':{'asset_groups':'catalog/asset-groups.json','visual_styles':'catalog/style-index.json','cover_catalog':'catalog/layout-index.json','structure_taxonomy':'catalog/layout-family-taxonomy.json','cover_specs':'covers.json','decision_components':'cover-components.json','titles':'titles/candidates.json','hooks':'hooks/candidates.json','formulas':'formulas/core-formulas.json','workflow':'workflow/workflow.md','platform_adapter':'workflow/platforms.md','qa':'workflow/qa.md','retrieval':'tools/retrieve.py','candidate_filter':'tools/candidate_filter.py'},'assets':assets,'reference_only':references,'inventory_path':'inventory.json','inventory_sha256':sha(ROOT/'inventory.json'),'ref_policy':'manifest_commit_inherits_consumer_pinned_manifest_ref','retrieval_policy':'Do not scan full inventory, HTML, maintenance logs, code or source full texts for ordinary creation. Follow entrypoint and selected record dependencies only.','control_files_excluded_from_inventory':sorted(CONTROL),'verification_scope':'file integrity, image decoding, metadata retrieval and structural classification; not platform effect validation'}
 (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 lines=[f"{x['sha256']}  {x['path']}" for x in inventory]+[f"{sha(ROOT/rel)}  {rel}" for rel in ['manifest.json','inventory.json']]
 (ROOT/'SHA256SUMS.txt').write_text('\n'.join(lines)+'\n')
 print(json.dumps({'active_assets':len(assets),'integrity_files':len(inventory),'reference_only_files':len(references),'manifest_sha256':sha(ROOT/'manifest.json'),'inventory_sha256':sha(ROOT/'inventory.json')}))
if __name__=='__main__':main()
