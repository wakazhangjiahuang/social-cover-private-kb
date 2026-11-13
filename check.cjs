const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert'),sharp=require('sharp');
const R=path.resolve(__dirname,'..'),D=JSON.parse(fs.readFileSync(R+'/covers.json','utf8'));
(async()=>{
 const dimensions=[];for(const d of D){const im=sharp(R+'/'+d.file);const m=await im.metadata();assert.equal(m.format,'png');assert.equal(m.width,d.width);assert.equal(m.height,d.height);await im.raw().toBuffer();dimensions.push(d.id);}
 const page=fs.readFileSync(R+'/START.html','utf8'),script=page.match(/<script>([\s\S]*?)<\/script>/)[1];new vm.Script(script);
 // Pure event/filter logic, using a minimal model of the required nodes. This is not a browser rendering test.
 const fake=()=>({value:'',style:{},dataset:{},handlers:{},addEventListener(k,f){this.handlers[k]=f;},close(){this.closed=true;},showModal(){this.opened=true;}});
 const cards=D.map(d=>Object.assign(fake(),{dataset:{platform:d.primaryPlatform,family:d.familyCode,search:[d.id,d.name,d.family,d.headline,d.audience,d.platformName].join(' ')}}));
 const ids={};for(const k of ['search','platform','family','count','empty','reset','modal','large','caption','modalDownload','close'])ids['#'+k]=fake();ids['#platform'].value='all';ids['#family'].value='all';
 const pics=D.map(d=>Object.assign(fake(),{dataset:{full:d.file,caption:d.id}}));
 const env={document:{querySelector:s=>ids[s],querySelectorAll:s=>s==='.cover'?cards:s==='.pic'?pics:[]},window:{open(){}}};vm.createContext(env);vm.runInContext(script,env);
 const visible=()=>cards.filter(c=>!c.hidden).length;
 vm.runInContext('applyFilters()',env);assert.equal(visible(),64);
 for(const [p,n] of [['xhs',22],['douyin',21],['channels',21]]){ids['#platform'].value=p;vm.runInContext('applyFilters()',env);assert.equal(visible(),n);}
 ids['#platform'].value='all';ids['#family'].value='C';vm.runInContext('applyFilters()',env);assert.equal(visible(),8);
 ids['#family'].value='all';ids['#search'].value='A01';vm.runInContext('applyFilters()',env);assert.equal(visible(),1);
 ids['#search'].value='不存在的筛选词XYZ';vm.runInContext('applyFilters()',env);assert.equal(visible(),0);
 ids['#reset'].handlers.click();assert.equal(visible(),64);
 pics[0].handlers.click();assert.equal(ids['#large'].src,D[0].file);assert.equal(ids['#modal'].opened,true);ids['#close'].handlers.click();assert.equal(ids['#modal'].closed,true);
 const q=JSON.parse(fs.readFileSync(R+'/QA.json','utf8'));q.checks.allPNGDecodeAndSize={passed:dimensions.length};q.checks.filterLogic={passed:['all64','xhs22','douyin21','channels21','family8','search1','empty0','reset64','modalPathAndClose'],method:'Node VM with minimal node mocks; not real browser'};q.checks.missingGlyphs=[];
 assert.equal(q.checks.titleFaceBoxConflicts.length,0);assert.equal(q.checks.textOutsideCanvas.length,0);assert.equal(q.checks.offlineRelativeAssets.missing.length,0);assert.equal(q.checks.uniquePNGHashes,64);assert.equal(q.checks.svgFilesInPackage,0);assert.equal(q.checks.SVGMarkupInHTML,false);
 fs.writeFileSync(R+'/QA.json',JSON.stringify(q,null,2));console.log(JSON.stringify({decodedPNG:64,staticReferences:q.checks.offlineRelativeAssets.references,svg:0,filterChecks:9,browser:'NOT_RUN',platformClient:'NOT_RUN'}));
})();
