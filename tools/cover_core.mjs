import {validateSpec, validatePlan, compilePrompt, validateDelivery, VERSION} from './core.mjs';
if(typeof process!=='undefined'&&process.argv?.[1]&&import.meta.url.startsWith('file:')){
  const {pathToFileURL}=await import('node:url');
  if(import.meta.url===pathToFileURL(process.argv[1]).href){
    try{
      const fs=await import('node:fs/promises');const op=process.argv[2],idx=process.argv.indexOf('--input');
      let value;
      if(op==='capabilities')value={version:VERSION,core:true,github_private_kb:'pending_access',laya:'not_configured',jev:'not_configured',exact_gpt_image_2_5:'not_verified'};
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
