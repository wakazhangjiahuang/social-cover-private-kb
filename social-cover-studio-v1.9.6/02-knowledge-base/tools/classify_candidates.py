#!/usr/bin/env python3
"""Add conservative, reproducible per-record metadata without changing originals."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
MOTIVES={"人群":"self_relevance","身份":"self_relevance","数字":"save_reference","清单":"save_reference","收藏":"save_reference","痛点":"problem_relief","焦虑":"problem_relief","悬念":"curiosity","提问":"curiosity","信息差":"curiosity","反常识":"curiosity","冲突":"curiosity","成本":"practical_value","收益":"practical_value","教程":"knowledge_value","SOP":"knowledge_value","低门槛":"practical_value","对比":"comparison","测评":"comparison","案例":"result_proof","经验":"result_proof","复盘":"result_proof","种草":"purchase_consideration","销售":"purchase_consideration","热点":"novelty","趋势":"novelty","损失":"risk_reduction","FOMO":"risk_reduction","社会证明":"trust","权威":"trust","搜索":"search_intent","SEO":"search_intent","互动":"participation"}
def classify(row):
 text=row["text"];category=row["category"];needs={"content_fulfillment"};risks=[]
 for pattern,requirement in [
  (r"数字|[0-9]|百分|小时|分钟|倍|省下|成本|收益|结果","numeric_or_result_evidence"),
  (r"我用|我做|亲测|亲历|复盘|经验","firsthand_record"),
  (r"客户|老板|高手|专家|权威|团队都|大家都","authority_or_relationship_evidence"),
  (r"对比|测评|vs|更适合|更好","comparable_basis"),
  (r"年份|最新|趋势|热点|越来越|未来","dated_primary_source")]:
  if re.search(pattern,text,re.I):needs.add(requirement)
 if re.search(r"保证|一定|必看|必备|都在|最|千万|闭眼|直接照|就能|立刻|轻松|错过|吃亏|起跑线",text):
  risks.append("absolute_or_pressure_framing")
 if re.search(r"不知道|隐藏|秘密|内幕",text):risks.append("unsupported_information_gap")
 if re.search(r"老板|客户|高手|权威",text):risks.append("unsupported_authority")
 return {"schema_version":"1.0.0","classification_status":"EDITORIAL_RULE_DERIVED",
  "classification_basis":"category+literal text; rules in tools/classify_candidates.py",
  "platforms":{x:"UNKNOWN" for x in "ABC"},
  "surfaces":{x:"REVIEW_REQUIRED" for x in ["cover_main_title","cover_subtitle","platform_title"]},
  "industry_scope":["AI_EDUCATION","AI_SERVICES"] if "AI" in text else ["GENERAL_TEMPLATE"],
  "motives":sorted({v for k,v in MOTIVES.items() if k in category}) or ["UNCLASSIFIED"],
  "evidence_prerequisites":sorted(needs),"risk_flags":risks,"rewrite_required":bool(risks),
  "instantiated_claims_status":"NOT_REVIEWED","calibration":"NOT_RUN","checked_on":"2026-11-14"}
def main():
 counts={}
 for path,key in [("titles/candidates.json",None),("hooks/candidates.json","items")]:
  p=ROOT/path;data=json.loads(p.read_text());rows=data[key] if key else data
  for row in rows:row["applicability"]=classify(row)
  p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n");counts[path]=len(rows)
 print(json.dumps(counts))
if __name__=="__main__":main()
