import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {validateDelivery, VERSION} from '../core.mjs';

// Synthetic records test validation rules only; they are not image acceptance evidence.
const record=()=>({requested_count:1,images:[{file:'synthetic-test.png',width:1536,height:2048,actual_model:'not_exposed',checks:Object.fromEntries(['text','visual','factual','reference_fidelity','crop'].map(k=>[k,{status:'passed',evidence:'synthetic validator fixture'}]))}]});

test('model identity is optional by default',()=>assert.equal(validateDelivery(record()).ok,true));
test('an explicitly requested model still requires matching identity',()=>{
  const d=record();d.exact_model_required=true;d.expected_model='user-requested-model';
  assert.equal(validateDelivery(d).ok,false);
  d.images[0].actual_model=d.expected_model;
  assert.equal(validateDelivery(d).ok,true);
});
test('relaxing model identity keeps evidence and image-count gates',()=>{
  const d=record();delete d.images[0].checks.factual.evidence;
  assert.equal(validateDelivery(d).ok,false);
  assert.equal(validateDelivery({images:[]}).ok,false);
});
test('capabilities read persisted activation instead of hardcoded pending flags',()=>{
  const root=new URL('../../',import.meta.url);
  const folder=fs.existsSync(new URL('assets/knowledge-locator.json',root))?'assets/':'config/';
  const locator=JSON.parse(fs.readFileSync(new URL(folder+'knowledge-locator.json',root),'utf8'));
  const cli=fileURLToPath(new URL('../cover_core.mjs',import.meta.url));
  const caps=JSON.parse(execFileSync(process.execPath,[cli,'capabilities'],{encoding:'utf8'}));
  assert.equal(caps.version,VERSION);
  assert.equal(caps.github_knowledge.status,'active');
  assert.equal(caps.github_knowledge.manifest_ref,locator.manifest_ref);
  assert.match(caps.github_knowledge.manifest_ref,/^[a-f0-9]{40}$/);
  assert.match(caps.github_knowledge.manifest_sha256,/^[a-f0-9]{64}$/);
  assert.equal(caps.image_tool.exact_model_required,false);
  assert.equal(caps.external_decision_services,'removed_from_default_workflow');
  assert.equal(caps.cover_mcp,'not_required_use_bundled_scripts');
});
