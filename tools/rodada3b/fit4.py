import zlib,struct,random,time,sys; sys.path.insert(0,'/home/claude/rt/work')
from fit3 import comp
from exact4 import shift
def fit_rand(data,clen,budget=120,seed=1):
    ad=struct.pack('>I',zlib.adler32(data)&0xffffffff); T=clen-6; n=len(data)
    rnd=random.Random(seed); t0=time.time()
    while time.time()-t0<budget:
        level=rnd.choice((9,6,4,1,2,3,5,7,8)); mem=rnd.choice((9,8,7,6,5)); strat=rnd.choice((0,0,1,3,4))
        k=rnd.choice((0,1,1,2,2,3)); 
        cuts=sorted(rnd.sample(range(1,n),k)) if k else []
        fl=[rnd.choice((zlib.Z_SYNC_FLUSH,zlib.Z_PARTIAL_FLUSH,zlib.Z_FULL_FLUSH,zlib.Z_BLOCK)) for _ in cuts]
        try: r=comp(data,level,mem,strat,cuts,fl)
        except Exception: continue
        if len(r)>T or T-len(r)>14: continue
        for kk in range(0,14):
            rr=shift(r,kk)
            if len(rr)==T:
                z=b'\x78\x9c'+rr+ad
                try:
                    if zlib.decompress(z)==data: return z
                except Exception: pass
            if len(rr)>T: break
    return None
if __name__=='__main__':
    import pickle
    pre=pickle.load(open('k3prep.pkl','rb'))
    res,fail=pickle.load(open('k3fit.pkl','rb'))
    for o in list(fail):
        c,d,nd=pre[o]; z=fit_rand(nd,c)
        print(o,'OK' if z else 'FAIL',flush=True)
        if z: res[o]=z; fail.remove(o)
    pickle.dump((res,fail),open('k3fit.pkl','wb')); print(len(res),len(fail))
