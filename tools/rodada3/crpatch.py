import sys,struct,zlib,csv,json
sys.path.insert(0,'/home/claude/rt/work')
from lib import blocks

def recompress(data, clen):
    best=None
    for lv in (9,6,1,0):
        z=zlib.compress(data,lv)
        if len(z)<=clen and (best is None or len(z)<len(best)): best=z
    if best is None:
        try:
            import zopfli.zlib as zz
            for it in (15,50,200):
                z=zz.compress(data,numiterations=it)
                if len(z)<=clen and (best is None or len(z)<len(best)): best=z
        except Exception: pass
    if best is not None: assert zlib.decompress(best)==data
    return best

def patch_fields(data, tmap):
    """replace u32-len-prefixed NUL-terminated cp932 fields; keep length prefix, NUL pad."""
    b=bytearray(data); n=len(b); i=0; changed=[]
    while i+5<=n:
        L=struct.unpack_from('<I',b,i)[0]
        if 2<=L<=2000 and i+4+L<=n and b[i+4+L-1]==0:
            raw=bytes(b[i+4:i+4+L-1])
            if raw in tmap:
                t=tmap[raw]
                if len(t)<=L-1:
                    b[i+4:i+4+L]=t+b'\x00'*(L-len(t))
                    changed.append(raw); i+=4+L; continue
        i+=1
    return bytes(b),changed

def edits(data,tmap):
    out=[];n=len(data);i=0
    while i+5<=n:
        L=struct.unpack_from('<I',data,i)[0]
        if 2<=L<=2000 and i+4+L<=n and data[i+4+L-1]==0:
            raw=bytes(data[i+4:i+4+L-1])
            if raw in tmap:
                c=tmap[raw]; c=c if isinstance(c,list) else [c]
                c=[x for x in c if len(x)<=L-1]
                if c:
                    out.append((i,L,raw,c)); i+=4+L; continue
        i+=1
    return out

def apply(path_in, path_out, tmap):
    D=bytearray(open(path_in,'rb').read())
    stats={'blocks':0,'fields':0,'fail':0}
    used=set()
    for o,c,data in blocks(bytes(D)):
        ed=edits(data,tmap)
        if not ed: continue
        nd=bytearray(data); z=None; done=[]
        def mk(buf,e,k=None):
            i,L,raw,cands=e; t=cands[0] if k is None else cands[k]; b=bytearray(buf); b[i+4:i+4+L]=t+b'\x00'*(L-len(t)); return b
        z=None
        maxk=max(len(e[3]) for e in ed)
        for k in range(maxk):
            full=data
            for e in ed: full=mk(full,e,min(k,len(e[3])-1))
            z=recompress(bytes(full),c)
            if z is not None:
                nd=full; done=ed; break
        if z is None:
            cur=bytearray(data); zc=None
            for e in ed:
                ok=False
                for k in range(len(e[3])):
                    trial=mk(cur,e,k); zt=recompress(bytes(trial),c)
                    if zt is not None: cur=trial; zc=zt; done.append(e); ok=True; break
                if not ok: stats['fail']+=1; stats.setdefault('failed',[]).append(e[2].decode('cp932'))
            z=zc; nd=cur
        if z is None: continue
        D[o:o+c]=z+b'\x00'*(c-len(z))
        stats['blocks']+=1; stats['fields']+=len(done); used.update(e[2] for e in done)
    open(path_out,'wb').write(D)
    return stats,used
