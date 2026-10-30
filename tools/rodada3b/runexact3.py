import sys,os,pickle,random,zlib,struct,time; sys.path.insert(0,'/home/claude/rt/work'); os.chdir('/home/claude/rt/work')
from lib import blocks
from exact2 import attempt
from fix2 import jpfields
O=open('/home/claude/rt/repo/game/rol/cr/a.cr.codex-original.bak','rb').read()
ol=blocks(O); ob={o:c for o,c,d in ol}; Od={o:d for o,c,d in ol}
P=open('grp9/P1_tudo_prefixos_preservados/a.cr','rb').read(); Pd={o:d for o,c,d in blocks(P)}
res,bad=pickle.load(open('exact_res.pkl','rb')); pickle.dump((res,bad),open('exact_res_backup.pkl','wb'))
def exact3(o,tries=3000):
    d=Pd[o]; clen=ob[o]; rnd=random.Random(o)
    flds=[]
    for i,L in jpfields(Od[o]):
        reg=d[i+4:i+4+L-1]
        if reg!=Od[o][i+4:i+4+L-1]:
            t=reg.rstrip(b' \0')
            if len(t)<len(reg): flds.append((i,L,t))
    for tr in range(tries):
        b=bytearray(d)
        for i,L,t in flds:
            mode=rnd.choice((0,1,2))
            pad=b' ' if mode==0 else b'\0'
            if mode==2: b[i+4:i+4+L-1]=t+b' '*rnd.randint(0,L-1-len(t))+b'\0'*(L-1-len(t)-0) if False else (t+pad*(L-1-len(t)))[:L-1]
            else: b[i+4:i+4+L-1]=(t+pad*(L-1-len(t)))[:L-1]
        data=bytes(b)
        level=rnd.choice((9,9,6,4,1)); mem=rnd.choice((9,8,7,6)); strat=rnd.choice((0,0,1,3))
        k=rnd.choice((0,0,1,2,3,4)); n=len(data)
        cuts=sorted(rnd.sample(range(1,n),min(k,n-1))) if k else []
        fm=[rnd.choice((zlib.Z_SYNC_FLUSH,zlib.Z_PARTIAL_FLUSH,zlib.Z_FULL_FLUSH)) for _ in cuts]
        r=attempt(data,clen,level,mem,strat,cuts,fm)
        if len(r)==clen-6:
            z=b'\x78\x9c'+r+struct.pack('>I',zlib.adler32(data)&0xffffffff)
            if zlib.decompress(z)==data: return z,data
    return None
got={}; still=[]
t=time.time()
for o in bad:
    r=exact3(o)
    if r: got[o]=r
    else: still.append(o)
print(len(got),len(still),time.time()-t)
pickle.dump((got,still),open('exact_res3.pkl','wb'))
