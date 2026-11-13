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

def records(kind,*,id=None,query=None,limit=6):
    path,key=RECORDS[kind];rows=read(path)
    if key:rows=rows[key]
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
    args=vars(p.parse_args());cmd=args.pop('command')
    if not 1<=args['limit']<=500:p.error('--limit must be 1..500')
    if cmd=='layout':
        if args['primary_only'] and not args['platform']:p.error('--primary-only requires --platform')
        result=layouts(**args)
    else:result=records(**args)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
