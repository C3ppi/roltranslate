import sys,os,pickle,random,zlib,struct,time,itertools,re,json; sys.path.insert(0,'/home/claude/rt/work'); os.chdir('/home/claude/rt/work')
from lib import blocks
from exact4 import shift
from fix2 import jpfields
import zopfli.zlib as zz
O=open('/home/claude/rt/repo/game/rol/cr/a.cr.codex-original.bak','rb').read()
ol=blocks(O); ob={o:c for o,c,d in ol}; Od={o:d for o,c,d in ol}
P=open('grp9/P1_tudo_prefixos_preservados/a.cr','rb').read(); Pd={o:d for o,c,d in blocks(P)}
left=pickle.load(open('exact_res6.pkl','rb'))[1]
def cands(data):
    for level in (9,6,1):
        for mem in (9,8):
            for strat in (0,1):
                c=zlib.compressobj(level,zlib.DEFLATED,-15,mem,strat); yield c.compress(data)+c.flush()
    yield zz.compress(data,numiterations=8)[2:-4]
def tryit(data,clen):
    ad=struct.pack('>I',zlib.adler32(data)&0xffffffff)
    for raw in cands(data):
        for k in range(0,10):
            r=shift(raw,k)
            if len(r)+6==clen:
                out=b'\x78\x9c'+r+ad
                try:
                    if zlib.decompress(out)==data: return out
                except Exception: pass
            if len(r)+6>clen: break
def variants(t,maxlen):
    t=t.decode('latin1'); out=[t]
    out.append(t.replace(' ',''))
    out.append(re.sub(r'(\w{5,})',lambda m:m.group(1)[:4]+'.',t))
    out.append(re.sub(r'(?<=\w)[aeiou](?=\w)','',t))
    for n in (1,2,3,4):
        if len(t)>n+2: out.append(t[:-n])
    seen=[];[seen.append(x) for x in out if x and x not in seen and len(x.encode('cp932','replace'))<=maxlen]
    return [x.encode('latin1') for x in seen]
res={}; still=[]; t0=time.time()
for o in left:
    d=Pd[o]; clen=ob[o]
    flds=[]
    for i,L in jpfields(Od[o]):
        reg=d[i+4:i+4+L-1]
        if reg!=Od[o][i+4:i+4+L-1]: flds.append((i,L,reg.rstrip(b' \0')))
    if not flds or len(flds)>2: still.append(o); continue
    opts=[variants(tt,L-1) for i,L,tt in flds]
    found=None
    for combo in itertools.product(*opts):
        for pad in (b' ',b'\0'):
            b=bytearray(d)
            for (i,L,_),v in zip(flds,combo): b[i+4:i+4+L-1]=(v+pad*(L-1-len(v)))[:L-1]
            z=tryit(bytes(b),clen)
            if z: found=(z,bytes(b),[v for v in combo]); break
        if found: break
    if found: res[o]=found
    else: still.append(o)
print(len(res),len(still),time.time()-t0)
pickle.dump((res,still),open('exact_res7.pkl','wb'))
