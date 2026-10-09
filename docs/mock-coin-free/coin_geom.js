// 錢幣部分交疊的幾何判斷（模擬用）。item 需有：x,y,w,h（外接框）；圓形幣 cr（半徑）；長方形幣 ow,oh,ang（度）。
// 規則：兩枚交疊面積各自 ≤ lim（預設 30%）、且不遮到對方中央的數字區、每枚最多和 1 枚交疊、不是每枚都能交疊（flag）。
const OVG={lim:0.3,min:0.04};
const _disk=[[0,0]];for(const [r,n] of [[.25,6],[.5,12],[.75,18],[.97,24]])for(let i=0;i<n;i++)_disk.push([r*Math.cos(2*Math.PI*i/n),r*Math.sin(2*Math.PI*i/n)]);
const _rect=[];for(let i=0;i<14;i++)for(let j=0;j<6;j++)_rect.push([(i+.5)/14-.5,(j+.5)/6-.5]);
function _sh(a){const cx=a.x+a.w/2,cy=a.y+a.h/2;return a.cr?{c:1,cx,cy,r:a.cr}:{c:0,cx,cy,w:a.ow,h:a.oh,t:(a.ang||0)*Math.PI/180}}
function _in(s,px,py){const dx=px-s.cx,dy=py-s.cy;if(s.c)return dx*dx+dy*dy<=s.r*s.r;const c=Math.cos(-s.t),n=Math.sin(-s.t),lx=dx*c-dy*n,ly=dx*n+dy*c;return Math.abs(lx)<=s.w/2&&Math.abs(ly)<=s.h/2}
function _pts(s){const o=[];if(s.c){for(const p of _disk)o.push([s.cx+p[0]*s.r,s.cy+p[1]*s.r])}else{const c=Math.cos(s.t),n=Math.sin(s.t);for(const p of _rect){const x=p[0]*s.w,y=p[1]*s.h;o.push([s.cx+x*c-y*n,s.cy+x*n+y*c])}}return o}
function _frac(A,B){const ps=_pts(A);let k=0;for(const p of ps)if(_in(B,p[0],p[1]))k++;return k/ps.length}
function _labelHit(A,B){ // B 是否碰到 A 中央的數字區
  const hw=A.c?A.r*.6:A.w*.4,hh=A.c?A.r*.45:A.h*.32,c=Math.cos(A.t||0),n=Math.sin(A.t||0);
  for(let i=-2;i<=2;i++)for(let j=-1;j<=1;j++){const x=i/2*hw,y=j*hh;if(_in(B,A.cx+x*c-y*n,A.cy+x*n+y*c))return true}return false}
// a、o 是否可以「合法交疊」
function overlapOK(a,o){const A=_sh(a),B=_sh(o);
  const f=Math.max(_frac(A,B),_frac(B,A)); if(f<OVG.min||f>OVG.lim)return false;
  // 各自被蓋住的比例都不可超過 lim
  if(_frac(A,B)>OVG.lim||_frac(B,A)>OVG.lim)return false;
  return !_labelHit(A,B)&&!_labelHit(B,A)}
// 檢查 a 放在目前位置是否合法；回傳 {ok, partner}
function checkPos(a,items,dist,minGap){let partner=null;
  for(const o of items){if(o===a||o.x===undefined)continue;
    if(dist(a,o)>=minGap)continue;
    if(!OVG.on||!a.flag||!o.flag||a.ov||o.ov||partner)return {ok:false};
    if(!overlapOK(a,o))return {ok:false};
    partner=o}
  return {ok:true,partner}}
// 提出候選位置：有 flag 的幣，偶數次嘗試改成「貼近某枚也有 flag 的幣」以產生部分交疊；其餘純隨機
function propose(a,items,x0,x1,y0,y1,n,rnd){
  a.x=x0+rnd()*(x1-x0-a.w);a.y=y0+rnd()*(y1-y0-a.h);
  if(OVG.on&&a.flag&&n%2==0){const c=items.filter(o=>o!==a&&o.x!==undefined&&o.flag&&!o.ov);
    if(c.length){const o=c[(rnd()*c.length)|0],t=rnd()*2*Math.PI,rr=(Math.max(a.w,a.h)+Math.max(o.w,o.h))/2*(0.55+0.3*rnd());
      a.x=Math.min(Math.max(o.x+o.w/2+rr*Math.cos(t)-a.w/2,x0),x1-a.w);a.y=Math.min(Math.max(o.y+o.h/2+rr*Math.sin(t)-a.h/2,y0),y1-a.h)}}}
