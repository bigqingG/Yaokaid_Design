const regions = [
  { name:'澄曜区', code:'REG_CHENGYAO', type:'现代新能源都市区', accent:'#d86b3f', description:'以新能源产业、职业竞技与商业媒体闻名的现代都市区；城市建设强调能源效率，也必须遵守宜居性与公共环境规则。', element:'火 · 金', places:['雾湖镇','静湖镇','澄湖镇','燃栖城','燃栖城郊带','红谷生态区','红谷','曜心城区','镜幕商环','赤轨新城','曜南竞技公园','市区中心站','澄曜港口','雾湖湿地保护区','静湖保护区','澄湖保护区'] },
  { name:'澜桥区', code:'REG_LANQIAO', type:'江河交通与物流枢纽型综合区', accent:'#3d7182', description:'数百座桥梁、内河码头、仓储走廊和调度中心构成的流动之区；货物、妖怪、卡牌与秘密都在这里不断转手。', element:'水', places:['回澜主埠','百桥旧街','退潮仓廊','河闸调度带','汀泊洲'] },
  { name:'青棠区', code:'REG_QINGTANG', type:'城市森林与老社区共生型综合区', accent:'#5b8560', description:'树冠、旧楼、社区市场和公共庭院交织的生活区；妖怪不是竞技场上的特殊存在，而是家庭、邻里与城市服务的一部分。', element:'木 · 水', places:['棠荫旧社区','青棠林寓带','养枝湖畔区','棠织生态服务园','枝合实验街区'] },
  { name:'砚岭区', code:'REG_YANLING', type:'山地高校与研究机构型综合区', accent:'#667078', description:'山地校园、层岩研究设施、旧道碑刻和严格实验制度共同构成的知识之区；九川许多关于妖怪、元素和幻影克隆的标准都从这里产生。', element:'土 · 金', places:['砚门学城','层岩研究谷','石经旧道','岩坳试训场','归壑镇'] },
  { name:'霜港区', code:'REG_SHUANGANG', type:'北方冷港与重工业型综合区', accent:'#52738c', description:'冷海、重型船坞、装卸巨臂和严格工序共同塑造的工业港区；这里最擅长把妖怪、装备和规则锻造成可以承受极端环境的形态。', element:'水 · 金', places:['北锚主港','寒坞船造带','白汐临海城','冻潮外海群岛','铁汛防务码头'] },
  { name:'沃衡区', code:'REG_WOHENG', type:'中原平原农业型综合区', accent:'#a78343', description:'平原、渠网、合作农场与旧集市共同铺展的丰饶之区；现代农业、水利与食品产业在日常劳作中与妖怪生态彼此交织。', element:'土 · 木', places:['丰埂城','苍原县','水衡渠网','南畴合作农场','谷垄旧集','西垣旱作带'] }
];

const monsters = [
  ['MON_CYS_001','火灶灵','燃栖城郊带','火','一般','源自火山暖岩缝、能把零散热量储进腹囊的小型兽灵；灶房只是它新近适应的人造暖穴。','#ce613e'],
  ['MON_CYS_002','锻金咚','赤轨新城','金','一般','用钟形额冠敲击岩石与矿壳，凭回声寻找盐晶和甲虫的敦实小兽。','#b0803c'],
  ['MON_CYS_003','霓火茧','镜幕商环','火','一般','把光伏遮阳棚下的散射光与设备余热储进半透明茧层、在适宜温度下短暂破茧疾行。','#d86865'],
  ['MON_CYS_004','烬甲魃','燃栖城郊带','火','一般','生活在干燥丘地和能源隔离带，外甲受损后会开放散热裂隙并进入高攻击状态。','#a74e39'],
  ['MON_CYS_005','日巡犬','曜南竞技公园','火','一般','每天沿固定领地路线巡游，静卧日照时能修复肌肉微损伤的犬型兽灵。','#e08b42'],
  ['MON_CYS_006','青铜叶鳅','赤轨新城','金','一般','栖息在城市冷却水道，以叶片状矿化鳍过滤金属微粒的微型鳅类妖怪。','#778b64'],
  ['MON_CYS_008','铁芯蟾','赤轨新城','金','罕见','皮膜会随温湿度改变导热与储液结构，在三种稳定形态间切换的城市两栖妖怪。','#647d70'],
  ['MON_CYS_009','曜金拉恩','曜心城区','金','稀有','能感知火元素反应产生的瞬时热差，并用矿化棱冠把热差转成定向电火花。','#c99e42'],
  ['MON_CYS_010','账眼鸮','镜幕商环','金','稀有','把连续出现的物品位置编码进多层眼睑纹路，擅长从杂乱库存中找出目标。','#7e7054'],
  ['MON_CYS_011','焰舞沙魈','燃栖城郊带','火','稀有','会在同伴受伤或天敌逼近时踩出高速环形步伐，用地表热浪制造错位轮廓。','#d04e3f'],
  ['MON_CYS_012','搏命熊','曜南竞技公园','火','稀有','能把体脂在短时间内转成强劲冲锋热量，但每次全力攻击都会加重搭档照护压力。','#9d4535'],
  ['MON_CYS_013','裂炉吼','燃栖城郊带','火','罕见','胸腔能吸收冲击并压缩热气，受扰后以越来越强的低频吼声划定领地。','#853c31'],
  ['MON_CYS_014','金羽戴胜','曜心城区','金','稀有','在高层建筑缝隙筑巢，冠羽能沉积轻质矿物并在受袭时整束脱落反击。','#c3984d'],
  ['MON_CYS_015','禁火魇','燃栖城郊带','火','罕见','会吞入不稳定火元素并把惰性灰膜覆盖到失控生物表面，以吃火而非放火生存。','#726154'],
  ['MON_CYS_016','冷阀蜥','赤轨新城','水','一般','生活在高温设施冷却边缘，通过喷出低温黏液软化矿化外壳并舔食盐分。','#5b91a3'],
  ['MON_CYS_018','金乌','曜心城区','火','史诗','沿城市上升热流巡飞，展翼时以大范围热压驱离领空内其他生物的稀有大型逐日鸟。','#c26b31'],
  ['MON_CYS_019','归焰凰','澄曜区跨地方单元','火','传说','在生命和环境能量跌至低谷时进入炭壳休眠，条件恢复后沿旧热流路线返巢。','#b84136'],
  ['MON_CYS_021','逆焰魃','燃栖城郊带','火','稀有','会把干燥环境中的冲击热导回受损组织，在战斗碰撞中反而快速愈合。','#ad5040'],
  ['MON_CYS_022','双面魍','镜幕商环','金','史诗','头部前后各有一组功能不同的感知面，会在攻击与扩大观察范围之间做出选择。','#876e6b'],
  ['MON_LQ_001','涟渡蝌蚪','百桥旧街','水','一般','背部水膜会保存沿途声振，抵岸后以一圈圈涟纹重放旅程的漂流幼生兽灵。','#5594a3','澜桥区'],
  ['MON_LQ_002','鳍皮皮','汀泊洲','水','一般','四肢间生有叶脉状皮鳍，借浪头贴水冲刺并随回卷水流滑回巢滩。','#66a39a','澜桥区'],
  ['MON_LQ_003','金签鳞','河闸调度带','水','一般','洄游时脱落签片状育卵鳞，把后代分散送入不同支流的细长河鱼。','#9c9962','澜桥区'],
  ['MON_LQ_004','锚沉沉','回澜主埠','金','一般','腹部抱着自幼筛选的重石，用蜕下的钩爪把同伴固定在洪流中。','#797d70','澜桥区'],
  ['MON_LQ_005','静景鹤','汀泊洲','水','罕见','静立时把倒影压平成无波水镜，借镜面感知周围离水动静的长脚伏猎鸟。','#7797a0','澜桥区'],
  ['MON_LQ_006','滩头小獭','汀泊洲','水','一般','把失散幼兽、空卵壳和陌生气味暂时收进公共泥窝的滩涂小兽。','#668f7a','澜桥区'],
  ['MON_LQ_007','浪螳螂','河闸调度带','水','罕见','前肢切出回卷薄浪，把猎物拨离原位后占据水流死角的半水生兽灵。','#3f8291','澜桥区'],
  ['MON_LQ_009','心流隼','回澜主埠','水','罕见','松开爪中旧猎物，依据坠落轨迹判断乱流并选择新目标俯冲的隼类。','#597f91','澜桥区'],
  ['MON_LQ_010','桥牙牙','百桥旧街','金','稀有','藏在桥缝中磨亮矿质门齿，从桥体新振动判断猎物方位的穴居兽灵。','#8a7863','澜桥区'],
  ['MON_LQ_011','水刃涟','河闸调度带','水','稀有','潜在极浅水层下，每有生物离水便沿空位放出高速切涟的薄体猎食者。','#367b8b','澜桥区'],
  ['MON_LQ_012','水取','退潮仓廊','水','稀有','用长须钓起浸透旧气味的沉物，再根据附着生物选择伏猎水域的安静水兽。','#516f77','澜桥区'],
  ['MON_LQ_013','码憨憨','回澜主埠','金','稀有','新成员靠近群落时便背起等重石绕岸行走，以震动记住对方步态。','#7b735c','澜桥区'],
  ['MON_LQ_017','邦卡胡迪','汀泊洲','水','稀有','用多层喉囊吸收低频声，再把失去节奏的浑浊水膜覆向入侵者。','#3d6570','澜桥区'],
  ['MON_LQ_018','澜江魁','澜桥区跨地方单元','水','史诗','每隔数年沿主河逆行，以胸鳍掀起不伤岸体却能迫使沿途兽灵退回支汊的巨型洄游兽灵。','#315e70','澜桥区'],
  ['MON_LQ_021','换身壳','退潮仓廊','水','稀有','钻进其他兽灵的空蜕壳并复写残留气味，使领地双方暂时认错彼此归属。','#6b8490','澜桥区']
].map(([id,name,area,element,rarity,description,color,region='澄曜区']) => ({id,name,area,element,rarity,description,color,region}));

const tabs = document.querySelector('.region-tabs');
const feature = document.querySelector('#region-feature');
function showRegion(index) {
  const r = regions[index];
  tabs.querySelectorAll('button').forEach((button, i) => button.classList.toggle('active', i === index));
  feature.innerHTML = `<div class="region-copy"><span class="region-code">${r.code}</span><h3>${r.name}</h3><p>${r.description}</p><div class="region-meta"><span><strong>地区类型</strong>${r.type}</span><span><strong>元素倾向</strong>${r.element}</span></div></div><div class="local-list" style="background:linear-gradient(140deg, ${r.accent}, #183f40)"><h4>可探索地方单元</h4><ul>${r.places.map(p => `<li>${p}</li>`).join('')}</ul></div>`;
}
regions.forEach((r,index) => { const button=document.createElement('button'); button.className=`region-tab ${index===0?'active':''}`; button.textContent=r.name; button.setAttribute('role','tab'); button.addEventListener('click',()=>showRegion(index)); tabs.append(button); });
showRegion(0);

const grid = document.querySelector('#monster-grid');
const dialog = document.querySelector('#monster-dialog');
const dialogContent = document.querySelector('#dialog-content');
let currentFilter = 'all';
let currentRegion = 'all';
function renderMonsters() {
  const search = document.querySelector('#search').value.trim().toLowerCase();
  const shown = monsters.filter(m => (currentFilter==='all'||m.element===currentFilter) && (currentRegion==='all'||m.region===currentRegion) && [m.name,m.region,m.area,m.description,m.id].join(' ').toLowerCase().includes(search));
  grid.innerHTML = shown.length ? shown.map(m => `<button class="monster-card" data-id="${m.id}" style="--card-bg:${m.color}"><div class="card-image"><span class="monster-id">${m.id.replace('MON_','')}</span><span class="monster-symbol">${m.element}</span></div><div class="card-info"><h3>${m.name}</h3><p>${m.region} · ${m.area}</p></div><span class="rarity">${m.rarity}</span></button>`).join('') : '<p class="empty">没有找到符合条件的妖怪。</p>';
  grid.querySelectorAll('.monster-card').forEach(card => card.addEventListener('click', () => openMonster(monsters.find(m => m.id === card.dataset.id))));
}
function openMonster(m) {
  dialogContent.innerHTML = `<div class="dialog-hero" style="--dialog-bg:${m.color}" data-symbol="${m.element}"><p>${m.id}</p><h2>${m.name}</h2></div><div class="dialog-body"><div class="dialog-tags"><span>${m.element}元素</span><span>${m.rarity}</span><span>${m.region}</span><span>${m.area}</span></div><h3>核心概念</h3><p>${m.description}</p><div class="dialog-note">该条目整理自项目中的${m.region}妖怪候选设定档案（C3）。战斗数值与正式设定以项目后续版本为准。</div></div>`;
  dialog.showModal();
}
document.querySelector('#search').addEventListener('input', renderMonsters);
document.querySelectorAll('.filter').forEach(button => button.addEventListener('click', () => { currentFilter=button.dataset.filter; document.querySelectorAll('.filter').forEach(b=>b.classList.toggle('active',b===button)); renderMonsters(); }));
document.querySelectorAll('.region-filter').forEach(button => button.addEventListener('click', () => { currentRegion=button.dataset.region; document.querySelectorAll('.region-filter').forEach(b=>b.classList.toggle('active',b===button)); renderMonsters(); }));
document.querySelector('.dialog-close').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',(event)=>{ if(event.target===dialog) dialog.close(); });
document.querySelector('.menu-button').addEventListener('click',()=>document.querySelector('#regions').scrollIntoView());
renderMonsters();
