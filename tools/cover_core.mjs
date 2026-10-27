import {validateSpec, validatePlan, compilePrompt, validateDelivery, VERSION} from './core.mjs';
if(typeof process!=='undefined'&&process.argv?.[1]&&import.meta.url.startsWith('file:')){
  const {pathToFileURL}=await import('node:url');
  if(import.meta.url===pathToFileURL(process.argv[1]).href){
    try{
      const fs=await import('node:fs/promises');const op=process.argv[2],idx=process.argv.indexOf('--input');
      let value;
      if(op==='capabilities'){
        const readConfig=async name=>{
          for(const relative of ['../assets/','../config/']){
            try{return JSON.parse(await fs.readFile(new URL(relative+name,import.meta.url),'utf8'));}
            catch(e){if(e.code!=='ENOENT')throw e;}
          }
          throw new Error('缺少配置：'+name);
        };
        const locator=await readConfig('knowledge-locator.json');
        const status=await readConfig('integration-status.json');
        value={version:VERSION,scope:'saved_configuration_not_live_probe',core:true,
          github_knowledge:{status:locator.status,repository:locator.repository,visibility:locator.visibility,manifest_ref:locator.manifest_ref,manifest_sha256:locator.manifest_sha256,last_check:locator.last_check},
          semantic_review:status.semantic_review,cover_mcp:status.cover_mcp,
          external_decision_services:status.external_decision_services,
          image_tool:status.image_tool,noterx:status.noterx};
      }
      else{
        if(idx<0||!process.argv[idx+1])throw new Error('需--input JSON路径');
        const d=JSON.parse(await fs.readFile(process.argv[idx+1],'utf8'));
        value=op==='validate'?(d.concepts?validatePlan(d):validateSpec(d)):op==='compile'?{prompt:compilePrompt(d)}:op==='delivery'?validateDelivery(d):null;
        if(!value)throw new Error('操作必须为validate/compile/delivery/capabilities');
      }
      console.log(JSON.stringify(value,null,2));if(value.ok===false)process.exitCode=2;
    }catch(e){console.log(JSON.stringify({ok:false,error:e.message,code:e.code??'INPUT_ERROR',details:e.details}));process.exitCode=2;}
  }
}
