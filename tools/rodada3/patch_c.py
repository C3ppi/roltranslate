import sys,re,struct,zlib
sys.path.insert(0,'/home/claude/rt/work')
from lib import blocks
from crpatch import recompress
SRC='/home/claude/rt/repo/game/rol/cr/c.cr'; OUT='/home/claude/rt/work/c_step.cr'
M={'魔徒再臨':'Demon Return','百人組手：ゴブリン':'100-Fight: Goblin','骨の軍団':'Bone Legion','風雲一派':'Wind Clan','太古の亡霊':'Ancient Ghost','百人組手：サハギンプリンス':'100-Fight: Sahagin Prince','伝説の大蛇':'Legend Serpent','雪原の竜':'Snow Dragon'}
D=bytearray(open(SRC,'rb').read())
start=16+struct.unpack_from('<I',D,12)[0]
n=0;fail=0
for o,c,data in blocks(bytes(D),start):
    nd=data
    for jp,en in M.items():
        a=('<msml name="'+jp+'"').encode(); b=('<msml name="'+en+'"').encode()
        if a in nd:
            pad=len(a)-len(b); assert pad>=0
            nd=nd.replace(a,b+b' '*pad)
    if nd!=data:
        assert len(nd)==len(data)
        z=recompress(nd,c)
        if z is None: fail+=1; print('fail',hex(o)); continue
        D[o:o+c]=z+b'\x00'*(c-len(z)); n+=1
open(OUT,'wb').write(D)
print('patched blocks',n,'fail',fail)
