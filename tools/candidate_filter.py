"""Scoped candidate filtering; unknown platform suitability is never certified."""
def select(rows,*,id=None,query=None,platform=None,surface=None,industry=None,motive=None,evidence=None,include_unverified=False,limit=6):
 found=[];excluded={"scope_unknown":0,"industry":0,"motive":0,"missing_evidence":0,"rewrite_required":0}
 supplied=set(evidence or [])
 scoped=any([platform,surface,industry,motive,evidence is not None])
 for row in rows:
  if id and row["id"]!=id:continue
  hay=" ".join(str(row.get(k,"")) for k in ("id","text","category")).casefold()
  if not all(t.casefold() in hay for t in (query or "").split()):continue
  a=row.get("applicability",{})
  if industry and industry not in a.get("industry_scope",[]) and "GENERAL_TEMPLATE" not in a.get("industry_scope",[]):
   excluded["industry"]+=1;continue
  if motive and motive not in a.get("motives",[]):excluded["motive"]+=1;continue
  unverified=(platform and a.get("platforms",{}).get(platform)!="VERIFIED") or (surface and a.get("surfaces",{}).get(surface)!="VERIFIED")
  if unverified and not include_unverified:excluded["scope_unknown"]+=1;continue
  if scoped and a.get("rewrite_required") and not include_unverified:excluded["rewrite_required"]+=1;continue
  if evidence is not None and not set(a.get("evidence_prerequisites",[]))<=supplied:
   excluded["missing_evidence"]+=1;continue
  found.append(dict(row,selection_status="REQUIRES_TASK_REVIEW",platform_certified=False))
 return {"status":"MATCH" if found else "NO_MATCH","total":len(found),"records":found[:limit],
         "excluded":excluded,"scope":"editorial templates only; verify instantiated claims, field limits and current platform rules",
         "unverified_candidates_explicitly_allowed":include_unverified}
