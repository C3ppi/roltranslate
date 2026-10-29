import sys,json,glob
sys.path.insert(0,'/home/claude/rt/work')
import chk
from build_kata import build as build_kata
from crpatch import apply
import importlib
FB=chk.load('/home/claude/rt/work/tr/fallback.py')
FB={k:[x.encode('cp932') for x in v] for k,v in FB.items()}
todo=json.load(open('/home/claude/rt/work/todo.json'))
files=['b000','b000f','b150','b150f','b150g','b150h','b300','b450','b600','b600f','b760','b760f','b910','b910f','b1060','b1060f','b1200','b1350']
T={}
for f in files:
    T.update(chk.load(f'/home/claude/rt/work/tr/{f}.py'))
tmap=build_kata()
tmap['キラーブーツ'.encode('cp932')]=[x.encode() for x in ['Killer Bt','KillerBt','Kilr Bt','Boots']]
tmap={k:(v if isinstance(v,list) else [v]) for k,v in tmap.items()}
n=0
for i,t in T.items():
    o=todo[i]; f=chk.fmt(t,o)
    assert chk.enc_ok(f),(i,t)
    b=f.encode('cp932'); k=o.encode('cp932')
    assert len(b)<=len(k),(i,t)
    tmap[k]=[b]+FB.get(i,[]); n+=1
print('manual',n,'total',len(tmap),'untranslated todo',len(todo)-n)
if __name__=='__main__':
    st,used=apply('/home/claude/rt/work/a_fixed.cr','/home/claude/rt/work/a_step2.cr',tmap)
    print(st)
    json.dump(sorted(x.decode('cp932') for x in used),open('/home/claude/rt/work/used.json','w'),ensure_ascii=False)
