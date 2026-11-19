import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cover_title_gate", ROOT / "tools/cover_title_gate.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class TitleGateV6(unittest.TestCase):
    def test_hs01_positive_reference(self):
        r = mod.assess("帮这座小城多一个被看见的理由", "让你的镜头成为英德山野的另一种介绍",
                       mode="overlay", main_lines=3, subtitle_lines=2)
        self.assertEqual(r["status"], "TEXT_BUDGET_PASS_VISUAL_NOT_APPLICABLE")
        self.assertEqual(r["counts"]["main_han"], 14)
        self.assertEqual(r["counts"]["subtitle_visible_graphemes"], 17)

    def test_hs02_separate_label(self):
        r = mod.assess("家乡这一池暖，想请你来讲讲", "让你的周末推荐多一站英德",
                       metadata="长寿桥温泉创作邀约", mode="overlay", main_lines=3)
        self.assertEqual(r["status"], "TEXT_BUDGET_PASS_VISUAL_NOT_APPLICABLE")
        self.assertEqual(r["counts"]["main_han"], 12)
        self.assertEqual(r["counts"]["main_visible_graphemes"], 13)
        self.assertEqual(r["counts"]["metadata_visible_graphemes"], 9)

    def test_hs03_positive_reference(self):
        r = mod.assess("让粉丝记住，是你推荐的这一站", "先认真体验，再写你的真实推荐",
                       mode="overlay", main_lines=3, subtitle_lines=2)
        self.assertEqual(r["status"], "TEXT_BUDGET_PASS_VISUAL_NOT_APPLICABLE")
        self.assertEqual(r["counts"]["main_han"], 13)
        self.assertEqual(r["counts"]["subtitle_visible_graphemes"], 14)

    def test_hs04_positive_reference(self):
        r = mod.assess("你的镜头也能参与小店成长", "从一条真实建议，聊到一次在地共创",
                       mode="overlay", main_lines=3, subtitle_lines=2)
        self.assertEqual(r["status"], "TEXT_BUDGET_PASS_VISUAL_NOT_APPLICABLE")
        self.assertEqual(r["counts"]["main_han"], 12)
        self.assertEqual(r["counts"]["subtitle_visible_graphemes"], 16)

    def test_main_15_chinese_characters_pass(self):
        self.assertEqual(mod.assess("这是一条十五个汉字的标题", mode="text-led")["status"], "TEXT_BUDGET_PASS_VISUAL_NOT_RUN")

    def test_main_16_chinese_characters_fails(self):
        r = mod.assess("这是一条超过十五个汉字的标题测试", mode="text-led")
        self.assertEqual(r["status"], "FAIL")

    def test_subtitle_18_visible_characters_pass(self):
        r = mod.assess("婴童家纺新机会", "2027SS欧洲花卉趋势与原创试稿", mode="text-led")
        self.assertNotEqual(r["status"], "FAIL")

    def test_subtitle_19_visible_characters_fails(self):
        r = mod.assess("婴童家纺新机会", "2027SS欧洲花卉趋势与原创试稿方法", mode="text-led")
        self.assertEqual(r["status"], "FAIL")

    def test_main_three_lines_allowed(self):
        self.assertNotEqual(mod.assess("第一行\n第二行\n第三行", mode="text-led")["status"], "FAIL")

    def test_main_four_lines_fails(self):
        self.assertEqual(mod.assess("第一行\n第二行\n第三行\n第四行", mode="text-led")["status"], "FAIL")

    def test_subtitle_two_lines_allowed(self):
        self.assertNotEqual(mod.assess("主标题", "第一行\n第二行", mode="text-led")["status"], "FAIL")

    def test_english_title_is_not_miscounted_as_han(self):
        r = mod.assess("走进 Peter Rabbit style", "DIY笔刷｜英式田园线条＋淡水彩", mode="text-led")
        self.assertEqual(r["counts"]["main_han"], 2)
        self.assertGreater(r["counts"]["main_visible_graphemes"], 15)
        self.assertTrue(any("实际封面检查" in w for w in r["warnings"]))

    def test_no_total_24_character_cap(self):
        r = mod.assess("帮这座小城多一个被看见的理由", "让你的镜头成为英德山野的另一种介绍",
                       metadata="清远·英德｜长寿桥温泉", cta="探店／文旅创作者共创邀约",
                       mode="overlay", cta_authorized=True, main_lines=3, subtitle_lines=2)
        self.assertNotEqual(r["status"], "FAIL")
        self.assertGreater(r["counts"]["all_visible_graphemes"], 24)

    def test_cta_requires_authorization(self):
        self.assertEqual(mod.assess("英德小城新选题", "让你的镜头成为另一种介绍",
                                    cta="立即报名", mode="text-led")["status"], "FAIL")

    def test_locked_long_subtitle_is_preserved_as_exception(self):
        r = mod.assess("春夏凉席|图案风格怎么选？", "2027SS母婴家纺｜TOP 5 Style",
                       mode="text-led", locked_exception=True)
        self.assertNotEqual(r["status"], "FAIL")
        self.assertTrue(any("锁定副标题" in w for w in r["warnings"]))

    def test_full_cover_requires_visual_review(self):
        r = mod.assess("婴童家纺新机会", "2027SS欧洲花卉趋势", mode="image-led")
        self.assertEqual(r["status"], "TEXT_BUDGET_PASS_VISUAL_NOT_RUN")

    def test_visual_fail_is_fail(self):
        r = mod.assess("婴童家纺新机会", "2027SS欧洲花卉趋势", mode="image-led", visual_check="FAIL")
        self.assertEqual(r["status"], "FAIL")

    def test_visual_pass_requires_explicit_review(self):
        r = mod.assess("婴童家纺新机会", "2027SS欧洲花卉趋势", mode="image-led", visual_check="PASS")
        self.assertEqual(r["status"], "PASS")

    def test_emoji_grapheme_count(self):
        self.assertEqual(mod.clusters("🐶"), 1)

    def test_line_breaks_not_counted_as_characters(self):
        self.assertEqual(mod.clusters("第一行\n第二行"), len("第一行第二行"))

    def test_positive_case_metadata_counts_match(self):
        data = json.loads((ROOT / "references/hot-spring-positive-cases-v2.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["cases"]), 4)
        for case in data["cases"]:
            self.assertLessEqual(case["main_han_count"], 15)
            self.assertLessEqual(case["subtitle_visible_graphemes"], 18)

if __name__ == "__main__":
    unittest.main()
