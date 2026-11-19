#!/usr/bin/env python3
"""Deterministic cover-title character and line-budget gate; never judges semantics or marketing effect."""
import argparse
import json
import re
import sys

try:
    import regex
except ImportError:
    regex = None

def _strip_layout_breaks(value):
    return (value or "").replace("\r", "").replace("\n", "")

def clusters(value):
    if regex is None:
        raise RuntimeError("Install regex; Unicode grapheme counting must not fall back to code points")
    return len(regex.findall(r"\X", _strip_layout_breaks(value)))

def han_count(value):
    if regex is None:
        raise RuntimeError("Install regex; Unicode script counting must not fall back to code points")
    return len(regex.findall(r"\p{Script=Han}", _strip_layout_breaks(value)))

def line_count(value, declared=None):
    if declared is not None:
        return declared
    if not value:
        return 0
    return max(1, len((value or "").splitlines()))

def assess(main, subtitle="", metadata="", cta="", mode="image-led",
           main_lines=None, subtitle_lines=None, cta_authorized=False,
           locked_exception=False, visual_check="NOT_RUN",
           hero_ratio=None, text_ratio=None, subtitle_font_ratio=None):
    issues, warnings = [], []
    main_visible = clusters(main)
    main_han = han_count(main)
    subtitle_visible = clusters(subtitle)
    metadata_visible = clusters(metadata)
    cta_visible = clusters(cta)
    ml = line_count(main, main_lines)
    sl = line_count(subtitle, subtitle_lines)

    if mode not in {"image-led", "text-led", "overlay"}:
        issues.append("mode必须是image-led/text-led/overlay")
    if visual_check not in {"PASS", "FAIL", "NOT_RUN", "NOT_APPLICABLE"}:
        issues.append("visual_check状态无效")
    if not (main or "").strip():
        issues.append("主标题不能为空")
    if main_han > 15:
        if locked_exception:
            warnings.append(f"锁定主标题含{main_han}个汉字，超过15字默认值；保留原文并要求人工确认版式")
        else:
            issues.append(f"主标题含{main_han}个汉字，超过15字默认上限")
    if main_visible > 15:
        warnings.append(f"主标题有{main_visible}个可见字素簇（其中汉字{main_han}个）；需在实际封面检查英文/数字/符号字宽与断行")
    if subtitle_visible > 18:
        if locked_exception:
            warnings.append(f"锁定副标题有{subtitle_visible}个可见字素簇，超过18个默认值；保留原文并要求人工确认版式")
        else:
            issues.append(f"副标题有{subtitle_visible}个可见字素簇，超过18个默认上限")
    if ml < 1 or ml > 3:
        issues.append(f"主标题为{ml}行；允许1–3行")
    if subtitle and (sl < 1 or sl > 2):
        issues.append(f"副标题为{sl}行；允许1–2行")
    if cta and not cta_authorized:
        issues.append("出现CTA但本轮未明确授权")
    if metadata_visible:
        warnings.append("地点/品牌/系列标签为独立字段，不并入主副标题字符预算；仍需检查整体视觉拥挤")
    if cta_visible:
        warnings.append("CTA为独立行动字段，不并入主副标题字符预算；需确认其授权与版式层级")

    if mode == "image-led":
        if visual_check == "FAIL":
            issues.append("完整封面视觉检查失败")
        elif visual_check != "PASS":
            warnings.append("完整封面主视觉/文字层级/缩略图检查尚未完成，视觉状态NOT_RUN")
    elif mode == "overlay":
        if visual_check not in {"NOT_APPLICABLE", "NOT_RUN"}:
            warnings.append("透明文字叠加素材不是完整封面；请在合成后的完整封面再执行视觉检查")
        warnings.append("透明文字叠加素材不含完整主画面，主视觉占比与缩略图状态NOT_APPLICABLE")
    else:
        warnings.append("当前为纯文案任务，视觉状态NOT_RUN")

    for name, value in (("hero_ratio", hero_ratio), ("text_ratio", text_ratio), ("subtitle_font_ratio", subtitle_font_ratio)):
        if value is not None and not 0 <= value <= 1:
            issues.append(f"{name}必须在0到1之间")

    if issues:
        status = "FAIL"
    elif mode == "overlay":
        status = "TEXT_BUDGET_PASS_VISUAL_NOT_APPLICABLE"
    elif mode == "text-led":
        status = "TEXT_BUDGET_PASS_VISUAL_NOT_RUN"
    elif visual_check == "PASS":
        status = "PASS"
    else:
        status = "TEXT_BUDGET_PASS_VISUAL_NOT_RUN"

    return {
        "status": status,
        "mode": mode,
        "counts": {
            "main_han": main_han,
            "main_visible_graphemes": main_visible,
            "subtitle_visible_graphemes": subtitle_visible,
            "metadata_visible_graphemes": metadata_visible,
            "cta_visible_graphemes": cta_visible,
            "all_visible_graphemes": main_visible + subtitle_visible + metadata_visible + cta_visible
        },
        "limits": {
            "main_han_max": 15,
            "subtitle_visible_graphemes_max": 18,
            "main_lines": "1–3",
            "subtitle_lines": "1–2",
            "metadata_and_cta": "separate_fields_not_in_main_subtitle_budget",
            "locked_exception": bool(locked_exception)
        },
        "line_counts": {"main": ml, "subtitle": sl},
        "visual_measurements": {
            "visual_check": visual_check,
            "hero_ratio": hero_ratio,
            "text_ratio": text_ratio,
            "subtitle_font_ratio": subtitle_font_ratio,
            "fixed_universal_area_threshold": False
        },
        "issues": issues,
        "warnings": warnings,
        "semantic_quality": "NOT_EVALUATED",
        "marketing_effect": "NOT_RUN"
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--main", required=True)
    p.add_argument("--subtitle", default="")
    p.add_argument("--metadata", default="")
    p.add_argument("--cta", default="")
    p.add_argument("--mode", choices=["image-led", "text-led", "overlay"], default="image-led")
    p.add_argument("--main-lines", type=int)
    p.add_argument("--subtitle-lines", type=int)
    p.add_argument("--cta-authorized", action="store_true")
    p.add_argument("--locked-exception", action="store_true")
    p.add_argument("--visual-check", choices=["PASS", "FAIL", "NOT_RUN", "NOT_APPLICABLE"], default="NOT_RUN")
    p.add_argument("--hero-ratio", type=float)
    p.add_argument("--text-ratio", type=float)
    p.add_argument("--subtitle-font-ratio", type=float)
    a = p.parse_args()
    try:
        result = assess(
            a.main, a.subtitle, a.metadata, a.cta, a.mode,
            a.main_lines, a.subtitle_lines, a.cta_authorized,
            a.locked_exception, a.visual_check,
            a.hero_ratio, a.text_ratio, a.subtitle_font_ratio
        )
    except (RuntimeError, ValueError) as exc:
        print(json.dumps({"status": "BLOCKED", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["status"] == "FAIL" else 0

if __name__ == "__main__":
    raise SystemExit(main())
