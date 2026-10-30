import zlib, struct, re
def load(path):
    return open(path,'rb').read()
def blocks(d, start=0x2a600):
    n=len(d); i=start; out=[]
    while i<n-2:
        if d[i]==0x78 and d[i+1] in (0x9c,0xda,0x01,0x5e):
            try:
                o=zlib.decompressobj(); data=o.decompress(d[i:])
                if o.eof:
                    clen=(n-i)-len(o.unused_data)
                    out.append((i,clen,data)); i+=clen; continue
            except Exception: pass
        i+=1
    return out
def has_jp(b):
    try: s=b.decode('cp932')
    except: return False
    return any('぀'<=c<='ヿ' or '一'<=c<='鿿' or '＀'<=c<='￯' for c in s)
