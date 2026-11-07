import sys,os,pickle,random,zlib,struct,time,itertools,re; sys.path.insert(0,'/home/claude/rt/work'); os.chdir('/home/claude/rt/work')
from lib import blocks
from exact4 import shift
import zopfli.zlib as zz
O=open('/home/claude/rt/repo/game/rol/cr/a.cr.codex-original.bak','rb').read()
G=open('/home/claude/rt/repo/game/rol/cr/a.cr','rb').read()
ob=blocks(O); cl={o:c for o,c,d in ob}; od={o:d for o,c,d in ob}; gd={o:d for o,c,d in blocks(G)}
def ofields(a):
    r=[]
    for i in range(0,len(a)-5):
        L=struct.unpack_from('<I',a,i)[0]
        if 2<=L<=400 and i+4+L<=len(a) and a[i+4+L-1]==0 and any(x>127 for x in a[i+4:i+3+L]): r.append((i,L))
    # drop nested overlaps: keep the earliest, non-overlapping
    out=[];end=-1
    for i,L in r:
        if i>=end: out.append((i,L)); end=i+4+L
    return out
def texts(o):
    """list of (i,L,text) of translated fields, text taken from G (handles shrunk L)"""
    a=od[o]; b=gd[o]; r=[]
    for i,L in ofields(a):
        L2=struct.unpack_from('<I',b,i)[0]
        if L2==L: t=b[i+4:i+4+L-1]
        elif 2<=L2<L: t=b[i+4:i+4+L2-1]
        else: continue
        if t!=a[i+4:i+4+L-1]:
            t=t.rstrip(b' \0'); r.append((i,L,t))
    return r
def assemble(o,fl,pad=b' '):
    b=bytearray(od[o])
    for i,L,t in fl:
        t=t[:L-1]; b[i+4:i+4+L-1]=(t+pad*(L-1-len(t)))[:L-1]
    return bytes(b)
def cands(data):
    for level in (9,6,1,4):
        for mem in (9,8):
            for strat in (0,1):
                c=zlib.compressobj(level,zlib.DEFLATED,-15,mem,strat); yield c.compress(data)+c.flush()
    for it in (5,15): yield zz.compress(data,numiterations=it)[2:-4]
def tryit(data,clen,full=True):
    ad=struct.pack('>I',zlib.adler32(data)&0xffffffff)
    for raw in cands(data):
        for k in range(0,12):
            r=shift(raw,k)
            if len(r)+6==clen:
                out=b'\x78\x9c'+r+ad
                try:
                    if zlib.decompress(out)==data: return out
                except Exception: pass
            if len(r)+6>clen: break
    if full:
        import exact2
        rnd=random.Random(len(data))
        for t in range(300):
            level=rnd.choice((9,6,4,1)); mem=rnd.choice((9,8,7)); strat=rnd.choice((0,1,3))
            k=rnd.choice((0,1,2,3,4,6)); n=len(data)
            cuts=sorted(rnd.sample(range(1,n),min(k,n-1))) if k else []
            fm=[rnd.choice((zlib.Z_SYNC_FLUSH,zlib.Z_PARTIAL_FLUSH)) for _ in cuts]
            r=exact2.attempt(data,clen,level,mem,strat,cuts,fm)
            if len(r)==clen-6:
                z=b'\x78\x9c'+r+ad
                if zlib.decompress(z)==data: return z
def variants(t,maxlen):
    s=t.decode('latin1'); out=[s]
    out.append(s.replace(' ',''))
    out.append(re.sub(r'(\w{5,})',lambda m:m.group(1)[:4]+'.',s))
    out.append(re.sub(r'(\w{4,})',lambda m:m.group(1)[:3]+'.',s))
    out.append(re.sub(r'(?<=\w)[aeiou](?=\w)','',s))
    out.append(re.sub(r'(?<=\w)[aeiou]','',s))
    for n in (1,2,3,4,5,6,8): 
        if len(s)>n+2: out.append(s[:-n])
    seen=[];[seen.append(x) for x in out if x and x not in seen and len(x.encode('cp932','replace'))<=maxlen]
    return [x.encode('latin1') for x in seen]
if __name__=='__main__':
    todo=[o for o in od if od[o]!=gd[o]]
    shr=[]
    for o in todo:
        fl=texts(o)
        # is any L shrunk?
        a=od[o];b=gd[o]
        if any(struct.unpack_from('<I',b,i)[0]!=L for i,L in ofields(a)): shr.append(o)
    print(len(todo),len(shr))
    res={};fail=[];t0=time.time();changedtext=0
    for o in shr:
        fl=texts(o); clen=cl[o]; ok=None
        opts=[variants(t,L-1) for i,L,t in fl]
        if not fl: fail.append(o); continue
        for ci,combo in enumerate(itertools.product(*opts)):
            if ci>12: break
            for pad in (b' ',b'\0'):
                data=assemble(o,[(i,L,t) for (i,L,_),t in zip(fl,combo)],pad)
                z=tryit(data,clen,full=(ci==0))
                if z: ok=(z,combo,pad); break
            if ok: break
        if ok: res[o]=ok
        else: fail.append(o)
    print('fitted',len(res),'failed',len(fail),time.time()-t0)
    pickle.dump((res,fail),open('fixL_res.pkl','wb'))
