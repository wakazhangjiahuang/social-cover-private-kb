#!/usr/bin/env python3
"""Verify real image files, uniqueness and an optional exact ZIP of those files."""
import argparse,hashlib,json,os,stat,tempfile,zipfile
from pathlib import Path
from PIL import Image
def digest(raw):return hashlib.sha256(raw).hexdigest()
def check_files(files,width,height,fmt="PNG",count=None):
 errors=[];rows=[];paths=set();hashes=set();names=set()
 if count is not None and len(files)!=count:errors.append(f"expected {count} files, got {len(files)}")
 if not files or width<1 or height<1:errors.append("positive dimensions and at least one image required")
 for name in files:
  path=Path(name).resolve()
  try:
   raw=path.read_bytes()
   with Image.open(path) as im:im.verify()
   with Image.open(path) as im:im.load();w,h=im.size;actual_format=im.format
   sha=digest(raw)
   if path in paths:errors.append("duplicate path: "+str(path))
   if sha in hashes:errors.append("duplicate image content: "+str(path))
   if path.name.casefold() in names:errors.append("duplicate archive filename: "+path.name)
   paths.add(path);hashes.add(sha);names.add(path.name.casefold())
   ok=(w==width and h==height and actual_format==fmt and w*height==h*width)
   if not ok:errors.append("image dimensions/format mismatch: "+str(path))
   rows.append({"path":str(path),"sha256":sha,"width":w,"height":h,"format":actual_format,"bytes":len(raw),"ratio_exact":w*height==h*width,"status":"PASS" if ok else "FAIL"})
  except Exception as exc:errors.append(str(path)+": "+str(exc))
 return {"status":"FAIL" if errors else "PASS","files":rows,"errors":errors,"scope":"file bytes/format/dimensions/uniqueness only; not visual quality"}
def check_zip(archive,rows):
 expected={Path(r["path"]).name:r for r in rows};errors=[];entries=[]
 try:
  with zipfile.ZipFile(archive) as z:
   infos=z.infolist();names=[i.filename for i in infos]
   if len(set(names))!=len(names):errors.append("duplicate ZIP entry names")
   if len({n.casefold() for n in names})!=len(names):errors.append("case-colliding ZIP entries")
   if set(names)!=set(expected):errors.append("ZIP entries differ from final image list")
   for info in infos:
    name=info.filename
    if info.is_dir() or "/" in name or "\\" in name or name in {".",".."}:errors.append("unexpected directory/path in ZIP: "+name);continue
    if info.flag_bits&1 or stat.S_ISLNK(info.external_attr>>16):errors.append("encrypted/symlink ZIP entry: "+name);continue
    if name not in expected:continue
    row=expected[name]
    if info.file_size!=row["bytes"]:errors.append("ZIP size mismatch: "+name);continue
    content=z.read(info);sha=digest(content)
    if sha!=row["sha256"]:errors.append("ZIP hash mismatch: "+name)
    entries.append({"name":name,"sha256":sha,"bytes":len(content),"crc_checked":True})
 except (OSError,ValueError,RuntimeError,zipfile.BadZipFile,EOFError) as exc:errors.append(str(exc))
 return {"status":"FAIL" if errors else "PASS","path":str(Path(archive).resolve()),"entries":entries,"errors":errors,"scope":"exact final files, decompression/CRC and SHA256"}
def write_zip(archive,rows):
 target=Path(archive).resolve()
 if target in {Path(r["path"]) for r in rows}:raise ValueError("ZIP cannot overwrite an image")
 target.parent.mkdir(parents=True,exist_ok=True)
 fd,tmp=tempfile.mkstemp(prefix=".cover-zip-",suffix=".zip",dir=target.parent);os.close(fd)
 try:
  with zipfile.ZipFile(tmp,"w",compression=zipfile.ZIP_DEFLATED) as z:
   for row in rows:z.write(row["path"],Path(row["path"]).name)
  result=check_zip(tmp,rows)
  if result["status"]!="PASS":raise ValueError(str(result["errors"]))
  os.replace(tmp,target)
 finally:
  if Path(tmp).exists():Path(tmp).unlink()
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("files",nargs="+")
 p.add_argument("--width",type=int,required=True);p.add_argument("--height",type=int,required=True)
 p.add_argument("--format",default="PNG",choices=["PNG","JPEG","WEBP"]);p.add_argument("--count",type=int)
 g=p.add_mutually_exclusive_group();g.add_argument("--zip",dest="archive");g.add_argument("--write-zip")
 p.add_argument("--require-zip",action="store_true");a=p.parse_args()
 result=check_files(a.files,a.width,a.height,a.format,a.count);archive=a.archive or a.write_zip
 if result["status"]=="PASS" and a.write_zip:
  try:write_zip(a.write_zip,result["files"])
  except Exception as exc:result["errors"].append(str(exc));result["status"]="FAIL"
 if archive and result["status"]=="PASS":
  result["zip"]=check_zip(archive,result["files"])
  if result["zip"]["status"]!="PASS":result["status"]="FAIL"
 if a.require_zip and not archive:result["status"]="FAIL";result["errors"].append("final delivery requires an actual ZIP")
 if not archive:result["zip"]={"status":"NOT_RUN"}
 print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(0 if result["status"]=="PASS" else 1)
if __name__=="__main__":main()
