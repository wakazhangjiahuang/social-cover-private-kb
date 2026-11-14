#!/usr/bin/env python3
"""Deterministic, namespaced retrieval of repository records (stdlib only)."""
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MODES={'A':'douyin','B':'channels','C':'xhs'}
RECORDS={'component':('cover-components.json','components'),
         'hook':('hooks/candidates.json','items'),
         'title':('titles/candidates.json',None),
         'formula':('formulas/core-formulas.json','formulas')}

def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
def matches(row,query):
    # AND across literal terms. No hidden semantic expansion or fabricated score.
    haystack=json.dumps(row,ensure_ascii=False).casefold()
    return all(term.casefold() in haystack for term in (query or '').split())

def layouts(*,id=None,platform=None,structure=None,family=None,nature=None,query=None,primary_only=False,limit=6):
    rows=read('catalog/layout-index.json')['entries']
    result=[]
    for row in rows:
        if id and row['id']!=id.upper():continue
        if structure and structure not in row['structure_ids']:continue
        if family and row['geometry_family']!=family:continue
        if nature and row['evidence_nature']!=nature:continue
        if primary_only and platform and row['source_platform']!=MODES[platform]:continue
        # Exclude adaptation/policy prose from matching to avoid false positives
        # such as finding a mockup when querying for a real photo.
        fields={k:row[k] for k in ['id','name','geometry_name','structure_names','keywords','headline_example']}
        if not matches(fields,query):continue
        result.append(row)
    result.sort(key=lambda row:(bool(platform and row['source_platform']!=MODES[platform]),row['id']))
    return {'kind':'layout','status':'MATCH' if result else 'NO_MATCH',
            'total':len(result),'records':result[:limit],
            'image_check_scope':'file and hash verified at pinned snapshot; verify selected bytes when loading',
            'fallback':None if result else 'Use the requested structure with task assets or original design; do not relabel AI examples as real photos'}

def records(kind,*,id=None,query=None,limit=6,include_unreviewed=False):
    path,key=RECORDS[kind];rows=read(path)
    if key:rows=rows[key]
    review_scope='decision protocol' if kind=='component' else 'editorial/user candidates; validate factual claims before use'
    if kind in ('title','hook'):
        try:
            sidecar=read('catalog/title-hook-metadata.json')
            metadata={item['id']:item for item in sidecar['items']}
        except (OSError,KeyError,ValueError,TypeError):
            return {'kind':kind,'status':'BLOCKED_METADATA_MISSING','total':0,'source_path':path,'records':[],
                    'scope':'Fail-closed: title/hook metadata sidecar unavailable.'}
        missing=[row['id'] for row in rows if row['id'] not in metadata]
        if missing:
            return {'kind':kind,'status':'BLOCKED_METADATA_INCOMPLETE','total':0,'source_path':path,'records':[],
                    'missing_metadata_ids':missing[:20],'scope':'Fail-closed: candidate metadata incomplete.'}
        if include_unreviewed:
            rows=[dict(row,review_status=metadata[row['id']]['review_status'],
                       auto_recommend=metadata[row['id']]['auto_recommend'],
                       performance_status=metadata[row['id']]['performance_status'],
                       retrieval_scope='UNREVIEWED_TEMPLATE_ONLY' if metadata[row['id']]['review_status']!='APPROVED' else 'APPROVED_CANDIDATE')
                  for row in rows]
            review_scope='Explicitly requested templates; unreviewed items are not platform-validated or performance-validated.'
        else:
            rows=[dict(row,review_status=metadata[row['id']]['review_status'])
                  for row in rows if metadata[row['id']]['review_status']=='APPROVED' and metadata[row['id']]['auto_recommend'] is True]
            review_scope='Approved-only retrieval; pending/unreviewed candidates are excluded by default.'
    found=[row for row in rows if (not id or row['id']==id) and matches(row,query)]
    status='MATCH' if found else ('NO_APPROVED_MATCH' if kind in ('title','hook') and not include_unreviewed else 'NO_MATCH')
    fallback='Generate a new candidate from current task facts; do not promote pending records.' if status=='NO_APPROVED_MATCH' else None
    return {'kind':kind,'status':status,'total':len(found),'source_path':path,'records':found[:limit],
            'scope':review_scope,'fallback':fallback}

def main():
    p=argparse.ArgumentParser(description=__doc__);subs=p.add_subparsers(dest='command',required=True)
    a=subs.add_parser('layout');a.add_argument('--id');a.add_argument('--platform',choices=MODES)
    a.add_argument('--structure',choices=[f'L{i:02}' for i in range(1,18)])
    a.add_argument('--family',choices=list('ABCDEFGH'));a.add_argument('--nature',choices=['AI_SYNTHETIC','REAL_PHOTO','ILLUSTRATION'])
    a.add_argument('--primary-only',action='store_true');a.add_argument('--query');a.add_argument('--limit',type=int,default=6)
    b=subs.add_parser('record');b.add_argument('--kind',choices=RECORDS,required=True)
    b.add_argument('--id');b.add_argument('--query');b.add_argument('--limit',type=int,default=6)
    c=subs.add_parser('style');c.add_argument('--id');c.add_argument('--query');c.add_argument('--include-prompt',action='store_true');c.add_argument('--limit',type=int,default=6)
    d=subs.add_parser('joint');d.add_argument('--style-id',required=True);d.add_argument('--structure',choices=[f'L{i:02}' for i in range(1,18)],required=True);d.add_argument('--platform',choices=MODES,required=True);d.add_argument('--limit',type=int,default=3)
    args=vars(p.parse_args());cmd=args.pop('command')
    if not 1<=args['limit']<=500:p.error('--limit must be 1..500')
    if cmd=='layout':
        if args['primary_only'] and not args['platform']:p.error('--primary-only requires --platform')
        result=layouts(**args)
    elif cmd=='record':result=records(**args)
    elif cmd=='style':result=styles(**args)
    else:result=joint(**args)
    print(json.dumps(result,ensure_ascii=False,indent=2))

def styles(*,id=None,query=None,include_prompt=False,limit=6):
    rows=read('catalog/style-index.json')['entries']
    found=[row for row in rows if (not id or row['id']==id) and matches({k:row[k] for k in ['id','name','tags']},query)]
    selected=[]
    for row in found[:limit]:
        row=dict(row)
        if include_prompt:row['source_preset']=read(row['preset_path'])
        selected.append(row)
    return {'kind':'style','status':'MATCH' if found else 'NO_MATCH','total':len(found),'records':selected,
      'scope':'visual reference; source prompt is not platform policy or current task evidence'}

def joint(*,style_id,structure,platform,limit=3):
    visual=styles(id=style_id,include_prompt=True,limit=1)
    composition=layouts(platform=platform,structure=structure,limit=limit)
    return {'kind':'joint','status':'PLANNING_REFERENCE_PAIR' if visual['total'] and composition['total'] else 'PARTIAL_OR_NO_MATCH',
      'style':visual,'layouts':composition,'platform_mode':platform,'premade_combined_image':False,'rendered_or_platform_tested':False,
      'next':'Apply task facts, available authorized materials and platform adapter; generate independently and inspect'}

if __name__=='__main__':main()
