import sys,struct,zlib; sys.path.insert(0,'/home/claude/rt/work')
from lib import blocks
from crpatch import recompress
def fields(d):
    r={};i=0;n=len(d)
    while i+5<=n:
        L=struct.unpack_from('<I',d,i)[0]
        if 2<=L<=2000 and i+4+L<=n and d[i+4+L-1]==0:
            r[i]=(L,d[i+4:i+4+L-1]); i+=4+L
        else: i+=1
    return r
def convert(orig_path,patched_path,out_path,only=None):
    O=open(orig_path,'rb').read(); P=open(patched_path,'rb').read(); D=bytearray(P)
    ob=blocks(O); pb={o:d for o,c,d in blocks(P)}
    offs=[o for o,c,d in ob]; end={o:(offs[i+1] if i+1<len(offs) else len(O)) for i,o in enumerate(offs)}
    st={'blocks':0,'fields':0,'fail':[]}
    for o,c,d in ob:
        p=pb[o]
        if p==d: continue
        if only is not None and o not in only: continue
        fo=fields(d); fp=fields(p); cand=[]
        for i,(L,raw) in fp.items():
            if i in fo and fo[i][0]==L and fo[i][1]!=raw:
                s=raw.rstrip(b'\0')
                if s and len(s)<L-1 and b'\0' not in s and all(x<128 for x in s):
                    cand.append((i,L,s))
        if not cand: continue
        # base: patched block with all candidate fields reverted to original
        cur=bytearray(p)
        for i,L,s in cand: cur[i+4:i+4+L-1]=fo[i][1]
        zc=recompress(bytes(cur),c); done=0
        for i,L,s in cand:
            t=bytearray(cur); t[i+4:i+4+L-1]=s.ljust(L-1,b' ')
            z=recompress(bytes(t),c)
            if z is not None: cur=t; zc=z; done+=1
            else: st['fail'].append((o,i,s.decode()))
        if zc is None: st['fail'].append((o,'blk')); continue
        D[o:end[o]]=zc+b'\0'*(end[o]-o-len(zc))
        st['blocks']+=1; st['fields']+=done
    open(out_path,'wb').write(D); return st
if __name__=='__main__':
    print(convert(*sys.argv[1:4]))
