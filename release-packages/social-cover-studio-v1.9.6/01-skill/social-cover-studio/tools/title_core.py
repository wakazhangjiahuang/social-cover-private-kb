#!/usr/bin/env python3
"""Aggregate reviewed records; never infer missing gates or verify CTR."""
import json,sys
from pathlib import Path
RUBRIC=json.loads((Path(__file__).resolve().parents[1]/"config/title-rubric.json").read_text())
DIMENSIONS={d["id"] for d in RUBRIC["dimensions"]}
GATES=set(RUBRIC["hard_gates"])
STATUSES={"PASS","FAIL","UNKNOWN","NOT_RUN","BLOCKED"}
def hold(keys,reason):
 return {"status":"HOLD","score":None,"failed_gates":[],"unknown_gates":sorted(keys),"reason":reason}
def references(value,registry):
 if isinstance(value,str):value=[value]
 return isinstance(value,list) and bool(value) and all(isinstance(x,str) and x in registry for x in value)
def aggregate(record):
 if not isinstance(record,dict):raise ValueError("record must be an object")
 gates=record.get("hard_gates",{})
 if not isinstance(gates,dict):raise ValueError("hard_gates must be an object")
 if set(gates)-GATES:raise ValueError("unknown hard gate keys: "+",".join(sorted(set(gates)-GATES)))
 normalized={}
 for key,value in gates.items():
  if isinstance(value,str):value={"status":value,"evidence_refs":record.get("gate_evidence",{}).get(key,[])}
  if not isinstance(value,dict) or value.get("status") not in STATUSES:raise ValueError(key+": invalid gate status")
  normalized[key]=value
 failed=[k for k,v in normalized.items() if v["status"]=="FAIL"]
 unknown=(GATES-set(gates))|{k for k,v in normalized.items() if v["status"] in {"UNKNOWN","NOT_RUN","BLOCKED"}}
 if failed:return {"status":"FAIL","score":None,"failed_gates":sorted(failed),"unknown_gates":sorted(unknown)}
 if unknown:return hold(unknown,"All four required gates must be explicitly reviewed")
 registry=record.get("evidence_registry",{})
 if not isinstance(registry,dict):raise ValueError("evidence_registry must be an object")
 usable={k:v for k,v in registry.items() if isinstance(k,str) and k.strip() and isinstance(v,dict) and isinstance(v.get("locator"),str) and v["locator"].strip()}
 missing=[k for k,v in normalized.items() if not references(v.get("evidence_refs"),usable)]
 if missing:return hold(missing,"PASS gates require resolvable evidence IDs and nonblank locators")
 dims=record.get("dimensions",{})
 if not isinstance(dims,dict) or set(dims)!=DIMENSIONS:raise ValueError("dimensions must contain D1-D8 exactly")
 total=0
 for key in sorted(DIMENSIONS):
  item=dims[key]
  if not isinstance(item,dict):raise ValueError(key+" must be an object")
  score=item.get("score")
  if type(score) is not int or not 0<=score<=4:raise ValueError(key+".score must be integer 0..4 (not boolean)")
  if not isinstance(item.get("reason"),str) or not item["reason"].strip():raise ValueError(key+" requires a nonblank reason")
  if not references(item.get("evidence"),usable):raise ValueError(key+" requires resolvable evidence IDs")
  total+=score
 return {"status":"TRIAL_RANKED","score":total,"max_score":32,"failed_gates":[],"unknown_gates":[],"not_a_ctr_probability":True,"evidence_semantically_verified_by_code":False}
if __name__=="__main__":
 if len(sys.argv)!=2:raise SystemExit("usage: title_core.py RECORD.json")
 try:result=aggregate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
 except (ValueError,TypeError,OSError) as exc:
  print(json.dumps({"status":"INVALID_RECORD","score":None,"error":str(exc)},ensure_ascii=False));raise SystemExit(2)
 print(json.dumps(result,ensure_ascii=False,indent=2))
 raise SystemExit(0 if result["status"]=="TRIAL_RANKED" else 1)
