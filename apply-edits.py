#!/usr/bin/env python3
"""Usage: python apply_edits.py index.html   ->  writes index.new.html (original untouched)."""
import sys
src = sys.argv[1] if len(sys.argv) > 1 else "index.html"
s = open(src, encoding="utf-8").read()
fails = []
def R(old, new, tag=""):
    global s
    if s.count(old) != 1:
        fails.append(f"{tag or old[:60]!r}: found {s.count(old)} times")
        return
    s = s.replace(old, new)

# ---------- CSS ----------
R("</style>", r'''
/* --- edits --- */
.authwrap{min-height:calc(100vh - 40px);display:flex;flex-direction:column;align-items:center;justify-content:center}
.authwrap .land{text-align:center;padding:0 0 20px}.authwrap .land h1,.authwrap .land p{margin-left:auto;margin-right:auto}.authwrap .logo{margin:0}
.authwrap .auth{width:100%;max-width:440px;margin-top:0}
.sc{grid-template-columns:260px 1fr;gap:36px;padding:22px 28px}
.sl{border-right:1px solid var(--line);padding-right:28px}
.mstat{margin-top:16px;font-size:.9rem;color:var(--muted)}.mstat b{font:500 1.15rem 'JetBrains Mono',monospace;color:var(--ink)}
.legend{display:flex;flex-direction:column;gap:7px;margin-top:14px;font-size:.8rem;color:var(--muted)}
.legend span{display:flex;align-items:center;gap:9px}
.lgd{width:14px;height:14px;border-radius:4px;display:inline-block;border:1px dashed var(--line)}
.lgd.on{background:var(--brand);border-color:var(--brand)}.lgd.fz{background:#cfe8ff;border:1px solid #9fcdf2}
@media(max-width:700px){.sc{grid-template-columns:1fr;gap:16px}.sl{border-right:0;padding-right:0}}
.crow{grid-template-columns:1fr minmax(120px,170px) 42px;padding:12px 16px}
.cmeta{color:var(--muted);font-size:.76rem;letter-spacing:.02em}
@media(max-width:620px){.crow{grid-template-columns:1fr 40px}}
</style>''', "css")

# ---------- 1. sign-up centered ----------
R('const authView=()=>{const s=mode=="up";return`<div class="land">',
  'const authView=()=>{const s=mode=="up";return`<div class="authwrap"><div class="land">', "auth open")
R('<p><button class="btn s" data-a="mode">${s?"I have an account":"Create an account"}</button></p></div>`};',
  '<p><button class="btn s" data-a="mode">${s?"I have an account":"Create an account"}</button></p></div></div>`};', "auth close")

# ---------- 2. remove corner rounding ----------
R('<div class="f" style="margin-top:14px"><label for="tr">Corner roundness</label><input id="tr" type="range" min="0" max="14" data-t="radius" value="${radius}"></div>', "", "slider")
R('try{radius=JSON.parse(localStorage.getItem("theme4")||"{}").radius??4}catch{}', "", "radius load")

# ---------- 3. streak card text ----------
R('<div class="k" style="margin-top:6px">${cnt} study ${cnt==1?"day":"days"} this month</div><div class="k">Filled = studied. Blue = freeze. Dashed = missed.</div></div>',
  '<div class="mstat"><b>${cnt}</b> study ${cnt==1?"day":"days"} this month</div><div class="legend"><span><i class="lgd on"></i>Studied</span><span><i class="lgd fz"></i>Streak freeze</span><span><i class="lgd"></i>Missed</span></div></div>', "streak")

# ---------- 4. course list: no numbers, cleaner meta, filters ----------
R('<span class="cn">${String(i+1).padStart(2,"0")}</span><span class="ct"><b>${esc(c.title)}</b><span>${esc(c.blurb)}</span></span>',
  '<span class="ct"><b>${esc(c.title)}</b><span>${esc(c.blurb)}</span><span class="cmeta">${[c.category||"General",c.level,(c.mins||"?")+" min",c.draft?"draft":c.featured?"featured":""].filter(Boolean).map(esc).join(" · ")}</span></span>', "row left")
R('<span class="cm2"><span class="k">${esc(c.category||"General")} / ${esc(c.level||"")} / ${esc(c.mins||"?")} min${c.draft?" / draft":c.featured?" / featured":""}</span><span class="bar">',
  '<span class="cm2"><span class="bar">', "row right")
R('list=(filter=="For you"?vis:vis.filter(c=>c.category==filter)).sort((a,b)=>score(b)-score(a));',
  'list=(filter=="For you"?vis:vis.filter(c=>c.category==filter)).filter(c=>{const p=prog(c),m=+c.mins||0;return(FL.stat=="All"||(FL.stat=="In progress"?p.d>0&&p.d<p.n:FL.stat=="Completed"?p.n&&p.d==p.n:p.d==0))&&(FL.len=="Any"||(FL.len=="Short"?m<=10:FL.len=="Medium"?m>10&&m<=20:m>20))&&(FL.lvl=="Any"||c.level==FL.lvl)}).sort((a,b)=>score(b)-score(a));', "filter logic")
R('<div class="chips">${cats.map(c=>`<button class="btn s ${c==filter?"on":""}" data-a="cat" data-v="${esc(c)}">${esc(c)}</button>`).join("")}</div>',
  '<div class="chips">${cats.map(c=>`<button class="btn s ${c==filter?"on":""}" data-a="cat" data-v="${esc(c)}">${esc(c)}</button>`).join("")}</div>'
  '<div class="row" style="gap:14px;margin:0 0 12px">${[["stat","Progress",["All","In progress","Not started","Completed"]],["len","Length",["Any","Short","Medium","Long"]],["lvl","Level",["Any",...LEVELS]]].map(([k,l,o])=>`<label class="k">${l} <select data-f="${k}" style="width:auto;padding:4px 8px">${o.map(x=>`<option ${x==FL[k]?"selected":""}>${x}</option>`).join("")}</select></label>`).join("")}<span class="k">Short: 10 min or less. Medium: 11-20. Long: 21+</span></div>', "filter ui")
R('No courses yet. ', 'No courses found. ', "empty msg")
R('document.addEventListener("keydown",e=>',
  'document.addEventListener("change",e=>{if(e.target.dataset.f){FL[e.target.dataset.f]=e.target.value;render()}});\ndocument.addEventListener("keydown",e=>', "filter listener")

# ---------- 5. friend requests + DMs ----------
R('return`<div class="f" style="margin-top:12px"><label for="pq">', 'return`${reqBox()}<div class="f" style="margin-top:12px"><label for="pq">', "people")
R('${av({name:g.name,group:1},40)}<span style="flex:1;min-width:0"><b>${esc(g.name)}</b>',
  '${av({name:gname(g),group:1},40)}<span style="flex:1;min-width:0"><b>${esc(gname(g))}</b>', "chats list")
R('${av({name:g.name,group:1},34)}<div style="flex:1;min-width:0"><b>${esc(g.name)}</b><div class="k">${(g.members||[]).length} members</div></div><button class="btn s" data-a="members">Members</button>',
  '${av({name:gname(g),group:1},34)}<div style="flex:1;min-width:0"><b>${esc(gname(g))}</b><div class="k">${g.dm?"Private chat":(g.members||[]).length+" members"}</div></div>${g.dm?"":`<button class="btn s" data-a="members">Members</button>`}', "chat head")
R('const gs=groups.filter(g=>(g.owner==user.uid||isAdmin())&&!(g.members||[]).includes(id));',
  'const gs=groups.filter(g=>!g.dm&&(g.owner==user.uid||isAdmin())&&!(g.members||[]).includes(id));', "addToGroup")
R('<button class="btn ${isFriend(id)?"on":"p"}" data-a="friend" data-v="${id}">${frState(id)}</button>',
  '<button class="btn ${isFriend(id)?"on":"p"}" data-a="friend" data-v="${id}">${frState(id)}</button>${isFriend(id)?`<button class="btn p" data-a="dm" data-v="${id}">Message</button>`:""}', "message btn")
R('if(id=="mgF"&&v("mt")){await addDoc(collection(db,"msgs"),{gid,uid:user.uid,text:v("mt"),at:Date.now()});g("mt").value=""}',
  'if(id=="mgF"&&v("mt")){const t=v("mt"),bad=modCheck(t);if(bad){await addDoc(collection(db,"flags"),{uid:user.uid,gid,text:t.slice(0,500),why:bad,at:Date.now()});return toast("Not sent: "+bad)}await addDoc(collection(db,"msgs"),{gid,uid:user.uid,text:t,at:Date.now()});g("mt").value=""}', "send")
R('L(collection(db,"credits"),x=>credits=x);',
  'L(collection(db,"credits"),x=>credits=x);if(u.uid==ADMIN_UID)L(query(collection(db,"flags"),orderBy("at","desc"),limit(100)),x=>flags=x);', "flags listener")
R('<button class="dl" data-a="site">Site settings</button>',
  '<button class="dl" data-a="site">Site settings</button><button class="dl" data-a="go" data-v="flags">Moderation</button>', "drawer admin")
R('["shop","Shop"],["me","Profile"]', '["shop","Shop"],["board","Leaderboard"],["me","Profile"]', "drawer")
R('chat:chatView}[view]||home)()', 'chat:chatView,board:lbView,flags:flagView}[view]||home)()', "view map")
R('buddy:v=>saveMe({buddy:v}),',
  'buddy:v=>saveMe({buddy:v}),decline:v=>deleteDoc(doc(db,"friends",v+"_"+user.uid)),lbt:v=>{lbT=v;render()},lbs:v=>{lbS=v;render()},'
  'dm:async v=>{const id="dm_"+[user.uid,v].sort().join("_");if(!groups.some(g=>g.id==id))await setDoc(doc(db,"groups",id),{name:"",dm:true,owner:user.uid,members:[user.uid,v],at:Date.now()});gid=id;view="chat";modal=null;render()},', "actions")

# ---------- 6. profile customisation ----------
R('["color","range","file"]', '["range","file"]', "color restore")
R('await saveMe({name:v("pn"),pronouns:v("pr"),bio:v("pb")});toast("Saved")}',
  'await saveMe({name:v("pn"),pronouns:v("pr"),bio:v("pb"),prof:{accent:g("pfA").value,banner:g("pfB").value,font:g("pfF").value,status:v("pfS"),tags:v("pfT"),quote:v("pfQ"),link:v("pfL"),showDone:g("pfD").checked,showWip:g("pfW").checked}});toast("Saved")}', "save profile")
R('<textarea id="pb" maxlength="160">${esc(m.bio||"")}</textarea></div><div class="err" id="err"></div>',
  '<textarea id="pb" maxlength="300">${esc(m.bio||"")}</textarea></div>${profFields(m)}<div class="err" id="err"></div>', "settings bio")
R('<div class="box"><div class="row" style="align-items:flex-start">${av(u,80)}',
  '<div class="box" style="${profStyle(u)}">${profBanner(u)}<div class="row" style="align-items:flex-start">${av(u,80)}', "profile open")
R('<p style="max-width:52ch;margin:6px 0 0">${esc(u.bio||"No bio yet.")}</p></div>',
  '<p style="max-width:52ch;margin:6px 0 0;white-space:pre-wrap">${esc(u.bio||"No bio yet.")}</p>${profExtras(u)}</div>', "profile bio")
R('${pets.length?`<div class="box"><h3>Pets</h3>', '${courseLists(u)}${pets.length?`<div class="box"><h3>Pets</h3>', "course lists")

# ---------- new helpers block ----------
R('function settings(){const m=me();return', r'''/* ===== edits: filters, moderation, leaderboard, profile styling ===== */
const FL={stat:"All",len:"Any",lvl:"Any"};let flags=[],lbT="all",lbS="courses";
const FONTS={Sans:"'Inter',sans-serif",Mono:"'JetBrains Mono',monospace",Serif:"Georgia,serif"};
const BAN={Solid:"var(--brand)",Gradient:"linear-gradient(120deg,var(--brand),transparent)",Dots:"radial-gradient(var(--brand) 1.5px,transparent 1.5px) 0 0/14px 14px",Stripes:"repeating-linear-gradient(45deg,var(--brand) 0 6px,transparent 6px 14px)"};
const norm=t=>t.toLowerCase().replace(/[@4]/g,"a").replace(/[1!|]/g,"i").replace(/0/g,"o").replace(/3/g,"e").replace(/\$/g,"s").replace(/[^a-z\s]/g," ").replace(/\s+/g," ");
const THREAT=/\b(kill|murder|shoot|stab|hurt|rape)\s+(you|u|ya|yourself)\b|\bkys\b|\bkill\s+yourself\b|\b(ill|i will|imma)\s+(find|get|kill|hurt)\s+(you|u)\b|\b(hope|wish)\s+(you|u)\s+die\b|\bgo\s+die\b|\bknow where you live\b/;
const INSULT=/\b(worthless|waste of (space|oxygen)|piece of (shit|trash|garbage)|subhuman|retard\w*|nobody likes you|everyone hates you|you should (die|disappear)|ugly (freak|pig))\b/;
const modCheck=t=>{const n=norm(t);return THREAT.test(n)?"threats aren't allowed":INSULT.test(n)?"that's too harsh, keep it kind":""};
const gname=g=>g.dm?(users.find(u=>u.id==(g.members||[]).find(x=>x!=user.uid))?.name||"user"):g.name;
const reqBox=()=>{const r=friends.filter(f=>f.b==user.uid&&!fr(user.uid,f.a)).map(f=>users.find(u=>u.id==f.a)).filter(Boolean);
 return r.length?`<div class="box"><h3>Friend requests (${r.length})</h3>${r.map(u=>`<div class="row" style="padding:8px 0;border-top:1px solid var(--line)">${avBtn(u,u.id,32)}${nmBtn(u,u.id)}<span class="sp"></span><button class="btn s p" data-a="friend" data-v="${u.id}">Accept</button><button class="btn s" data-a="decline" data-v="${u.id}">Decline</button></div>`).join("")}</div>`:""};
const lbView=()=>{const val=u=>lbS=="courses"?cc(u):(u.coins||0);
 const l=users.filter(u=>u.name&&(lbT=="all"||u.id==user.uid||isFriend(u.id))).sort((a,b)=>val(b)-val(a)||(b.coins||0)-(a.coins||0)||cc(b)-cc(a)).slice(0,50);
 return`<h1>Leaderboard</h1><div class="row" style="margin:12px 0"><span class="row" style="gap:6px">${[["all","Everyone"],["friends","Friends"]].map(([v,n])=>`<button class="btn s ${lbT==v?"on":""}" data-a="lbt" data-v="${v}">${n}</button>`).join("")}</span><span class="row sp" style="gap:6px">${[["courses","Courses completed"],["coins","Coins"]].map(([v,n])=>`<button class="btn s ${lbS==v?"on":""}" data-a="lbs" data-v="${v}">${n}</button>`).join("")}</span></div>
 ${l.map((u,i)=>`<button class="les ${u.id==user.uid?"cur":""}" data-a="user" data-v="${u.id}"><span class="cn" style="min-width:26px">${i+1}</span>${av(u,32)}<span style="flex:1;min-width:0"><b>${esc(u.name)}</b>${u.id==user.uid?' <span class="k">you</span>':""}</span><span class="k" style="${lbS=="courses"?"color:var(--ink)":""}">${cc(u)} courses</span><span class="k" style="${lbS=="coins"?"color:var(--ink)":""}">${u.coins||0} coins</span></button>`).join("")||'<p class="k">Nobody here yet. Add some friends.</p>'}`};
const flagView=()=>`<h1>Moderation</h1><h3 style="margin:14px 0 6px">Flagged messages</h3>${flags.map(f=>{const u=users.find(x=>x.id==f.uid);return`<div class="box"><div class="row">${nmBtn(u,f.uid)}<span class="k">${ago(f.at)} / ${esc(f.why)}</span></div><p style="margin:6px 0 0">${esc(f.text)}</p></div>`}).join("")||'<p class="k">Nothing flagged.</p>'}<h3 style="margin:18px 0 6px">All private chats</h3>${groups.filter(g=>g.dm).map(g=>`<button class="les" data-a="chat" data-v="${g.id}">${(g.members||[]).map(id=>esc(users.find(u=>u.id==id)?.name||"user")).join(" and ")}</button>`).join("")||'<p class="k">None yet.</p>'}`;
const profStyle=u=>{const p=u.prof||{},a=/^#[0-9a-f]{6}$/i.test(p.accent||"")?p.accent:"";return(a?`--brand:${a};--on:${lum(a)>.45?"#111":"#fff"};`:"")+(FONTS[p.font]?`font-family:${FONTS[p.font]};`:"")};
const profBanner=u=>{const b=BAN[(u.prof||{}).banner];return b?`<div style="height:72px;margin:-14px -14px 14px;background:${b};opacity:.55;border-radius:var(--radius) var(--radius) 0 0"></div>`:""};
const profExtras=u=>{const p=u.prof||{},tags=(p.tags||"").split(",").map(x=>x.trim()).filter(Boolean).slice(0,6);
 return`${p.status?`<div style="margin-top:8px"><span class="chip">${esc(p.status)}</span></div>`:""}${tags.length?`<div class="row" style="gap:6px;margin-top:8px">${tags.map(t=>`<span class="chip">#${esc(t)}</span>`).join("")}</div>`:""}${p.quote?`<p class="lg" style="margin:10px 0 0">\u201C${esc(p.quote)}\u201D</p>`:""}${/^https?:\/\//i.test(p.link||"")?`<p style="margin:8px 0 0"><a href="${esc(p.link)}" target="_blank" rel="noopener nofollow">${esc(p.link.replace(/^https?:\/\//i,""))}</a></p>`:""}`};
const courseLists=u=>{const p=u.prof||{},dn=[],wip=[];courses.filter(c=>!c.draft).forEach(c=>{const g=prog(c,u);if(g.n&&g.d==g.n)dn.push(c);else if(g.d>0)wip.push([c,g])});
 const a=p.showDone===false||!dn.length?"":`<div class="box" style="${profStyle(u)}"><h3>Completed courses</h3><div class="row" style="gap:6px;margin-top:8px">${dn.map(c=>`<span class="chip">${esc(c.title)}</span>`).join("")}</div></div>`;
 const b=p.showWip===false||!wip.length?"":`<div class="box" style="${profStyle(u)}"><h3>Working on now</h3>${wip.map(([c,g])=>`<div style="margin-top:10px"><div class="row"><b>${esc(c.title)}</b><span class="k sp">${g.d}/${g.n}</span></div><div class="bar" style="margin-top:4px"><i style="width:${g.d/g.n*100}%"></i></div></div>`).join("")}</div>`;
 return a+b};
const profFields=m=>{const p=m.prof||{},sel=(id,l,o,v)=>`<div class="f"><label for="${id}">${l}</label><select id="${id}">${o.map(x=>`<option ${x==v?"selected":""}>${x}</option>`).join("")}</select></div>`;
 return`<h3 style="margin:16px 0 6px">Customize your profile</h3>
 <div class="two" style="gap:10px"><div class="f"><label for="pfA">Accent color</label><input id="pfA" type="color" value="${esc(p.accent||"#6c9bd8")}"></div>${sel("pfB","Banner",["None","Solid","Gradient","Dots","Stripes"],p.banner||"None")}</div>
 <div class="two" style="gap:10px">${sel("pfF","Font",Object.keys(FONTS),p.font||"Sans")}<div class="f"><label for="pfS">Status</label><input id="pfS" maxlength="40" value="${esc(p.status||"")}" placeholder="grinding chess"></div></div>
 <div class="f"><label for="pfT">Tags (comma separated, up to 6)</label><input id="pfT" value="${esc(p.tags||"")}" placeholder="night owl, chess, js"></div>
 <div class="f"><label for="pfQ">Favourite quote</label><input id="pfQ" maxlength="100" value="${esc(p.quote||"")}"></div>
 <div class="f"><label for="pfL">Link (https://...)</label><input id="pfL" value="${esc(p.link||"")}"></div>
 <label style="display:block"><input id="pfD" type="checkbox" ${p.showDone===false?"":"checked"}> Show courses I've completed</label><label style="display:block;margin-bottom:10px"><input id="pfW" type="checkbox" ${p.showWip===false?"":"checked"}> Show courses I'm working on</label>`};
function settings(){const m=me();return''', "helpers")

if fails:
    print("NOT APPLIED. These snippets didn't match your file exactly:")
    print("\n".join(" - "+f for f in fails)); sys.exit(1)
out = src.replace(".html", ".new.html")
open(out, "w", encoding="utf-8").write(s)
print("Done ->", out)
