import sys,struct,json,os,shutil; sys.path.insert(0,'/home/claude/rt/work')
from lib import blocks
from crpatch import recompress
def jpfields(d):
    r=[]
    for i in range(0,len(d)-5):
        L=struct.unpack_from('<I',d,i)[0]
        if 2<=L<=400 and i+4+L<=len(d) and d[i+4+L-1]==0:
            raw=d[i+4:i+4+L-1]
            if raw and b'\0' not in raw and any(x>127 for x in raw):
                try: raw.decode('cp932'); r.append((i,L))
                except: pass
    return r
def fixblock(orig,new):
    nd=bytearray(new); n=0
    for i,L in jpfields(orig):
        reg=bytes(nd[i+4:i+4+L-1])
        if reg==orig[i+4:i+4+L-1]: continue
        t=reg.rstrip(b'\0')
        if t and b'\0' not in t and len(t)<L-1 and all(32<=x<127 or x in(10,) for x in t):
            nd[i+4:i+4+L-1]=t.ljust(L-1,b' '); n+=1
    return bytes(nd),n
