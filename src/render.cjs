const fs=require('fs'),path=require('path');
const {createCanvas,loadImage,GlobalFonts}=require('@napi-rs/canvas');
const sharp=require('sharp');
const ROOT=path.resolve(__dirname,'..');
const data=JSON.parse(fs.readFileSync(path.join(ROOT,'covers.json'),'utf8'));
for(const f of ['sans','sansBold','serif','serifBold','mono'])GlobalFonts.registerFromPath(path.join(ROOT,'fonts',f+'.otf'),f);
const palettes=[['#F5EFE3','#242522','#DF4E2E','#E7CD53'],['#E8EAD8','#26362D','#526748','#F2CF58'],['#EDE8E3','#2B2C2D','#B63D2D','#D9C5B2'],['#252922','#F3EFDD','#E9CD55','#AB6D51'],['#F2DFDC','#362F2F','#B63D52','#F4D659'],['#DFE2D5','#24372D','#A63E28','#E7D5B8'],['#292526','#F7F0E3','#EAC451','#B76956'],['#F4F0E7','#2D2A27','#A43B2B','#CFD7BC']];
let imgs={},ctx,H,O,rec,pal;
const SY=y=>O+y*1440,SX=x=>x*1080;
function rect(x,y,w,h,c,r=0){ctx.fillStyle=c;ctx.beginPath();if(r)ctx.roundRect(SX(x),SY(y),SX(w),h*1440,r);else ctx.rect(SX(x),SY(y),SX(w),h*1440);ctx.fill();}
function line(x1,y1,x2,y2,c,width=3){ctx.strokeStyle=c;ctx.lineWidth=width;ctx.beginPath();ctx.moveTo(SX(x1),SY(y1));ctx.lineTo(SX(x2),SY(y2));ctx.stroke();}
function txt(t,x,y,w,h,opt={}){let lines=t.split('\n'),font=opt.font||rec.font;let size=opt.size||110;const lh=opt.lh||1.12;
 while(size>18){ctx.font=`${size}px "${font}"`;if(Math.max(...lines.map(z=>ctx.measureText(z).width))<=w*1080&&lines.length*size*lh<=h*1440)break;size--;}
 const total=lines.length*size*lh;let top=SY(y)+(h*1440-total)*(opt.valign==='top'?0:.5);
 ctx.textBaseline='top';ctx.textAlign=opt.align||'left';ctx.lineJoin='round';
 lines.forEach((z,j)=>{const tw=ctx.measureText(z).width,xx=SX(x)+(opt.align==='center'?w*1080/2:opt.align==='right'?w*1080:0),yy=top+j*size*lh;
 if(opt.shadow){ctx.shadowColor='rgba(0,0,0,.25)';ctx.shadowBlur=10;ctx.shadowOffsetY=7;}
 if(opt.stroke){ctx.strokeStyle=opt.stroke;ctx.lineWidth=Math.max(3,size*.055);ctx.strokeText(z,xx,yy);}
 ctx.fillStyle=(Array.isArray(opt.color)?opt.color[j%opt.color.length]:opt.color)||pal[1];ctx.fillText(z,xx,yy);
 ctx.shadowBlur=0;ctx.shadowOffsetY=0;
 if(!opt.decorative)rec.textGeometry.push({text:z,role:opt.role||'title',box:[(xx-(opt.align==='center'?tw/2:opt.align==='right'?tw:0))/1080,yy/H,tw/1080,size/H],font,sizePx:size,color:ctx.fillStyle});
 });return size;
}
function title(x=.08,y=.12,w=.84,h=.23,opt={}){return txt(rec.headline,x,y,w,h,{size:118,color:[pal[1],pal[2]],...opt,role:'title'});}
function sub(t,x=.08,y=.79,w=.84,h=.07,opt={}){return txt(t,x,y,w,h,{size:31,font:'sans',...opt,role:'support'});}
function tag(t,x,y,w=.31,c=pal[2],fg=pal[0]){rect(x,y,w,.045,c,4);txt(t,x+.014,y+.002,w-.028,.041,{size:26,font:'sansBold',color:fg,role:'label'});}
function ellipse(x,y,w,h,c){ctx.fillStyle=c;ctx.beginPath();ctx.ellipse(SX(x+w/2),SY(y+h/2),SX(w/2),h*720,0,0,Math.PI*2);ctx.fill();}
function person(x,y,w,h,asset=rec.asset,opts={}){
 const im=imgs[asset],alpha=Number(asset.slice(5))<=4;let bx=SX(x),by=SY(y),bw=SX(w),bh=h*1440;
 ctx.save();if(opts.round){ctx.beginPath();ctx.roundRect(bx,by,bw,bh,opts.round);ctx.clip();}if(opts.circle){ctx.beginPath();ctx.ellipse(bx+bw/2,by+bh/2,bw/2,bh/2,0,0,Math.PI*2);ctx.clip();}
 let dw,dh,dx,dy;
 if(alpha&&!opts.fill){const s=Math.min(bw/im.width,bh/im.height);dw=im.width*s;dh=im.height*s;dx=bx+(bw-dw)/2;dy=by+bh-dh;ctx.drawImage(im,dx,dy,dw,dh);}
 else{const s=Math.max(bw/im.width,bh/im.height);dw=im.width*s;dh=im.height*s;dx=bx+(bw-dw)/2;dy=by+(bh-dh)/2;ctx.drawImage(im,dx,dy,dw,dh);}
 ctx.restore();
 const faces={photo1:[.45,.075,.34,.285],photo2:[.32,.035,.37,.29],photo3:[.25,.01,.42,.29],photo4:[.32,.045,.40,.28],photo5:[.51,.36,.28,.24],photo6:[.48,.29,.28,.22]};const f=faces[asset];
 rec.subjectGeometry.push({asset,box:[dx/1080,dy/H,dw/1080,dh/H],clipBox:[bx/1080,by/H,bw/1080,bh/H],faceBox:[(dx+f[0]*dw)/1080,(dy+f[1]*dh)/H,f[2]*dw/1080,f[3]*dh/H],kind:alpha?'人物抠图':'环境人像'});
}
function photoBG(asset=rec.asset){const im=imgs[asset];const s=Math.max(1080/im.width,H/im.height);const dx=(1080-im.width*s)/2,dy=(H-im.height*s)/2,dw=im.width*s,dh=im.height*s;ctx.drawImage(im,dx,dy,dw,dh);const f=asset==='photo5'?[.51,.36,.28,.24]:[.48,.29,.28,.22];rec.subjectGeometry.push({asset,box:[dx/1080,dy/H,dw/1080,dh/H],clipBox:[0,0,1,1],faceBox:[(dx+f[0]*dw)/1080,(dy+f[1]*dh)/H,f[2]*dw/1080,f[3]*dh/H],kind:'环境人像'});}
function veil(top=true,dark=true){const g=ctx.createLinearGradient(0,top?0:H,0,top?H*.65:H*.3);g.addColorStop(0,dark?'rgba(15,18,13,.86)':'rgba(247,241,226,.98)');g.addColorStop(1,dark?'rgba(15,18,13,0)':'rgba(247,241,226,0)');ctx.fillStyle=g;ctx.fillRect(0,0,1080,H);}
function card(x,y,w,h,color=pal[0]){ctx.save();ctx.shadowColor='rgba(0,0,0,.12)';ctx.shadowBlur=20;ctx.shadowOffsetY=10;rect(x,y,w,h,color,15);ctx.restore();}
function labelRow(words,x,y,w=.84){const gap=.025,cw=(w-gap*(words.length-1))/words.length;words.forEach((z,j)=>tag(z,x+j*(cw+gap),y,cw));}
function arrow(x,y,w=.12,c=pal[2]){line(x,y,x+w,y,c,7);line(x+w-.025,y-.018,x+w,y,c,7);line(x+w-.025,y+.018,x+w,y,c,7);}
function smallPortrait(x,y,w,h,asset=rec.asset){rect(x,y,w,h,pal[3],14);person(x,y,w,h,asset,{round:14});}
async function run(){for(let j=1;j<=6;j++)imgs['photo'+j]=await loadImage(path.join(ROOT,'assets','photo'+j+'.png'));
for(let i=0;i<data.length;i++){
 rec=data[i];if(process.env.COVER_IDS&&!process.env.COVER_IDS.split(',').includes(rec.id))continue;H=rec.height;O=(H-1440)/2;pal=palettes[(i+Math.floor(i/8))%palettes.length];ctx=createCanvas(1080,H).getContext('2d');ctx.fillStyle=pal[0];ctx.fillRect(0,0,1080,H);rec.textGeometry=[];rec.subjectGeometry=[];
 const [a,b]=rec.headline.split('\n');
 switch(i){
 case 0: tag('口播表达',.08,.045);title(.08,.12,.84,.26);ellipse(.13,.42,.77,.58,pal[3]);person(.08,.34,.84,.62);sub('先说对象，再说本条所得',.08,.87,.78,.05);break;
 case 1: person(0,.00,1,.70,'photo6',{fill:true});rect(0,.66,1,.34,pal[0]);title(.08,.70,.84,.22);break;
 case 2: txt(a,.08,.11,.84,.10,{size:100});person(.12,.24,.76,.65);rect(.055,.77,.89,.14,pal[2]);txt(b,.09,.785,.82,.11,{size:84,color:pal[0]});break;
 case 3: rect(.08,.04,.84,.86,pal[3],30);person(.10,.06,.80,.82);rect(.04,.65,.92,.24,pal[0],12);title(.08,.665,.84,.205);break;
 case 4: ellipse(.14,.16,.72,.61,pal[3]);person(.10,.08,.80,.67);rect(0,.70,1,.30,pal[1]);title(.08,.735,.84,.21,{color:[pal[0],pal[3]]});break;
 case 5: rect(.40,.39,.54,.53,pal[3],30);person(.38,.30,.57,.64);card(.06,.10,.80,.30);title(.09,.12,.74,.25);tag('输入 → 输出 → 验收',.08,.75,.48);break;
 case 6: rect(0,.04,1,.05,pal[2]);txt('SOCIAL COVER / DESIGN',.08,.041,.84,.04,{size:25,font:'mono',color:pal[0],role:'label'});title(.08,.14,.84,.23);person(.08,.38,.84,.57);tag('一主一辅',.08,.78,.29);break;
 case 7: tag('创作方法',.08,.055);title(.08,.18,.66,.23);person(.47,.40,.48,.48);labelRow(['问题','证据','答案'],.08,.84);arrow(.10,.58,.22);sub('一条内容只交付一个核心所得',.08,.68,.52,.09);break;
 case 8: rect(.53,0,.47,1,pal[3]);person(.46,.17,.53,.73);title(.07,.19,.45,.43,{size:107});tag('给谁看？',.07,.68,.34);break;
 case 9: rect(0,0,.48,1,pal[3]);person(.01,.20,.53,.70);title(.54,.19,.40,.42,{size:95});line(.55,.68,.90,.68,pal[2],6);break;
 case 10: ctx.fillStyle=pal[3];ctx.beginPath();ctx.moveTo(0,SY(.75));ctx.lineTo(1080,SY(.40));ctx.lineTo(1080,H);ctx.lineTo(0,H);ctx.fill();title(.08,.11,.84,.25);person(.25,.37,.70,.59);sub('先对照封面承诺，再看正文证据',.08,.76,.44,.13);break;
 case 11: title(.08,.13,.70,.24);arrow(.68,.40,.19);person(.39,.40,.55,.54);tag('先改主次',.08,.68,.35);sub('第一眼 → 第二眼',.08,.80,.55,.05);break;
 case 12: rect(.05,.12,.13,.76,pal[2]);txt('应\n用\n场\n景',.065,.21,.10,.48,{size:70,color:pal[0],align:'center'});person(.15,.35,.48,.58);title(.58,.14,.36,.38,{size:88});break;
 case 13: rect(.06,.09,.86,.05,pal[2]);rect(.06,.09,.045,.79,pal[2]);title(.13,.20,.72,.24);person(.34,.43,.61,.52);sub('标题留白先于人物摆位',.13,.77,.45,.08);break;
 case 14: line(.10,.72,.91,.31,pal[2],11);title(.08,.12,.84,.24);person(.29,.38,.63,.57);tag('先画布局再拍人',.08,.77,.48);break;
 case 15: rect(.08,.13,.40,.63,pal[3]);title(.11,.17,.34,.43,{size:88});person(.54,.31,.40,.60);sub('主标题 / 条件',.11,.68,.31,.06);break;
 case 16: txt(a,.08,.12,.81,.10,{size:103});rect(.07,.28,.13,.57,pal[2]);txt('留\n白',.085,.35,.10,.31,{size:76,color:pal[0],align:'center'});person(.29,.27,.64,.66);txt(b,.24,.78,.68,.10,{size:77,color:pal[1]});break;
 case 17: person(.26,.23,.48,.68);txt('先\n主',.06,.27,.17,.31,{size:81,color:pal[2],align:'center'});txt('后\n辅',.77,.42,.17,.31,{size:81,color:pal[2],align:'center'});title(.08,.09,.84,.15,{size:76});sub('眼口区域保持完整',.08,.87,.84,.04,{align:'center'});break;
 case 18: txt('大字',.045,.12,.91,.19,{size:217,color:pal[3],align:'center',decorative:true});person(.14,.24,.74,.68);rect(.045,.70,.91,.20,pal[0]);title(.08,.71,.84,.17,{size:79});break;
 case 19: txt('层次',.07,.11,.86,.19,{size:212,color:pal[3],align:'center',decorative:true});person(.25,.23,.62,.68);tag('前 / 后',.07,.40,.24);rect(.06,.74,.87,.17,pal[0]);title(.09,.75,.81,.15,{size:75});break;
 case 20: ellipse(.17,.10,.66,.51,pal[3]);person(.17,.10,.66,.51,rec.asset,{circle:true});title(.08,.66,.84,.24,{font:'serifBold'});break;
 case 21: rect(.47,.12,.44,.74,pal[3],220);person(.46,.14,.46,.72);title(.07,.22,.36,.39,{size:90,font:'serifBold'});sub('主次 / 呼吸 / 留白',.08,.74,.36,.09);break;
 case 22: rect(.13,.28,.74,.56,pal[3],20);person(.17,.19,.66,.70);title(.08,.055,.84,.19);tag('头肩伸出框外',.08,.82,.43);break;
 case 23: card(.07,.12,.79,.26);title(.11,.135,.70,.22,{size:96});person(.09,.42,.62,.52);tag('正文直接给出回答',.52,.76,.41);break;
 case 24: title(.08,.17,.84,.29,{font:'serif',size:135});person(.50,.48,.40,.41);line(.08,.66,.40,.66,pal[2],6);sub('简洁不是省略对象',.08,.76,.43,.10);break;
 case 25: txt(a.split('').join('\n'),.09,.14,.18,.66,{size:91,align:'center'});txt(b.split('').join('\n'),.31,.17,.17,.62,{size:72,align:'center'});person(.47,.35,.47,.58);break;
 case 26: [a,b].forEach((z,j)=>{rect(.07+j*.08,.17+j*.13,.79,.12,j?pal[1]:pal[2]);txt(z,.10+j*.08,.185+j*.13,.73,.09,{size:87,color:pal[0]});});person(.36,.48,.57,.44);tag('读序先于装饰',.08,.76,.40);break;
 case 27: txt('？',.07,.15,.35,.36,{size:335,color:pal[3],decorative:true});title(.12,.22,.80,.27,{size:94});person(.45,.50,.47,.42);sub('让问题具体，让答案可找',.08,.77,.39,.11);break;
 case 28: txt(a,.08,.16,.84,.11,{size:74});txt(b,.08,.30,.84,.18,{size:130,color:pal[2]});person(.11,.48,.52,.43);sub('主句要短\n条件放副题',.67,.68,.25,.15);break;
 case 29: rect(.07,.15,.18,.66,pal[2]);rect(.29,.24,.18,.65,pal[1]);txt('别\n堆\n术\n语',.09,.24,.14,.45,{size:75,color:pal[0],align:'center'});txt('说\n成\n具\n体\n动\n作',.31,.27,.14,.55,{size:75,color:pal[0],align:'center'});person(.51,.30,.44,.61);break;
 case 30: txt('谁',.08,.13,.42,.47,{size:431,color:pal[2],font:'sansBold',decorative:true});person(.45,.34,.50,.58);title(.08,.68,.84,.21,{size:83});break;
 case 31: card(.07,.12,.86,.41);title(.11,.16,.77,.23);line(.11,.43,.87,.43,pal[2]);sub('当前状态 / 下一步 / 责任人',.11,.45,.76,.06);person(.32,.52,.59,.40);break;
 case 32: title(.08,.11,.84,.24);ellipse(.29,.42,.43,.44,pal[3]);person(.29,.39,.43,.50);tag('起点',.08,.43,.18);tag('动作',.73,.53,.18);tag('验收',.08,.76,.18);break;
 case 33: title(.08,.11,.84,.25);person(.06,.41,.54,.49);smallPortrait(.62,.46,.30,.29,'photo4');rect(.60,.78,.34,.07,pal[2]);sub('细节 → 作用',.62,.79,.30,.045,{color:pal[0],size:29});break;
 case 34: person(.09,.07,.82,.72);rect(.045,.70,.91,.22,pal[2]);title(.085,.715,.83,.18,{size:84,color:pal[0]});break;
 case 35: card(.06,.10,.88,.34);title(.10,.13,.80,.26);rect(.10,.53,.53,.33,pal[3],8);person(.42,.46,.51,.46);sub('媒介 / 尺寸 / 格式',.13,.57,.38,.12);break;
 case 36: ctx.save();ctx.translate(140,SY(.17));ctx.rotate(-.055);ctx.fillStyle=pal[3];ctx.fillRect(0,0,780,410);ctx.restore();title(.11,.19,.76,.25,{font:'serifBold'});person(.44,.48,.49,.44);txt('观点在画面外',.08,.60,.29,.20,{size:48,font:'serif',role:'support'});break;
 case 37: person(.07,.06,.86,.87);rect(.06,.72,.88,.18,pal[0],8);title(.10,.732,.80,.155,{size:81,font:'serif'});break;
 case 38: photoBG('photo5');veil(true,false);title(.08,.08,.84,.27,{font:'serifBold'});tag('整理输入',.08,.80,.37);break;
 case 39: rect(.04,.10,.35,.80,pal[1],6);txt('验\n收\n标\n准',.085,.27,.26,.40,{size:89,color:pal[0],align:'center'});person(.42,.21,.55,.69);rect(.44,.765,.49,.075,pal[0],6);sub('先定义正确结果',.47,.77,.43,.065,{color:pal[1]});tag('别急着选工具',.44,.12,.49);tag('先写',.085,.15,.26,pal[0],pal[1]);break;
 case 40: title(.08,.10,.84,.24);person(.47,.40,.47,.49);['问题','证据','结论'].forEach((z,j)=>{tag(`${j+1} ${z}`,.08,.43+j*.13,.36);if(j<2)line(.26,.48+j*.13,.26,.54+j*.13,pal[2],6);});break;
 case 41: title(.08,.10,.84,.24);person(.48,.40,.47,.49);['标题正文','主体遮挡','发布预览'].forEach((z,j)=>{txt('0'+(j+1),.08,.44+j*.13,.10,.07,{size:42,color:pal[2],font:'mono',role:'label'});sub(z,.21,.44+j*.13,.27,.07,{size:33});line(.08,.525+j*.13,.46,.525+j*.13,pal[3]);});break;
 case 42: title(.08,.10,.84,.23);rect(.05,.43,.44,.39,pal[3],8);rect(.51,.43,.44,.39,pal[3],8);person(.05,.44,.44,.37,'photo3');person(.51,.44,.44,.37,'photo3');txt('文字靠左',.07,.735,.17,.065,{size:31,color:pal[2],role:'label'});txt('文字靠右',.76,.735,.17,.065,{size:31,color:pal[2],role:'label'});labelRow(['布局示意','非效果对照'],.12,.86,.76);break;
 case 43: title(.08,.10,.84,.23);person(.34,.42,.33,.44);ellipse(.43,.35,.15,.11,pal[2]);txt('问题',.445,.38,.12,.05,{size:32,color:pal[0],align:'center',role:'label'});['依据','条件','边界'].forEach((z,j)=>{const x=[.08,.73,.08][j],y=[.48,.54,.77][j];tag(z,x,y,.20);line(x+.10,y+.045,.50,.43,pal[3],5);});break;
 case 44: title(.08,.10,.84,.25);card(.07,.44,.46,.40);sub('原始出处\n适用范围\n个人判断',.12,.48,.35,.28,{size:43});person(.53,.42,.43,.48);tag('证据核对',.08,.86,.38);break;
 case 45: title(.08,.09,.84,.24);person(.06,.40,.61,.45,'photo5',{round:14});rect(.70,.40,.24,.45,pal[1],10);sub('目标\n操作\n结果',.735,.47,.17,.28,{size:43,color:pal[0]});break;
 case 46: title(.08,.10,.84,.25);ellipse(.16,.43,.57,.43,pal[3]);ellipse(.19,.455,.51,.38,pal[0]);person(.34,.43,.49,.46);tag('目标',.08,.43,.21);tag('变量',.08,.67,.21);tag('复核',.69,.81,.21);break;
 case 47: title(.08,.10,.84,.24);line(.14,.43,.14,.85,pal[2],8);['开场','证据','收尾'].forEach((z,j)=>{ellipse(.115,.44+j*.14,.05,.038,pal[2]);tag(z,.22,.43+j*.14,.28);});person(.55,.43,.40,.46);break;
 case 48: txt('FIELD NOTES',.08,.06,.84,.055,{size:52,font:'serifBold',role:'label'});line(.08,.125,.92,.125,pal[1],2);person(.08,.20,.84,.73);rect(.05,.73,.90,.18,pal[0]);title(.08,.74,.84,.15,{font:'serifBold',size:79});break;
 case 49: rect(.04,.07,.09,.84,pal[2]);txt('工\n作\n台',.052,.24,.065,.38,{size:55,color:pal[0],align:'center',role:'label'});title(.18,.11,.74,.24);person(.20,.38,.73,.55);tag('从已有资料开始',.19,.81,.46);break;
 case 50: txt('工作方法 / 03',.08,.08,.84,.05,{size:31,font:'mono',role:'label'});title(.08,.20,.84,.24,{font:'serifBold'});person(.35,.45,.56,.42);line(.08,.88,.92,.88,pal[1],3);sub('可复用的是结构，需复核的是内容',.08,.91,.84,.045,{size:25});break;
 case 51: txt('“',.08,.10,.26,.16,{size:210,color:pal[2],decorative:true});title(.12,.24,.78,.24,{font:'serif',size:105});person(.58,.55,.35,.33);sub('个人观点\n情境与方法',.12,.67,.36,.15,{size:38});break;
 case 52: rect(.04,.045,.92,.91,pal[2]);rect(.065,.065,.87,.87,pal[0]);title(.12,.13,.76,.24,{font:'serifBold'});person(.18,.41,.64,.47);sub('条件 → 过程 → 结果',.12,.87,.76,.045,{align:'center'});break;
 case 53: person(.04,.05,.92,.56,'photo5',{round:18});rect(.05,.51,.16,.12,pal[2],8);txt('01',.065,.525,.13,.08,{size:72,font:'mono',color:pal[0],align:'center'});title(.09,.65,.82,.24);break;
 case 54: title(.08,.11,.84,.24);person(.20,.39,.61,.53);ctx.save();ctx.translate(SX(.08),SY(.54));ctx.rotate(-.13);ctx.fillStyle=pal[3];ctx.fillRect(0,0,210,74);ctx.fillStyle=pal[1];ctx.font='30px sansBold';ctx.fillText('少量点缀',16,18);ctx.restore();tag('焦点要明确',.62,.77,.31);break;
 case 55: card(.14,.19,.80,.32,pal[3]);card(.06,.12,.80,.32,pal[0]);title(.10,.145,.72,.26);person(.41,.51,.51,.42);sub('主卡 / 副卡',.08,.68,.34,.10);break;
 case 56: photoBG('photo6');veil(true,false);title(.08,.01,.84,.20,{font:'serifBold',size:112});tag('路线 / 天气 / 体力',.08,.78,.49);break;
 case 57: photoBG('photo5');veil(true,false);title(.08,.10,.84,.24,{font:'serif'});line(.08,.38,.70,.38,pal[1],3);break;
 case 58: rect(.51,.05,.44,.88,pal[3],20);person(.51,.05,.44,.88,'photo5',{round:20});title(.07,.23,.39,.37,{font:'serif',size:96});sub('给当前任务\n留一个安静入口',.08,.72,.35,.13);break;
 case 59: photoBG('photo6');veil(true,true);title(.08,.01,.84,.20,{color:['#F8F2E5','#E5D268'],font:'serifBold',size:112});line(.08,.54,.39,.41,'#E5D268',5);break;
 case 60: photoBG('photo5');veil(false,true);title(.08,.76,.84,.13,{size:65,font:'serif',color:'#FFF6E7'});break;
 case 61: title(.08,.13,.84,.27,{font:'serifBold'});person(.05,.48,.90,.35,'photo5',{round:10});sub('对象 / 交付 / 验收',.08,.88,.84,.05);break;
 case 62: title(.08,.11,.84,.25,{font:'serifBold'});person(.04,.48,.92,.44,'photo6',{round:10});tag('开放信息先查清',.08,.84,.43);break;
 case 63: ctx.fillStyle='#20241F';ctx.fillRect(0,0,1080,H);pal=['#20241F','#F5EFE0','#E3CA66','#515947'];ellipse(.25,.38,.65,.53,pal[3]);person(.27,.37,.62,.54);title(.08,.11,.84,.25,{color:[pal[1],pal[2]],font:'serifBold'});sub('干净文字区 / 明确亮暗层级',.08,.83,.79,.05,{color:pal[1]});break;
 }
 // One support line remains readable at full size. A visible label identifies all fictional AI people.
 const dark=pal[0].startsWith('#2');ctx.fillStyle='rgba(247,244,233,.94)';ctx.fillRect(0,H-68,1080,68);ctx.font='25px sans';ctx.fillStyle='#353731';ctx.textBaseline='middle';ctx.textAlign='left';ctx.fillText('AI生成人物 · 排版示例',42,H-34);ctx.textAlign='right';ctx.fillText(rec.id+' / '+rec.platformName,1038,H-34);
 rec.footerGeometry={box:[0,(H-68)/H,1,68/H],role:'AI来源与编号'};
 const png=ctx.canvas.toBuffer('image/png');const dest=path.join(ROOT,rec.file);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.writeFileSync(dest,png);
 fs.mkdirSync(path.join(ROOT,'thumbs'),{recursive:true});await sharp(png).resize({width:270}).jpeg({quality:84}).toFile(path.join(ROOT,rec.thumb));
 rec.renderStats={pngBytes:png.length,titleMinSizePx:Math.min(...rec.textGeometry.filter(t=>t.role==='title').map(t=>t.sizePx)),width:1080,height:H};
 }
 fs.writeFileSync(path.join(ROOT,'covers.json'),JSON.stringify(data,null,2));
 console.log(JSON.stringify({rendered:data.length,totalPngMB:data.reduce((a,r)=>a+r.renderStats.pngBytes,0)/1e6,smallestTitle:Math.min(...data.map(r=>r.renderStats.titleMinSizePx))}));}
run().catch(e=>{console.error(e);process.exit(1)});
