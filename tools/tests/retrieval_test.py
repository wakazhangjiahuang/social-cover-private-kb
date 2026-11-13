import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('retrieve',ROOT/'tools/retrieve.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
class RetrievalTests(unittest.TestCase):
    def test_exact_id(self):self.assertEqual([x['id'] for x in r.layouts(id='a01')['records']],['A01'])
    def test_family(self):self.assertEqual(r.layouts(family='C',limit=64)['total'],8)
    def test_platform_source_counts(self):
        for mode,n in [('A',21),('B',21),('C',22)]:self.assertEqual(r.layouts(platform=mode,primary_only=True,limit=64)['total'],n)
    def test_platform_preference_is_not_exclusion(self):self.assertEqual(r.layouts(platform='A',limit=64)['total'],64)
    def test_cross_platform_exact_id(self):self.assertEqual(r.layouts(id='A01',platform='A')['total'],1)
    def test_missing_structure_no_forced_match(self):self.assertEqual(r.layouts(structure='L15')['total'],0)
    def test_real_photo_does_not_match_ai(self):self.assertEqual(r.layouts(nature='REAL_PHOTO')['total'],0)
    def test_illustration_does_not_match_titles_about_art(self):self.assertEqual(r.layouts(nature='ILLUSTRATION')['total'],0)
    def test_list(self):self.assertEqual([x['id'] for x in r.layouts(structure='L05')['records']],['F02'])
    def test_comparison(self):self.assertEqual([x['id'] for x in r.layouts(structure='L07')['records']],['F03'])
    def test_steps(self):self.assertEqual({x['id'] for x in r.layouts(structure='L13')['records']},{'A08','F01','F07','F08'})
    def test_impossible_filters(self):self.assertEqual(r.layouts(id='F03',structure='L05')['total'],0)
    def test_literal_query(self):self.assertEqual(r.layouts(query='AI工作台')['records'][0]['id'],'A06')
    def test_workroom_negative_space(self):
        result=r.layouts(family='H',query='工作室 负空间')
        self.assertGreater(result['total'],0)
        self.assertTrue(all(x['source_asset']=='assets/photo5.png' for x in result['records']))
    def test_no_match(self):self.assertEqual(r.layouts(query='不存在的筛选词XYZ')['total'],0)
    def test_namespaced_C01(self):
        self.assertEqual(r.layouts(id='C01')['records'][0]['name'],'半包围人物')
        self.assertEqual(r.records('component',id='C01')['records'][0]['name'],'画布与展示面')
    def test_original_counts(self):
        self.assertEqual(r.records('hook',limit=500)['total'],225)
        self.assertEqual(r.records('title',limit=500)['total'],225)
        self.assertEqual(r.records('formula',limit=500)['total'],10)
        self.assertEqual(sum(len(x['fields']) for x in r.records('component',limit=500)['records']),179)
    def test_original_hook_id(self):self.assertEqual(r.records('hook',id='user-hook-001')['total'],1)
    def test_coverage_is_explicit(self):
        d=r.read('catalog/layout-index.json')
        self.assertEqual(len(d['structure_coverage']),17)
        self.assertEqual(sum(bool(ids) for ids in d['structure_coverage'].values()),8)
if __name__=='__main__':unittest.main()
