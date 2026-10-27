export const VERSION = '1.2.0';
export const COMPONENT_IDS = Array.from({length:18},(_,i)=>`C${String(i+1).padStart(2,'0')}`);
const object = x => x && typeof x === 'object' && !Array.isArray(x);
const nonempty = x => typeof x === 'string' && x.trim().length > 0;
const modes = new Set(['A','B','C']);
const routes = new Set(['person','product','artwork','ui','diagram','typography','scene']);
const empty = x => x == null || x === '' || x === '待定' || x === '由模型决定' || x === '任选';

export function validateSpec(s) {
  const errors=[], warnings=[];
  const fail=(code,path,message)=>errors.push({code,path,message});
  if(!object(s)) return {ok:false,scope:'structure_only',errors:[{code:'SPEC_TYPE',path:'$',message:'单案必须为对象'}],warnings};
  for(const k of ['id','topic','audience','promise']) if(!nonempty(s[k]))fail('REQUIRED',k,'缺少明确内容');
  if(!modes.has(s.mode))fail('MODE','mode','必须为A抖音、B视频号或C小红书');
  if(!routes.has(s.visual_route))fail('ROUTE','visual_route','主视觉路线无效');
  if(typeof s.headline!=='string')fail('HEADLINE','headline','标题必须为字符串；无字封面用空字符串');
  const modules=Array.isArray(s.modules)?s.modules:[];
  if(modules.length!==18)fail('MODULE_COUNT','modules','必须覆盖18模块，省略项也需决策记录');
  const seen=new Set();
  for(const [i,m] of modules.entries()) {
    const path=`modules[${i}]`;
    if(!object(m)){fail('MODULE_TYPE',path,'模块必须为对象');continue;}
    if(!COMPONENT_IDS.includes(m.id))fail('MODULE_ID',path+'.id','未知模块');
    if(seen.has(m.id))fail('MODULE_DUPLICATE',path+'.id','模块重复');
    seen.add(m.id);
    if(!['apply','omit'].includes(m.status))fail('MODULE_STATUS',path+'.status','状态必须为apply或omit');
    if(!nonempty(m.decision))fail('DECISION',path+'.decision','必须有具体决定或省略理由');
    if(!object(m.params))fail('PARAMS',path+'.params','参数必须为对象');
    if(m.status==='apply'&&object(m.params)&&Object.keys(m.params).length===0)fail('EMPTY_PARAMS',path+'.params','启用模块需具体参数');
    if(!Array.isArray(m.qa)||m.status==='apply'&&m.qa.length===0)fail('QA',path+'.qa','启用模块需验收条件');
    if(m.status==='apply'&&object(m.params))for(const [k,v] of Object.entries(m.params))if(empty(v))fail('PLACEHOLDER',path+'.params.'+k,'不能保留空值或待定');
  }
  for(const id of COMPONENT_IDS)if(!seen.has(id))fail('MODULE_MISSING','modules',id+'缺失');
  const mod=id=>modules.find(m=>m?.id===id);
  for(const id of ['C01','C06','C10','C11','C12','C13','C14','C17','C18'])if(mod(id)&&mod(id).status!=='apply')fail('CORE_OMITTED','modules.'+id,'全局生产决定不能省略');
  if(s.visual_route==='person'&&mod('C07')?.status!=='apply')fail('PERSON_MODULE','modules.C07','人物路线需人物规格');
  if(['product','artwork','ui'].includes(s.visual_route)&&mod('C08')?.status!=='apply')fail('MATERIAL_MODULE','modules.C08','素材路线需保真规格');
  if(nonempty(s.headline))for(const id of ['C02','C03','C04'])if(mod(id)?.status!=='apply')fail('TEXT_MODULE','modules.'+id,'有字封面需文字规格');
  if(s.headline===''&&['C02','C03','C04'].some(id=>mod(id)?.status==='apply'))warnings.push('无主标题，核对文字模块是否仅供必要辅助文案。');
  const refs=Array.isArray(s.evidence_refs)?s.evidence_refs:[];
  if(!Array.isArray(s.evidence_refs))fail('REFS','evidence_refs','必须为数组，可为空');
  const refIds=new Set();
  for(const [i,r] of refs.entries()) {
    if(!object(r)||!nonempty(r.id)||!nonempty(r.source)||!nonempty(r.role)){fail('REF_FIELDS',`evidence_refs[${i}]`,'需id/source/role');continue;}
    if(refIds.has(r.id))fail('REF_DUPLICATE',`evidence_refs[${i}].id`,'引用ID重复');
    refIds.add(r.id);
  }
  const elements=Array.isArray(s.elements)?s.elements:[];
  if(!Array.isArray(s.elements)||elements.length===0)fail('ELEMENTS','elements','至少有一个可见元素');
  const ids=new Set();
  for(const [i,x] of elements.entries()) {
    const p=`elements[${i}]`;
    if(!object(x)){fail('ELEMENT_TYPE',p,'元素必须为对象');continue;}
    if(!nonempty(x.id)||ids.has(x.id))fail('ELEMENT_ID',p+'.id','元素ID为空或重复');
    ids.add(x.id);
    if(!nonempty(x.role))fail('ELEMENT_ROLE',p+'.role','元素需职责');
    if(x.reference_id!=null&&!refIds.has(x.reference_id))fail('REF_MISSING',p+'.reference_id','引用不存在');
    const b=x.bbox;
    if(!Array.isArray(b)||b.length!==4||!b.every(Number.isFinite))fail('BBOX',p+'.bbox','需4个有限数值');
    else {const [a,c,w,h]=b;if(a<0||c<0||w<=0||h<=0||a+w>1000||c+h>1000)fail('BOUNDS',p+'.bbox','坐标或大小越界');}
    if(!Number.isFinite(x.z_order))fail('Z_ORDER',p+'.z_order','需明确图层顺序');
  }
  const pairs=Array.isArray(s.forbidden_overlap_pairs)?s.forbidden_overlap_pairs:[];
  for(const pair of pairs){
    if(!Array.isArray(pair)||pair.length!==2){fail('OVERLAP_PAIR','forbidden_overlap_pairs','保护对需两个元素ID');continue;}
    const [a,b]=pair;
    const x=elements.find(x=>x.id===a),y=elements.find(x=>x.id===b);
    if(!x||!y){fail('OVERLAP_REF','forbidden_overlap_pairs','保护元素不存在');continue;}
    if(x.bbox?.length!==4||y.bbox?.length!==4)continue;
    const [ax,ay,aw,ah]=x.bbox,[bx,by,bw,bh]=y.bbox;
    if(Math.min(ax+aw,bx+bw)>Math.max(ax,bx)&&Math.min(ay+ah,by+bh)>Math.max(ay,by))fail('PROTECTED_OVERLAP','forbidden_overlap_pairs',a+'与'+b+'保护区重叠');
  }
  warnings.push('仅检查结构、引用和给定几何；事实、审美、真实型号与成品仍需独立验收。');
  return {ok:errors.length===0,scope:'structure_only',errors,warnings};
}

export function validatePlan(plan){
  if(!object(plan)||!Array.isArray(plan.concepts))return {ok:false,scope:'structure_only',errors:[{code:'PLAN',message:'需concepts数组'}]};
  const requested=Number.isInteger(plan.requested_count)&&plan.requested_count>0?plan.requested_count:3;
  const expected=plan.requested_count?Math.max(requested,plan.planned_count??requested*2):6;
  const results=plan.concepts.map(s=>({id:s?.id,...validateSpec(s)}));
  const errors=[];
  if(plan.concepts.length!==expected)errors.push({code:'CONCEPT_COUNT',message:`预期${expected}案`});
  const ids=plan.concepts.map(s=>s.id);
  if(new Set(ids).size!==ids.length)errors.push({code:'CONCEPT_DUPLICATE',message:'方案ID重复'});
  if(!modes.has(plan.mode)||plan.concepts.some(s=>s.mode!==plan.mode))errors.push({code:'MODE_MISMATCH',message:'计划与方案平台不一致'});
  const selected=plan.selected_ids??[];
  if(!Array.isArray(selected))errors.push({code:'SELECTION_TYPE',message:'selected_ids必须数组'});
  else if(selected.length){
    if(selected.length!==requested||new Set(selected).size!==selected.length||selected.some(id=>!ids.includes(id)))errors.push({code:'SELECTION',message:'选择数量/ID无效'});
    if(!nonempty(plan.selection_reason))errors.push({code:'SELECTION_REASON',message:'需取舍依据'});
    if(results.some(r=>selected.includes(r.id)&&!r.ok))errors.push({code:'INVALID_SELECTED',message:'不能选择结构失败方案'});
  }
  return {ok:errors.length===0&&results.every(r=>r.ok),scope:'structure_only',errors,results,selected_ids:selected,semantic_review_required:true,visual_review_required:true};
}

export function compilePrompt(s){
  const result=validateSpec(s);if(!result.ok){const err=new Error('规格未通过结构检查');err.code='INVALID_SPEC';err.details=result;throw err;}
  const mode={A:'抖音',B:'微信视频号',C:'小红书'}[s.mode];
  return ['创作一张独立的'+mode+'封面，不合并多案。','主题：'+s.topic,'受众：'+s.audience,'内容承诺：'+s.promise,
    '主标题逐字：'+JSON.stringify(s.headline),'副标题逐字：'+JSON.stringify(s.subheadline??''),'主视觉路线：'+s.visual_route,
    s.evidence_refs.length?'真实材料引用及角色（仅图像类引用须实际传入对应图片；文字/文档来源按其实际类型提供，不冒充图像）：'+JSON.stringify(s.evidence_refs):'没有提供图像参考：依据文字材料创作，不虚构实拍、截图、数据或人物身份。',
    ...s.modules.map(m=>`${m.id} ${m.status==='omit'?'不使用':'执行'}：${m.decision}${m.status==='apply'?'；参数：'+JSON.stringify(m.params):''}`),
    '空间元素：'+JSON.stringify(s.elements),'配色职责：'+JSON.stringify(s.palette??{}),'画法与保真：'+JSON.stringify(s.rendering??{}),
    '锁定项：'+JSON.stringify(s.constraints??[]),'各空间坐标是归一化布局目标，最终以清楚阅读、主体保真和保护区为准。',
    '精确渲染所列文案，不改写数字、单位、品牌和否定词；没有列出的Logo/账号/认证/额外文字不要添加。',
    '这是创作规格；生成后逐图看图、核字与裁切验收，不把本提示词的参数当作成品实测。'].join('\n\n');
}

export function validateDelivery(d){
  const errors=[];const expected=Number.isInteger(d?.requested_count)?d.requested_count:3;
  if(!Array.isArray(d?.images)||d.images.length!==expected)errors.push('独立图片数量不符');
  const ids=new Set();
  for(const x of d?.images??[]){
    if(!object(x)||!nonempty(x.file)||ids.has(x.file))errors.push('文件为空或重复');ids.add(x?.file);
    if(!(x.width>0&&x.height>0))errors.push('缺实际像素');
    for(const k of ['text','visual','factual','reference_fidelity','crop'])if(x?.checks?.[k]?.status!=='passed'||!nonempty(x.checks[k].evidence))errors.push(`${x?.file??'?'}:${k}未有通过证据`);
    if(d.exact_model_required===true){
      const actual=x?.actual_model??'';
      const matches=nonempty(d.expected_model)?actual===d.expected_model:/^gpt-image-2\.5-(sunburst|flare)(-\d{4}-\d{2}-\d{2})?$/.test(actual);
      if(!matches)errors.push('用户要求的精确型号未确认');
    }
  }
  return {ok:errors.length===0,scope:'delivery_record_only',errors,warning:'记录通过不认证其真实性；还须实际看图/核文件和检查证据。'};
}

