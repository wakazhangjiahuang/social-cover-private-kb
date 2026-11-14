#!/usr/bin/env python3
"""Task-first routing. Platform selection is required only for image-production tasks."""
import argparse, json

PRODUCTION = {"create", "redesign", "series"}
NON_PRODUCTION = {"title_only", "analysis", "repair", "review"}

def route(task, platform_modes=None, requested_count=None):
    if task not in PRODUCTION | NON_PRODUCTION:
        raise ValueError("Unknown task")
    platforms = list(dict.fromkeys(platform_modes or []))
    if any(p not in {"A", "B", "C"} for p in platforms):
        raise ValueError("platform_modes must contain only A/B/C")
    if task not in PRODUCTION:
        default_count = 1 if task == "repair" else 0
        count = requested_count if requested_count is not None else default_count
        return {"task":task,"requires_platform":False,"platform_modes":platforms,
          "platform_status":"OPTIONAL_NOT_REQUIRED","image_generation":task=="repair",
          "default_count":count,"six_to_three":False,"deliver_zip":task=="repair" and count>0,
          "route":{"title_only":"TITLE_ONLY","analysis":"ANALYSIS_ONLY","repair":"SOURCE_PRESERVING_REPAIR","review":"REVIEW_ONLY"}[task]}
    count=requested_count if requested_count is not None else 3
    if count<1: raise ValueError("Production task count must be >= 1")
    return {"task":task,"requires_platform":True,"platform_modes":platforms,
      "platform_status":"SELECT_OR_INFER" if not platforms else "READY",
      "image_generation":True,"default_count":count,"six_to_three":True,"deliver_zip":True,
      "count_scope":"per_platform" if task=="series" and len(platforms)>1 else "total","route":"IMAGE_PRODUCTION"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--task",required=True,choices=sorted(PRODUCTION|NON_PRODUCTION))
    p.add_argument("--platform",action="append",default=[])
    p.add_argument("--count",type=int)
    p.add_argument("--self-test",action="store_true")
    a=p.parse_args()
    if a.self_test:
        assert route("analysis")["requires_platform"] is False
        assert route("title_only")["image_generation"] is False
        assert route("repair")["default_count"]==1
        assert route("review")["six_to_three"] is False
        assert route("create",["A"])["default_count"]==3
        assert route("series",["A","C"])["count_scope"]=="per_platform"
        print("PASS task-router self-test: 6 cases"); return
    print(json.dumps(route(a.task,a.platform,a.count),ensure_ascii=False,indent=2))
if __name__=="__main__": main()
