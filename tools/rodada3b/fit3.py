import sys,zlib,struct,pickle,random,time; sys.path.insert(0,'/home/claude/rt/work')
from exact4 import shift
def comp(data,level,mem,strat,cuts,fl):
    c=zlib.compressobj(level,zlib.DEFLATED,-15,mem,strat); out=b'';p=0
    for x,f in zip(cuts,fl):
        out+=c.compress(data[p:x]); out+=c.flush(f); p=x
    out+=c.compress(data[p:]); out+=c.flush(); return out
def fit(data,clen,seed=0,budget=60):
    ad=struct.pack('>I',zlib.adler32(data)&0xffffffff); target=clen-6; n=len(data)
    rnd=random.Random(seed); t0=time.time()
    while time.time()-t0<budget:
        level=rnd.choice((9,6,4,1,2,3,5,7,8)); mem=rnd.choice((9,8,7,6)); strat=rnd.choice((0,0,1,3,4))
        F=rnd.choice((zlib.Z_SYNC_FLUSH,zlib.Z_FULL_FLUSH,zlib.Z_PARTIAL_FLUSH))
        lo,hi=0,min(400,n-2)
        def ln(m,jit=0):
            cuts=[int(n*(i+1)/(m+1))+jit for i in range(m)]
            return cuts
        # find largest m with len<=target
        best=None
        jit=rnd.randrange(0,50)
        for m in range(0,hi+1,1):
            cuts=ln(m,jit); r=comp(data,level,mem,strat,cuts,[F]*m)
            if len(r)>target: break
            best=(m,r)
            if target-len(r)<=14:
                for k in range(0,14):
                    rr=shift(r,k)
                    if len(rr)==target:
                        z=b'\x78\x9c'+rr+ad
                        try:
                            if zlib.decompress(z)==data: return z
                        except Exception: pass
                    if len(rr)>target: break
            if m>60 and target-len(r)>400: break
    return None
if __name__=='__main__':
    pre=pickle.load(open('k3prep.pkl','rb'))
    res={};fail=[]
    for o,(c,d,nd) in pre.items():
        t=time.time(); z=fit(nd,c,budget=40)
        if z: res[o]=z
        else: fail.append(o)
        print(o,c,len(nd),'OK' if z else 'FAIL',round(time.time()-t,1),flush=True)
    pickle.dump((res,fail),open('k3fit.pkl','wb'))
    print(len(res),len(fail))
