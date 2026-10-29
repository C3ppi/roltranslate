import sys,struct,collections,json; sys.path.insert(0,'.')
from lib import *
def jp(s): return any('぀'<=ch<='ヿ' or '一'<=ch<='鿿' or '！'<=ch<='ﾟ' for ch in s)
def fields(data):
    """yield (off, L, text) for u32-len-prefixed NUL-terminated cp932 strings containing JP"""
    n=len(data); i=0
    while i+5<=n:
        L=struct.unpack_from('<I',data,i)[0]
        if 2<=L<=2000 and i+4+L<=n and data[i+4+L-1]==0:
            raw=data[i+4:i+4+L-1]
            if b'\x00' not in raw and any(b>=0x80 for b in raw):
                try:
                    s=raw.decode('cp932')
                    if jp(s): yield i,L,s,raw
                except: pass
        i+=1
if __name__=='__main__':
    R='/home/claude/rt/repo/'
    bl=blocks(load('a_fixed.cr'))
    cnt=collections.Counter(); first={}
    for k,(o,c,data) in enumerate(bl):
        seen=set()
        for off,L,s,raw in fields(data):
            # skip overlapping (a shorter string inside longer one)
            cnt[s]+=1; first.setdefault(s,(k,o,off,L))
    print('distinct',len(cnt),'occ',sum(cnt.values()))
    json.dump({s:[cnt[s],*first[s]] for s in cnt},open('remaining.json','w'),ensure_ascii=False)
    import itertools
    for s,n in cnt.most_common(60): print(n,repr(s))
