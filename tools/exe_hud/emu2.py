import struct,pefile
from unicorn import *; from unicorn.x86_const import *
d=open('rol_hud.exe','rb').read(); pe=pefile.PE(data=d)
mu=Uc(UC_ARCH_X86,UC_MODE_32)
mu.mem_map(0x400000,0x704000)
for s in pe.sections:
    mu.mem_write(0x400000+s.VirtualAddress,d[s.PointerToRawData:s.PointerToRawData+s.SizeOfRawData])
mu.mem_write(0x400000,d[:0x1000])
mu.mem_map(0x2000000,0x20000); mu.mem_map(0x2100000,0x2100000)
def run(name,lv=b'3'):
    mu.mem_write(0x2100100,name+b'\0'); mu.mem_write(0x2100000,struct.pack('<I',0x2100100))
    sp=0x2008000; mu.reg_write(UC_X86_REG_ESP,sp)
    mu.mem_write(sp+0x90,struct.pack('<I',0x2100000)); mu.mem_write(sp+0x8c,b'\x01\0\0\0')
    mu.mem_write(0x2100200,lv+b'\0')
    cap={}
    def hk(uc,addr,size,ud):
        esp=uc.reg_read(UC_X86_REG_ESP)
        buf,fmt,a1,a2=struct.unpack('<4I',bytes(uc.mem_read(esp+4,16)))
        def cs(p): return bytes(uc.mem_read(p,64)).split(b'\0')[0]
        cap['fmt']=cs(fmt); cap['name']=cs(a1); cap['lv']=cs(a2); cap['esp']=esp
        uc.emu_stop()
    h=mu.hook_add(UC_HOOK_CODE,hk,None,0x7d0350,0x7d0350)
    mu.emu_start(0x5248ba,0x7d0350+0x100,count=500000)
    mu.hook_del(h); return cap
for n in ['スライム'.encode('cp932'),'サイドワインダー Lv1'.encode('cp932'),b'Allen','ゴブリンNM'.encode('utf8')]:
    print(run(n))
