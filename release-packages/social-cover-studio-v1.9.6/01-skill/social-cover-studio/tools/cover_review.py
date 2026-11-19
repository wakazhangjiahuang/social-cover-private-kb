#!/usr/bin/env python3
"""Validate editorial records and aggregate ratings. No semantic truth inference."""
import argparse, json
from decimal import Decimal
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
RUBRIC = json.loads((ROOT / 'config/cover-rubric.json').read_text(encoding='utf-8'))
STATUSES = {'PASS', 'FAIL', 'UNKNOWN', 'NOT_RUN', 'BLOCKED'}

def count_visible(text):
    try:
        import regex
    except ImportError as exc:
        raise RuntimeError('Install regex to count visible clusters; do not fall back to code points') from exc
    return len(regex.findall(r'\X', text))

def aggregate(record):
    if not isinstance(record, dict): raise ValueError('record must be an object')
    scope = record.get('review_scope')
    if scope not in {'text_only', 'cover'}: raise ValueError('review_scope must be text_only or cover')
    registry = record.get('evidence_registry', {})
    if not isinstance(registry, dict): raise ValueError('evidence_registry must be an object')
    usable = {k:v for k,v in registry.items() if isinstance(k,str) and isinstance(v,dict) and isinstance(v.get('locator'),str) and v['locator'].strip()}
    def refs_ok(refs): return isinstance(refs,list) and bool(refs) and all(isinstance(x,str) and x in usable for x in refs)
    required_gates = RUBRIC['text_only_hard_gates'] if scope == 'text_only' else (RUBRIC['hard_gates'] + RUBRIC.get('visual_gate_for_full_cover', []))
    all_gate_keys = set(RUBRIC['hard_gates']) | set(RUBRIC['text_only_hard_gates']) | set(RUBRIC.get('visual_gate_for_full_cover', []))
    gates = record.get('hard_gates', {})
    if not isinstance(gates, dict) or set(gates)-all_gate_keys: raise ValueError('invalid gate keys')
    pending, failed = [], []
    for key in required_gates:
        item = gates.get(key)
        if item is None: pending.append(key); continue
        if not isinstance(item,dict) or item.get('status') not in STATUSES: raise ValueError(key+': invalid status')
        if item['status']=='FAIL': failed.append(key)
        elif item['status']!='PASS' or not refs_ok(item.get('evidence_refs')): pending.append(key)
    base = {'rubric_version':RUBRIC['rubric_version'],'review_scope':scope,'failed_gates':failed,'pending_gates':pending,
            'semantic_truth_verified_by_code':False,'not_a_ctr_probability':True,'effectiveness':'NOT_RUN'}
    if failed or pending: return {**base,'status':'FAIL' if failed else 'HOLD','score':None}
    dims = record.get('dimensions', {})
    excluded = set(RUBRIC.get('text_only',{}).get('excluded_dimensions',[])) if scope=='text_only' else set()
    required = {d['id'] for d in RUBRIC['dimensions'] if d['id'] not in excluded}
    if not isinstance(dims,dict) or set(dims)!=required: raise ValueError('dimensions must exactly match scope: '+','.join(sorted(required)))
    total = Decimal(0); low=[]
    critical=set(RUBRIC['critical_dimensions'][scope])
    for dim in RUBRIC['dimensions']:
        key=dim['id']
        if key in excluded: continue
        item=dims[key]
        if not isinstance(item,dict) or type(item.get('score')) is not int or not 0<=item['score']<=4: raise ValueError(key+': integer score 0..4 required')
        if not isinstance(item.get('reason'),str) or not item['reason'].strip() or not refs_ok(item.get('evidence')): raise ValueError(key+': reason and resolvable evidence required')
        total += Decimal(item['score'])*Decimal(dim['weight'])/4
        if item['score'] < RUBRIC['bands']['all_dimension_min'] or (key in critical and item['score'] < RUBRIC['bands']['critical_min']): low.append(key)
    if scope=='text_only':
        band='COPY_CANDIDATE' if total>=RUBRIC['bands']['candidate_min'] and not low else ('REVISE' if total>=RUBRIC['bands']['revise_min'] else 'REWRITE')
        return {**base,'status':'TEXT_ONLY_TRIAL','score':float(total),'max_score':RUBRIC['text_only']['max_score'],
                'band':band,'visual_readability':'NOT_RUN','independent_user_validation':'NOT_RUN','weak_dimensions':low}
    band='HIGH_EDITORIAL_CANDIDATE' if total>=RUBRIC['bands']['candidate_min'] and not low else ('REVISE_CANDIDATE' if total>=RUBRIC['bands']['revise_min'] else 'REWRITE')
    return {**base,'status':'TRIAL_RANKED','score':float(total),'max_score':100,'band':band,'weak_dimensions':low,'independent_user_validation':'NOT_RUN'}

def main():
    p=argparse.ArgumentParser(); p.add_argument('record',nargs='?'); p.add_argument('--count',dest='text')
    args=p.parse_args()
    try:
        if args.text is not None: result={'visible_characters':count_visible(args.text),'method':'UAX29_grapheme_clusters'}
        elif args.record: result=aggregate(json.loads(Path(args.record).read_text(encoding='utf-8')))
        else: p.error('supply record or --count TEXT')
    except (ValueError,TypeError,OSError,RuntimeError) as exc:
        print(json.dumps({'status':'INVALID_RECORD','score':None,'error':str(exc)},ensure_ascii=False)); return 2
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if result.get('status') in {'HOLD','FAIL'} else 0
if __name__=='__main__': raise SystemExit(main())
