import sys,os,pickle,random,zlib,struct,time; sys.path.insert(0,'/home/claude/rt/work'); os.chdir('/home/claude/rt/work')
from lib import blocks
from exact4 import shift
from fix2 import jpfields
import zopfli.zlib as zz
O=open('/home/claude/rt/repo/game/rol/cr/a.cr.codex-original.bak','rb').read()
ol=blocks(O); ob={o:c for o,c,d in ol}; Od={o:d for o,c,d in ol}
P=open('grp9/P1_tudo_prefixos_preservados/a.cr','rb').read(); Pd={o:d for o,c,d in blocks(P)}
new,left=pickle.load(open('exact_res4.pkl','rb'))
def cands(data):
    for level in (9,6,4,1):
        for mem in (9,8,6):
            for strat in (0,1,3):
                c=zlib.compressobj(level,zlib.DEFLATED,-15,mem,strat); yield c.compress(data)+c.flush()
    for it in (5,15):
        yield zz.compress(data,numiterations=it)[2:-4]
def tryit(data,clen):
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
res={}; still=[]; t=time.time()
for o in left:
    d=Pd[o]; clen=ob[o]; rnd=random.Random(o)
    flds=[]
    for i,L in jpfields(Od[o]):
        reg=d[i+4:i+4+L-1]
        if reg!=Od[o][i+4:i+4+L-1]:
            tt=reg.rstrip(b' \0')
            if len(tt)<len(reg): flds.append((i,L,tt))
    z=tryit(d,clen)
    for tr in range(120):
        if z: break
        b=bytearray(d)
        for i,L,tt in flds:
            pad=rnd.choice((b' ',b'\0')); b[i+4:i+4+L-1]=(tt+pad*(L-1-len(tt)))[:L-1]
        z=tryit(bytes(b),clen)
    if z: res[o]=z
    else: still.append(o)
print(len(res),len(still),time.time()-t)
pickle.dump((res,still),open('exact_res5.pkl','wb'))
