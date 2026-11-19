"""Regression probes for gates, file/ZIP identity and scoped recall."""
import copy,importlib.util,json,shutil,sys,tempfile,unittest,zipfile
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
core=load('title_core',ROOT/'tools/title_core.py')
files=load('image_check',ROOT/'tools/check_image_export.py')
filters=load('candidate_filter_test',ROOT/'tools/candidate_filter.py')
assets=load('asset_client',ROOT/'scripts/cover_assets.py')
def title_record():
 return {'hard_gates':{k:{'status':'PASS','evidence_refs':['TASK']} for k in core.GATES},
 'evidence_registry':{'TASK':{'locator':'user-input:fixture-facts'}},
 'dimensions':{f'D{i}':{'score':2,'reason':'fixture editorial reason','evidence':['TASK']} for i in range(1,9)}}
class Gates(unittest.TestCase):
 def test_complete(self):self.assertEqual(core.aggregate(title_record())['score'],16)
 def test_empty(self):
  r=title_record();r['hard_gates']={};self.assertEqual(core.aggregate(r)['status'],'HOLD')
 def test_each_missing(self):
  for k in core.GATES:
   r=title_record();del r['hard_gates'][k];self.assertIsNone(core.aggregate(r)['score'])
 def test_invalid_key(self):
  r=title_record();r['hard_gates']['truth']='PASS'
  with self.assertRaises(ValueError):core.aggregate(r)
 def test_invalid_status(self):
  r=title_record();r['hard_gates']['platform_scope']['status']='OK'
  with self.assertRaises(ValueError):core.aggregate(r)
 def test_unknown_states(self):
  for state in ['UNKNOWN','NOT_RUN','BLOCKED']:
   r=title_record();r['hard_gates']['platform_scope']['status']=state
   self.assertEqual(core.aggregate(r)['status'],'HOLD')
 def test_failure(self):
  r=title_record();r['hard_gates']['truth_and_evidence']['status']='FAIL'
  self.assertEqual(core.aggregate(r)['status'],'FAIL')
 def test_missing_evidence(self):
  r=title_record();r['evidence_registry']={};self.assertEqual(core.aggregate(r)['status'],'HOLD')
 def test_unresolved_dimension_evidence(self):
  r=title_record();r['dimensions']['D1']['evidence']=['FAKE']
  with self.assertRaises(ValueError):core.aggregate(r)
 def test_bool_score(self):
  r=title_record();r['dimensions']['D1']['score']=True
  with self.assertRaises(ValueError):core.aggregate(r)
 def test_blank_reason(self):
  r=title_record();r['dimensions']['D1']['reason']=' '
  with self.assertRaises(ValueError):core.aggregate(r)
class Delivery(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
  self.a=self.root/'a.png';self.b=self.root/'b.png'
  Image.new('RGB',(144,256),'white').save(self.a);Image.new('RGB',(144,256),'green').save(self.b)
  self.rows=files.check_files([self.a,self.b],144,256,count=2)['files']
 def tearDown(self):self.tmp.cleanup()
 def test_valid_images(self):self.assertEqual(files.check_files([self.a,self.b],144,256,count=2)['status'],'PASS')
 def test_same_path(self):self.assertEqual(files.check_files([self.a,self.a],144,256,count=2)['status'],'FAIL')
 def test_same_content(self):
  c=self.root/'copy.png';shutil.copy2(self.a,c)
  self.assertEqual(files.check_files([self.a,c],144,256)['status'],'FAIL')
 def test_wrong_size(self):self.assertEqual(files.check_files([self.a],145,256)['status'],'FAIL')
 def test_bad_image(self):
  self.a.write_bytes(b'bad');self.assertEqual(files.check_files([self.a],144,256)['status'],'FAIL')
 def test_exact_zip(self):
  p=self.root/'final.zip';files.write_zip(p,self.rows);self.assertEqual(files.check_zip(p,self.rows)['status'],'PASS')
 def test_missing_zip_entry(self):
  p=self.root/'bad.zip'
  with zipfile.ZipFile(p,'w') as z:z.write(self.a,'a.png')
  self.assertEqual(files.check_zip(p,self.rows)['status'],'FAIL')
 def test_extra_zip_entry(self):
  p=self.root/'bad.zip';files.write_zip(p,self.rows)
  with zipfile.ZipFile(p,'a') as z:z.writestr('note.txt','extra')
  self.assertEqual(files.check_zip(p,self.rows)['status'],'FAIL')
 def test_duplicate_zip_entry(self):
  import warnings
  p=self.root/'bad.zip';files.write_zip(p,self.rows)
  with warnings.catch_warnings():
   warnings.simplefilter('ignore')
   with zipfile.ZipFile(p,'a') as z:z.write(self.a,'a.png')
  self.assertEqual(files.check_zip(p,self.rows)['status'],'FAIL')
 def test_hash_mismatch(self):
  p=self.root/'bad.zip'
  with zipfile.ZipFile(p,'w') as z:z.write(self.b,'a.png');z.write(self.a,'b.png')
  self.assertEqual(files.check_zip(p,self.rows)['status'],'FAIL')
 def test_bad_archive(self):
  p=self.root/'bad.zip';p.write_bytes(b'corrupt');self.assertEqual(files.check_zip(p,self.rows)['status'],'FAIL')
 def test_bad_crc(self):
  p=self.root/'bad.zip'
  with zipfile.ZipFile(p,'w',compression=zipfile.ZIP_STORED) as z:z.write(self.a,'a.png');z.write(self.b,'b.png')
  raw=bytearray(p.read_bytes())
  with zipfile.ZipFile(p) as z:
   i=z.getinfo('a.png');offset=i.header_offset+30+len(i.filename.encode())+len(i.extra)
  raw[offset+20]^=255;p.write_bytes(raw)
  self.assertEqual(files.check_zip(p,self.rows)['status'],'FAIL')
class Recall(unittest.TestCase):
 def setUp(self):
  self.rows=[{'id':'x','text':'AI教程','category':'教程','applicability':{'platforms':{'A':'UNKNOWN'},'surfaces':{'cover_main_title':'REVIEW_REQUIRED'},'industry_scope':['AI_EDUCATION'],'motives':['knowledge_value'],'evidence_prerequisites':['content_fulfillment'],'rewrite_required':False}}]
 def test_unknown_platform_excluded(self):self.assertEqual(filters.select(self.rows,platform='A')['total'],0)
 def test_explicit_draft(self):
  r=filters.select(self.rows,platform='A',include_unverified=True)
  self.assertEqual(r['total'],1);self.assertFalse(r['records'][0]['platform_certified'])
 def test_industry_mismatch(self):self.assertEqual(filters.select(self.rows,industry='INFANT_PRINT')['total'],0)
 def test_evidence_missing(self):self.assertEqual(filters.select(self.rows,evidence=[])['total'],0)
 def test_evidence_supplied(self):self.assertEqual(filters.select(self.rows,evidence=['content_fulfillment'])['total'],1)
 def test_rewrite_excluded(self):
  self.rows[0]['applicability']['rewrite_required']=True
  self.assertEqual(filters.select(self.rows,evidence=['content_fulfillment'])['total'],0)
 def test_source_filter(self):
  idx=assets.read('assets/cover-64-index.json')
  r=assets.query(idx,'A',limit=64,primary_only=True)
  self.assertEqual(r['matching_records'],21)
  self.assertTrue(all(x['source_platform']=='douyin' for x in r['candidates']))
 def test_real_photo_no_match(self):
  self.assertEqual(assets.query(assets.read('assets/cover-64-index.json'),'A',nature='REAL_PHOTO')['matching_records'],0)
if __name__=='__main__':unittest.main()
