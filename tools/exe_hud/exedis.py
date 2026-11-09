import pefile,struct,sys,re
from capstone import *
pe=pefile.PE('/home/claude/rt/repo/game/rol/rol.exe'); data=open('/home/claude/rt/repo/game/rol/rol.exe','rb').read()
base=pe.OPTIONAL_HEADER.ImageBase
def off2va(o):
    for s in pe.sections:
        if s.PointerToRawData<=o<s.PointerToRawData+s.SizeOfRawData: return base+s.VirtualAddress+o-s.PointerToRawData
def va2off(v): return pe.get_offset_from_rva(v-base)
text=[s for s in pe.sections if s.Name.startswith(b'.text')][0]
tb=text.PointerToRawData; ts=text.SizeOfRawData; tva=base+text.VirtualAddress
def xrefs(va):
    p=struct.pack('<I',va); out=[];i=tb
    while True:
        i=data.find(p,i,tb+ts)
        if i<0: break
        out.append(tva+i-tb); i+=1
    return out
def strva(s):
    r=[];i=0
    while True:
        i=data.find(b'\0'+s+b'\0',i)
        if i<0: break
        r.append(off2va(i+1)); i+=1
    return r
md=Cs(CS_ARCH_X86,CS_MODE_32)
def dis(va,n=40,back=0):
    o=va2off(va-back); 
    for ins in md.disasm(data[o:o+n*8],va-back):
        print(hex(ins.address),ins.mnemonic,ins.op_str); n-=1
        if n<=0: break
if __name__=='__main__':
    for s in sys.argv[1:]:
        for v in strva(s.encode()):
            print(s,hex(v),[hex(x) for x in xrefs(v)])
