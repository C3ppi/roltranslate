import sys,re,pickle,zlib; sys.path.insert(0,'/home/claude/rt/work')
from lib import blocks
from nameconv import tr
K=open('/home/claude/rt/repo/game/rol/cr/a.cr','rb').read()
B=blocks(K)
PAT=re.compile(rb'(?<=[ \t])name="([^"]*(?:[\xe3-\xe9][\x80-\xbf][\x80-\xbf])[^"]*)"')
out={}
bad=0
for o,c,d in B:
    if not PAT.search(d): continue
    def rep(m):
        global bad
        old=m.group(0); n=m.group(1).decode('utf8')
        e=tr(n)
        if e is None: bad+=1; return old
        budget=len(m.group(1))
        if len(e)>budget:
            from fixL import variants
            vs=variants(e.encode('ascii'),budget)
            e=vs[0].decode() if vs else None
            if e is None: bad+=1; print('NOFIT',n); return old
        new=b'name="'+e.encode('ascii')+b'"'
        k=len(old)-len(new)
        assert k>=0,(n,e)
        return new+b' '*k
    nd=PAT.sub(rep,d)
    assert len(nd)==len(d)
    out[o]=(c,d,nd)
print(len(out),'blocks, bad',bad)
pickle.dump(out,open('k3prep.pkl','wb'))
for o,(c,d,nd) in list(out.items())[:8]:
    print(o,c,len(d),len(zlib.compress(nd,9))+0)
