#!/usr/bin/env node
// Deterministic editorial score aggregation and claim-evidence gate. Not a CTR predictor.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const here=path.dirname(fileURLToPath(import.meta.url));
const rubric=JSON.parse(fs.readFileSync(path.join(here,"../config/title-rubric.json"),"utf8"));
function gate(claims=[],hardGates=[]){
  const failed=claims.filter(c=>c.status==="UNSUPPORTED");
  const unknown=claims.filter(c=>c.status==="UNKNOWN");
  const failedGates=hardGates.filter(g=>g.status==="FAIL"||g.status==="BLOCKED");
  const unknownGates=hardGates.filter(g=>["UNKNOWN","NOT_RUN"].includes(g.status));
  if(failed.length||failedGates.length)return {status:"FAIL",failed_claims:failed.length,failed_gates:failedGates.map(g=>g.id)};
  if(unknown.length||unknownGates.length)return {status:"UNKNOWN",unknown_claims:unknown.length,unknown_gates:unknownGates.map(g=>g.id)};
  return {status:"PASS",failed_claims:0,unknown_claims:0};
}
function aggregate(dimensions={}){
  const ids=rubric.dimensions.map(d=>d.id);
  const missing=ids.filter(id=>{const d=dimensions[id];return !d||!Number.isInteger(d.score)||d.score<0||d.score>4||!Array.isArray(d.evidence)||d.evidence.length===0||!d.reason;});
  if(missing.length)return {aggregate:null,status:"UNRATED",missing_dimensions:missing,not_a_ctr_probability:true};
  const sum=ids.reduce((n,id)=>n+dimensions[id].score,0);
  return {aggregate:Math.round(sum/(ids.length*4)*10000)/100,status:"TRIAL_RANKED",missing_dimensions:[],not_a_ctr_probability:true};
}
function evaluate(input){
  const hardGate=gate(input.claims||[],input.hard_gates||[]);
  const score=aggregate(input.editorial_score?.dimensions||{});
  return {hard_gate:hardGate,editorial_score:score,release_eligible:hardGate.status==="PASS"&&score.status!=="UNRATED",
    note:"Editorial score is for comparative review only; it is not CTR, reach, conversion or viral probability."};
}
function selfTest(){
  const cases=fs.readFileSync(path.join(here,"../evals/title-gold-cases.jsonl"),"utf8").trim().split(/\r?\n/).map(JSON.parse);
  const failures=[];
  for(const c of cases){const got=gate(c.claims,c.hard_gates).status;if(got!==c.expected_gate)failures.push({id:c.case_id,expected:c.expected_gate,actual:got});}
  const complete=Object.fromEntries(rubric.dimensions.map(d=>[d.id,{score:3,evidence:["fixture-evidence"],reason:"fixture",confidence:"medium"}]));
  const scored=aggregate(complete);
  if(scored.status!=="TRIAL_RANKED"||scored.aggregate!==75)failures.push({id:"aggregate",expected:75,actual:scored.aggregate});
  const unrated=aggregate({});
  if(unrated.status!=="UNRATED"||unrated.aggregate!==null)failures.push({id:"unrated",expected:"UNRATED",actual:unrated.status});
  if(failures.length){console.error(JSON.stringify({status:"FAIL",failures},null,2));process.exit(1);}
  console.log("PASS title-core self-test: "+cases.length+" synthetic gate cases + 2 scoring cases");
}
if(process.argv.includes("--self-test"))selfTest();
else{let raw="";for await(const chunk of process.stdin)raw+=chunk;console.log(JSON.stringify(evaluate(JSON.parse(raw)),null,2));}
