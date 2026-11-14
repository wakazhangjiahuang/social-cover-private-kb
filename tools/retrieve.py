#!/usr/bin/env python3
"""Deterministic, namespaced retrieval of repository records (stdlib only)."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from candidate_filter import select

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

def records(kind,*,id=None,query=None,limit=6,platform=None,surface=None,industry=None,motive=None,evidence=None,include_unverified=False):
    path,key=RECORDS[kind];rows=read(path)
    if key:rows=rows[key]
    if kind in {"title","hook"}:
        result=select(rows,id=id,query=query,limit=limit,platform=platform,surface=surface,
                      industry=industry,motive=motive,evidence=evidence,include_unverified=include_unverified)
        return dict(result,kind=kind,source_path=path)
    if any([platform,surface,industry,motive,evidence is not None,include_unverified]):
        raise ValueError("applicability filters only support title/hook")
    found=[row for row in rows if (not id or row['id']==id) and matches(row,query)]
    return {'kind':kind,'status':'MATCH' if found else 'NO_MATCH','total':len(found),
            'source_path':path,'records':found[:limit],
            'scope':'decision protocol' if kind=='component' else 'editorial/user candidates; validate factual claims before use'}

def main():
    p=argparse.ArgumentParser(description=__doc__);subs=p.add_subparsers(dest='command',required=True)
    a=subs.add_parser('layout');a.add_argument('--id');a.add_argument('--platform',choices=MODES)
    a.add_argument('--structure',choices=[f'L{i:02}' for i in range(1,18)])
    a.add_argument('--family',choices=list('ABCDEFGH'));a.add_argument('--nature',choices=['AI_SYNTHETIC','REAL_PHOTO','ILLUSTRATION'])
    a.add_argument('--primary-only',action='store_true');a.add_argument('--query');a.add_argument('--limit',type=int,default=6)
    b=subs.add_parser('record');b.add_argument('--kind',choices=RECORDS,required=True)
    b.add_argument('--id');b.add_argument('--query');b.add_argument('--limit',type=int,default=6)
    b.add_argument('--platform',choices=MODES);b.add_argument('--surface',choices=['cover_main_title','cover_subtitle','platform_title'])
    b.add_argument('--industry');b.add_argument('--motive');b.add_argument('--evidence',nargs='*')
    b.add_argument('--include-unverified',action='store_true')
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
