import sys,struct;sys.path.insert(0,'/home/claude/rt/work')
from unicorn import *; from unicorn.x86_const import *
import build_exe as B
mu=Uc(UC_ARCH_X86,UC_MODE_32)
mu.mem_map(B.NEW_VA,len(B.blob)); mu.mem_write(B.NEW_VA,B.blob)
mu.mem_map(0x10000,0x10000); mu.mem_map(0x5248000&~0xfff,0x2000)  # dummy for RET target
mu.mem_map(0x7f0000,0x10000)
def run(name):
    p=0x10100; mu.mem_write(p,name+b'\0'); mu.mem_write(0x10000,struct.pack('<I',p))
    sp=0x7f8000; mu.reg_write(UC_X86_REG_ESP,sp); mu.reg_write(UC_X86_REG_ECX,0x10000)
    for r,v in ((UC_X86_REG_EBX,0xb1),(UC_X86_REG_EDX,0xd1),(UC_X86_REG_ESI,0x51),(UC_X86_REG_EDI,0xd7)): mu.reg_write(r,v)
    mu.emu_start(B.NEW_VA,B.RET,count=100000)
    esp=mu.reg_read(UC_X86_REG_ESP); ptr=struct.unpack('<I',bytes(mu.mem_read(esp,4)))[0]; eax=mu.reg_read(UC_X86_REG_EAX)
    out=bytes(mu.mem_read(ptr,80)).split(b'\0')[0]
    regs=[mu.reg_read(r) for r in (UC_X86_REG_EBX,UC_X86_REG_EDX,UC_X86_REG_ESI,UC_X86_REG_EDI)]
    return out,(esp==sp-4, eax==sp-4+0x1c)+tuple(regs)
for n in ['スライム','サイドワインダー','サイドワインダーNM','魔人：剣士I','ゴブリン','Allen','ミノタウロス','ゴブリンチーフ','未知の敵']:
    for enc in ('cp932','utf8'):
        try: b=n.encode(enc)
        except: continue
        print(n,enc,run(b))
