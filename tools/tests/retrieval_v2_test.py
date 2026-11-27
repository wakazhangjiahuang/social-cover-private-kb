import importlib.util,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("retrieve_v2",ROOT/"tools/retrieve_v2.py")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class TestRetrieveV2(unittest.TestCase):
 def test_eight_platforms_registered(self):self.assertEqual(set(mod.PLATFORM_FILES),set("ABCDEFGH"))
 def test_each_platform_path_exists(self):
  for path in mod.PLATFORM_FILES.values():self.assertTrue((ROOT/path).is_file(),path)
 def test_pipeline_and_qa_exist(self):self.assertTrue((ROOT/mod.STAGE_FILE).is_file());self.assertTrue((ROOT/mod.GATE_FILE).is_file())
 def test_source_register_exists(self):self.assertTrue((ROOT/mod.SOURCE_FILE).is_file())
if __name__=="__main__":unittest.main()
