import zlib,struct,random
import zopfli.zlib as zz
def shift(raw,k):
    if k==0: return raw
    v=int.from_bytes(raw,'little')<<(10*k)
    for j in range(k): v|=2<<(10*j)
    nb=(v.bit_length()+7)//8
    return v.to_bytes(nb,'little')
def exact_zop(data,clen,iters=(3,10,30,100)):
    ad=struct.pack('>I',zlib.adler32(data)&0xffffffff)
    for it in iters:
        z=zz.compress(data,numiterations=it); raw=z[2:-4]
        for k in range(0,14):
            r=shift(raw,k)
            if len(r)+6==clen:
                out=b'\x78\x9c'+r+ad
                try:
                    if zlib.decompress(out)==data: return out
                except Exception: pass
            if len(r)+6>clen: break
    return None
