import zlib,struct,random
def attempt(data,clen,level,mem,strat,cuts,fm=None):
    fm=list(fm) if fm else []
    c=zlib.compressobj(level,zlib.DEFLATED,-15,mem,strat); out=b''; prev=0
    for p in cuts:
        out+=c.compress(data[prev:p])+c.flush(fm.pop() if fm else zlib.Z_SYNC_FLUSH); prev=p
    out+=c.compress(data[prev:])+c.flush(zlib.Z_FINISH)
    return out
def exact(data,clen,tries=3000,seed=1):
    rnd=random.Random(seed); n=len(data)
    ad=struct.pack('>I',zlib.adler32(data)&0xffffffff); target=clen-6
    best=None
    for t in range(tries):
        level=rnd.choice((9,9,6,4,1)); mem=rnd.choice((9,8,7,6)); strat=rnd.choice((0,0,1,3))
        k=rnd.choice((0,1,1,2,2,3,4,5,6,8,10)) if t>5 else 0
        cuts=sorted(rnd.sample(range(1,n),min(k,n-1))) if k else []
        fm=[rnd.choice((zlib.Z_SYNC_FLUSH,zlib.Z_PARTIAL_FLUSH,zlib.Z_PARTIAL_FLUSH,zlib.Z_FULL_FLUSH)) for _ in cuts]
        r=attempt(data,clen,level,mem,strat,cuts,fm)
        if len(r)==target:
            z=b'\x78\x9c'+r+ad
            if zlib.decompress(z)==data: return z
    return None
