import sys,struct,hashlib; sys.path.insert(0,'/home/claude/rt/work')
from keystone import Ks,KS_ARCH_X86,KS_MODE_32
from names_tr import D
SRC='/home/claude/rt/repo/game/rol/rol.exe'
data=bytearray(open(SRC,'rb').read())
IB=0x400000; NEW_RVA=0x6fe000; NEW_VA=IB+NEW_RVA
BUFSZ=0x100
HOOK=0x5248c6; RET=0x5248cd
# --- table
ents=[]
for jp,en in D.items():
    if len(en)>40: en=en[:40]
    en=en.encode('ascii')
    for enc in ('cp932','utf8'):
        try: k=jp.encode(enc)
        except Exception: continue
        if 0<len(k)<250: ents.append((k,en))
seen=set();tab=[]
for k,en in sorted(ents,key=lambda x:-len(x[0])):
    if (k,en) in seen: continue
    seen.add((k,en)); tab.append((k,en))
table=b''.join(bytes([len(k)])+k+bytes([len(en)])+en for k,en in tab)+b'\x00'
# --- code
def build(code_len_guess=0x200):
    BUF=NEW_VA+code_len_guess; TABLE=BUF+BUFSZ
    asm=f'''
tramp:
    mov eax,[ecx]
    call xlat
    push eax
    lea eax,[esp+0x1c]
    jmp {RET}
xlat:
    push ebx
    push ecx
    push edx
    push esi
    push edi
    mov esi,{TABLE}
    mov edi,eax
next:
    movzx ecx,byte ptr [esi]
    test ecx,ecx
    jz notfound
    lea ebx,[esi+1]
    mov edx,edi
cmpl:
    mov al,[ebx]
    cmp al,[edx]
    jne nomatch
    inc ebx
    inc edx
    dec ecx
    jnz cmpl
    movzx eax,byte ptr [edx]
    cmp al,0x80
    jae nomatch
    jmp matched
nomatch:
    movzx ecx,byte ptr [esi]
    lea esi,[esi+ecx+1]
    movzx ecx,byte ptr [esi]
    lea esi,[esi+ecx+1]
    jmp next
matched:
    movzx ecx,byte ptr [ebx]
    inc ebx
    mov esi,{BUF}
copyen:
    test ecx,ecx
    jz endcopy
    mov al,[ebx]
    mov [esi],al
    inc ebx
    inc esi
    dec ecx
    jmp copyen
endcopy:
    mov al,[edx]
    cmp al,0x30
    jb copyrest
    cmp al,0x39
    jbe addsp
    cmp al,0x41
    jb copyrest
    cmp al,0x5a
    jbe addsp
    cmp al,0x61
    jb copyrest
    cmp al,0x7a
    ja copyrest
addsp:
    mov byte ptr [esi],0x20
    inc esi
copyrest:
    mov ecx,40
cr:
    mov al,[edx]
    mov [esi],al
    test al,al
    jz fin
    inc esi
    inc edx
    dec ecx
    jnz cr
    mov byte ptr [esi],0
fin:
    mov eax,{BUF}
    jmp out
notfound:
    mov eax,edi
out:
    pop edi
    pop esi
    pop edx
    pop ecx
    pop ebx
    ret
'''
    ks=Ks(KS_ARCH_X86,KS_MODE_32)
    enc,_=ks.asm(asm,NEW_VA)
    return bytes(enc),BUF,TABLE
code,BUF,TABLE=build(0x200)
assert len(code)<=0x200,len(code)
code=code.ljust(0x200,b'\xcc')
tramp_va=NEW_VA
# --- section blob
blob=code+b'\0'*BUFSZ+table
raw=(len(blob)+0xfff)//0x1000*0x1000
blob=blob.ljust(raw,b'\0')
if __name__=='__main__':
    # jump at hook
    ho=HOOK-IB-0x1000+0x1000  # .text RVA 0x1000 raw 0x1000 -> offset == RVA
    assert data[ho:ho+7]==bytes.fromhex('8b0150 8d44241c'.replace(' ','')),data[ho:ho+7].hex()
    jmp=b'\xe9'+struct.pack('<i',tramp_va-(HOOK+5))+b'\x90\x90'
    data[ho:ho+7]=jmp
    # headers
    pe=struct.unpack_from('<I',data,0x3c)[0]
    nsec=struct.unpack_from('<H',data,pe+6)[0]; opt=struct.unpack_from('<H',data,pe+20)[0]
    sh=pe+24+opt+nsec*40
    assert data[sh:sh+40]==b'\0'*40
    fileend=len(data)
    assert fileend%0x1000==0
    vsize=len(blob)
    data[sh:sh+40]=b'.trad\0\0\0'+struct.pack('<IIIIIIHHI',vsize,NEW_RVA,raw,fileend,0,0,0,0,0xE0000060)
    struct.pack_into('<H',data,pe+6,nsec+1)
    soi=pe+24+56; struct.pack_into('<I',data,soi,NEW_RVA+(vsize+0xfff)//0x1000*0x1000)
    data+=blob
    out='/home/claude/rt/work/rol_hud.exe'; open(out,'wb').write(data)
    print('written',out,len(data),'table entries',len(tab),'code',len(code),hashlib.md5(data).hexdigest())
