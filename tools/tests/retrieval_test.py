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
    def test_style_count(self):self.assertEqual(r.styles(limit=30)['total'],18)
    def test_style_exact_id(self):self.assertEqual(r.styles(id='hand-drawn-border')['records'][0]['name'],'手绘边框')
    def test_style_literal_and(self):self.assertEqual(r.styles(query='手绘 边框')['records'][0]['id'],'hand-drawn-border')
    def test_style_unknown(self):self.assertEqual(r.styles(id='C01')['total'],0)
    def test_styles_have_no_task_evidence(self):self.assertTrue(all(x['evidence_nature']=='STYLE_REFERENCE_NOT_TASK_EVIDENCE' for x in r.styles(limit=30)['records']))
    def test_style_prompt_is_opt_in(self):
        self.assertNotIn('source_preset',r.styles(id='neon-contrast')['records'][0])
        self.assertIn('prompt',r.styles(id='neon-contrast',include_prompt=True)['records'][0]['source_preset'])
    def test_style_queries_do_not_search_claims_in_raw_prompt(self):self.assertEqual(r.styles(query='亲测')['total'],0)
    def test_joint_is_reference_pair_not_render(self):
        x=r.joint(style_id='neon-contrast',structure='L05',platform='C')
        self.assertEqual(x['style']['records'][0]['id'],'neon-contrast')
        self.assertEqual(x['layouts']['records'][0]['id'],'F02')
        self.assertFalse(x['premade_combined_image']);self.assertFalse(x['rendered_or_platform_tested'])
    def test_joint_does_not_force_uncovered_structure(self):self.assertEqual(r.joint(style_id='neon-contrast',structure='L15',platform='A')['layouts']['total'],0)
    def test_deleted_duplicate_components_still_readable(self):self.assertEqual(r.records('component',limit=30)['total'],18)
    def test_runtime_manifest_excludes_noise(self):
        m=r.read('manifest.json')
        self.assertFalse(any(x['path'].startswith(('sources/','workbench/','maintenance/','examples/')) for x in m['assets']))
    def test_metadata_stays_inferred(self):self.assertTrue(all(x['metadata_status']=='INFERRED_EDITOR_HINTS' for x in r.styles(limit=30)['records']))
if __name__=='__main__':unittest.main()
