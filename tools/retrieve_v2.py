#!/usr/bin/env python3
"""Local deterministic retrieval for V2.0 platform/workflow knowledge."""
import argparse,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PLATFORM_FILES={"A":"platforms/A-douyin.md","B":"platforms/B-wechat-channels.md","C":"platforms/C-xiaohongshu.md","D":"platforms/D-xianyu.md","E":"platforms/E-taobao-tmall.md","F":"platforms/F-douyin-mall.md","G":"platforms/G-douyin-live.md","H":"platforms/H-taobao-live.md"}
STAGE_FILE="workflow/pipeline-contract-v2.md";GATE_FILE="workflow/qa-v2.md";EXPRESSION_FILE="workflow/cover-expression-contract-v2.md";SOURCE_FILE="research/platform-evidence-2026-11-27.json"
def read(path):return (ROOT/path).read_text(encoding="utf-8")
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def verify():
 loc=json.loads(read("config/knowledge-locator.json")); ms=sha("manifest.json"); ins=sha("inventory.json")
 ok=ms==loc.get("manifest_sha256") and ins==loc.get("inventory_sha256")
 return {"status":"PASS" if ok else "BLOCKED","manifest_ref":loc.get("manifest_ref"),"manifest_sha_match":ms==loc.get("manifest_sha256"),"inventory_sha_match":ins==loc.get("inventory_sha256"),"scope":"local checkout bytes only; remote commit existence must be verified separately"}
def retrieve(kind,value):
 if kind=="platform":
  mode=value.upper()
  if mode not in PLATFORM_FILES:raise ValueError("platform mode must be A-H")
  return {"kind":kind,"id":mode,"path":PLATFORM_FILES[mode],"content":read(PLATFORM_FILES[mode])}
 if kind=="stage":
  if value not in {"01","02","03","04","05","06"}:raise ValueError("stage id must be 01-06")
  return {"kind":kind,"id":value,"path":STAGE_FILE,"content":read(STAGE_FILE)}
 if kind=="gate":
  if value not in {"G1","G2","G3","G4","G5","G6","G7"}:raise ValueError("gate id must be G1-G7")
  return {"kind":kind,"id":value,"path":GATE_FILE,"content":read(GATE_FILE)}
 if kind=="expression":return {"kind":kind,"id":value or "all","path":EXPRESSION_FILE,"content":read(EXPRESSION_FILE)}
 if kind=="source":
  data=json.loads(read(SOURCE_FILE)); rows=[x for x in data["sources"] if x["id"]==value]
  return {"kind":kind,"id":value,"status":"MATCH" if rows else "NO_MATCH","records":rows}
 raise ValueError("unsupported retrieval kind")
def main():
 p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest="cmd",required=True);sub.add_parser("verify")
 for name in ("platform","stage","gate","expression","source"):
  q=sub.add_parser(name);q.add_argument("--mode" if name=="platform" else "--id",dest="value",required=(name!="expression"))
 a=p.parse_args()
 try:r=verify() if a.cmd=="verify" else retrieve(a.cmd,getattr(a,"value",None))
 except Exception as e:r={"status":"BLOCKED","error":str(e)}
 print(json.dumps(r,ensure_ascii=False,indent=2));sys.exit(0 if r.get("status") in {"PASS","MATCH"} or r.get("content") else 1)
if __name__=="__main__":main()
