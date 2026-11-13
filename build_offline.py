from pathlib import Path
from lxml import html,etree
import re,json,base64

ROOT=Path(__file__).resolve().parent
P=ROOT/'project'
ST=P/'public/studio'
MODULES=[('case','case-v5.mjs',{}),('text','text-engine.mjs',{'case-v5.mjs':'case'}),('engine','engine.mjs',{'text-engine.mjs':'text'}),('zip','zip.mjs',{}),('app','app.mjs',{'text-engine.mjs':'text','engine.mjs':'engine','zip.mjs':'zip'})]
chunks=[]
for name,path,deps in MODULES:
 code=(ST/path).read_text()
 def imports(m):return 'const {'+m[1]+'}=__scs_'+deps[m[2]]+';'
 code=re.sub(r"import\s*\{([^}]+)\}\s*from\s*'\./([^']+)';",imports,code)
 exports=re.findall(r'export\s+(?:async\s+)?(?:function|const|let)\s+(\w+)',code)
 code=re.sub(r'\bexport\s+','',code)
 if name=='app':chunks.append('(()=>{\n'+code+'\n})();')
 else:chunks.append('const __scs_'+name+'=(()=>{\n'+code+'\nreturn {'+','.join(exports)+'};\n})();')
bundle='\n'.join(chunks)
(ROOT/'offline-bundle.js').write_text(bundle)
data={}
for p in (ST/'data').glob('*.json'):data['data/'+p.name]=json.loads(p.read_text())
data['fonts/index.json']=json.loads((ST/'fonts/index.json').read_text())
assets={}
for p in (ST/'previews/thumbs').glob('*.jpg'):assets['previews/thumbs/'+p.name]='data:image/jpeg;base64,'+base64.b64encode(p.read_bytes()).decode()
doc=html.fromstring((ST/'index.html').read_text())
for el in doc.xpath('//link[@rel="stylesheet"]|//script[@src]'):el.getparent().remove(el)
style=etree.SubElement(doc.xpath('//head')[0],'style')
css=(ST/'studio.css').read_text()
css=re.sub(r'@font-face\{[^}]+\}','',css)
style.text=css
def script(data,id=None,type=None):
 el=etree.SubElement(doc.xpath('//body')[0],'script')
 if id:el.set('id',id)
 if type:el.set('type',type)
 el.text=data
script(json.dumps({'data':data,'assets':assets},ensure_ascii=False,separators=(',',':')).replace('<','\\u003c'),'scs-offline-data','application/json')
script('null','scs-reopen-project','application/json')
bootstrap='''
window.SCS_OFFLINE=true;window.SCS_LIGHT_MODE=true;
const packageData=JSON.parse(document.getElementById('scs-offline-data').textContent);
window.SCS_ASSET_URLS=packageData.assets;
window.SCS_REOPEN_STATE=JSON.parse(document.getElementById('scs-reopen-project').textContent);
const originalFetch=window.fetch.bind(window);
window.fetch=async function(input,options){
 let path=typeof input==='string'?input:input.url;
 if(path==='/api/capabilities')return Response.json({status:'success',image:false,text:false,vision:false,storage:false,localComposition:true,exactTypography:true,version:'5.0.3-rebuilt',note:'离线预览；未连接图片模型'});
 if(path.startsWith('/api/'))return Response.json({status:'error',code:'OFFLINE_PREVIEW',message:'离线HTML不调用后端；请运行完整项目并配置实际接口。'},{status:503});
 if(path.startsWith('/studio/'))path=path.slice(8);
 if(Object.hasOwn(packageData.data,path))return Response.json(packageData.data[path]);
 if(Object.hasOwn(packageData.assets,path))return originalFetch(packageData.assets[path]);
 return originalFetch(input,options);
};
'''
script(bootstrap+bundle.replace('</script','<\\/script'))
out='<!doctype html>\n'+html.tostring(doc,encoding='unicode',method='html')
(ROOT/'START.html').write_text(out)
assert len(assets)==18
assert not doc.xpath('//script[@src]')
ids=doc.xpath('//*[@id]/@id');assert len(ids)==len(set(ids))
print('Built self-contained core HTML; 18 embedded thumbnails; original full previews resolve inside the complete ZIP')
