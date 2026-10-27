import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {validateDelivery, compilePrompt, COMPONENT_IDS, VERSION} from '../core.mjs';

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
test('text evidence is not presented as an image attachment',()=>{
  const s={id:'text-case',mode:'A',topic:'询价邮件转报价草稿',audience:'小企业销售',promise:'演示提取字段和人工复核',headline:'报价草稿怎么做',visual_route:'diagram',
    modules:COMPONENT_IDS.map(id=>({id,status:'apply',decision:'文字素材演示',params:{instruction:'流程示意，不虚构实拍截图'},qa:['与文字来源一致']})),
    evidence_refs:[{id:'brief',kind:'text',source:'用户本轮文字需求',role:'事实来源'}],
    elements:[{id:'flow',role:'流程示意',reference_id:'brief',bbox:[100,300,800,400],z_order:1}]};
  const prompt=compilePrompt(s);
  assert.ok(prompt.includes('仅图像类引用须实际传入对应图片'));
  assert.ok(prompt.includes('文字/文档来源按其实际类型提供'));
  assert.ok(!prompt.includes('真实参考及角色（须实际传入对应图片）'));
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
