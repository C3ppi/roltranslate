import sys,json,time,os; sys.path.insert(0,'/home/claude/rt/work'); os.chdir('/home/claude/rt/work')
from lib import blocks
from exact2 import exact
O=open('/home/claude/rt/repo/game/rol/cr/a.cr.codex-original.bak','rb').read()
ol=blocks(O); ob={o:c for o,c,d in ol}; O_d={o:d for o,c,d in ol}
P=open('grp9/P1_tudo_prefixos_preservados/a.cr','rb').read()
mod=[(o,d) for o,c,d in blocks(P) if d!=O_d[o]]
res={}; bad=[]
t=time.time()
for o,d in mod:
    z=exact(d,ob[o],tries=4000)
    if z: res[o]=z
    else: bad.append(o)
print(len(res),len(bad),time.time()-t)
import pickle; pickle.dump((res,bad),open('exact_res.pkl','wb'))
