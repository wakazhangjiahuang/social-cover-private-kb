#!/usr/bin/env python3
"""Verify real exported image files; exact ratio uses integer cross multiplication."""
import argparse, hashlib, json, struct
from pathlib import Path

def parse_ratio(value):
    a,b=value.split(":"); return int(a),int(b)

def inspect(path,expected_w=None,expected_h=None,ratio=None):
    p=Path(path);result={"path":str(p),"status":"FAIL"}
    if not p.is_file(): result.update(error="FILE_MISSING");return result
    data=p.read_bytes()
    result.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),format=p.suffix.lower().lstrip(".").upper())
    width=height=None;decoded="BLOCKED"
    try:
        from PIL import Image
        with Image.open(p) as im: im.verify()
        with Image.open(p) as im: width,height=im.size
        decoded="PASS"
    except ImportError:
        if data[:8]==b"\x89PNG\r\n\x1a\n" and len(data)>=24:
            width,height=struct.unpack(">II",data[16:24]);decoded="HEADER_ONLY"
    except Exception as e:
        result.update(error="DECODE_ERROR:"+str(e));decoded="FAIL"
    result.update(width=width,height=height,decode_status=decoded)
    if width and height:
        exact=True
        if expected_w and expected_h: exact=exact and width==expected_w and height==expected_h
        if ratio:
            rw,rh=parse_ratio(ratio);exact=exact and width*rh==height*rw
        result["ratio_exact"]=exact
        result["status"]="PASS" if exact and decoded=="PASS" else ("BLOCKED" if decoded!="FAIL" else "FAIL")
    else: result["status"]="BLOCKED" if decoded=="BLOCKED" else "FAIL"
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument("files",nargs="+")
    p.add_argument("--width",type=int);p.add_argument("--height",type=int);p.add_argument("--ratio");p.add_argument("--expected-count",type=int)
    a=p.parse_args();results=[inspect(x,a.width,a.height,a.ratio) for x in a.files]
    unique=len({x.get("sha256") for x in results if x.get("sha256")})==len(results)
    count_ok=a.expected_count is None or len(results)==a.expected_count
    status="PASS" if all(x["status"]=="PASS" for x in results) and unique and count_ok else "FAIL"
    print(json.dumps({"status":status,"unique_files":unique,"count_ok":count_ok,"results":results},ensure_ascii=False,indent=2))
    raise SystemExit(0 if status=="PASS" else 1)
if __name__=="__main__":main()
