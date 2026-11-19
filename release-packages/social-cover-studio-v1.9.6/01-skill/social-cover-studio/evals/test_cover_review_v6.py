import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('cover_review_v6',ROOT/'tools/cover_review.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

def make(scope='cover',score=3):
    keys=(mod.RUBRIC['hard_gates'] if scope=='text_only' else
          mod.RUBRIC['hard_gates']+mod.RUBRIC.get('visual_gate_for_full_cover',[]))
    dims={d['id']:{'score':score,'reason':'fixture score is only an arithmetic test','evidence':['E1']}
          for d in mod.RUBRIC['dimensions']
          if scope=='cover' or d['id'] not in mod.RUBRIC['text_only']['excluded_dimensions']}
    return {
      'review_scope':scope,
      'hard_gates':{k:{'status':'PASS','evidence_refs':['E1']} for k in keys},
      'evidence_registry':{'E1':{'locator':'fixture://not-real-evidence'}},
      'dimensions':dims
    }

class ReviewV6(unittest.TestCase):
    def test_cover_score(self):
        self.assertEqual(mod.aggregate(make())['score'],75)

    def test_text_only_max_95(self):
        r=mod.aggregate(make('text_only',4))
        self.assertEqual(r['max_score'],95)
        self.assertEqual(r['status'],'TEXT_ONLY_TRIAL')

    def test_missing_click_gate_holds(self):
        r=make(); del r['hard_gates']['click_reason']
        self.assertEqual(mod.aggregate(r)['status'],'HOLD')

    def test_failed_pair_complementarity_fails(self):
        r=make(); r['hard_gates']['pair_complementarity']['status']='FAIL'
        self.assertEqual(mod.aggregate(r)['status'],'FAIL')

    def test_missing_visual_gate_holds_for_cover(self):
        r=make(); del r['hard_gates']['visual_dominance']
        self.assertEqual(mod.aggregate(r)['status'],'HOLD')

    def test_visual_gate_not_required_for_text_only(self):
        r=make('text_only',4)
        self.assertNotIn('visual_dominance',r['hard_gates'])
        self.assertEqual(mod.aggregate(r)['status'],'TEXT_ONLY_TRIAL')

    def test_low_critical_dimension_revises(self):
        r=make(); r['dimensions']['D6']['score']=2
        self.assertIn('D6',mod.aggregate(r)['weak_dimensions'])

    def test_evidence_locator_required(self):
        r=make(); r['evidence_registry']['E1']['locator']=' '
        self.assertEqual(mod.aggregate(r)['status'],'HOLD')

if __name__=='__main__': unittest.main()
