#!/usr/bin/env python3
"""Check the saved support-file set; run before using local asset clients."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
def check():
 contract=json.loads((ROOT/'config/package-files.json').read_text())
 missing=[];changed=[]
 for row in contract['files']:
  p=ROOT/row['path']
  if not p.is_file():missing.append(row['path'])
  elif hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:changed.append(row['path'])
 return {'status':'PACKAGE_VERIFIED' if not missing and not changed else 'BLOCKED',
         'version':contract['version'],'required_files':len(contract['files']),
         'missing':missing,'changed':changed,'scope':'support-file presence and bytes only'}
if __name__=='__main__':
 try:r=check()
 except Exception as exc:r={'status':'BLOCKED','error':str(exc)}
 print(json.dumps(r,ensure_ascii=False,indent=2));sys.exit(0 if r['status']=='PACKAGE_VERIFIED' else 1)
