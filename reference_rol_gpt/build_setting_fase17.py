import zipfile,struct,pathlib,hashlib,json,csv
P=pathlib.Path('/mnt/data'); O=P/'rol_setting_fase17';O.mkdir(exist_ok=True)
with zipfile.ZipFile(P/'rol-20261021T232919Z-1-001.zip') as z: data=bytearray(z.read('rol/setting.exe'))
pe=struct.unpack_from('<I',data,0x3c)[0]; opt=pe+24; n=struct.unpack_from('<H',data,pe+6)[0];sz=struct.unpack_from('<H',data,pe+20)[0];sec=opt+sz
align=lambda x,a:(x+a-1)//a*a
sections=[]
for i in range(n):
 q=sec+40*i;sections.append(dict(q=q,name=data[q:q+8].rstrip(b'\0').decode('ascii'),vs=struct.unpack_from('<I',data,q+8)[0],va=struct.unpack_from('<I',data,q+12)[0],raw=struct.unpack_from('<I',data,q+16)[0],ptr=struct.unpack_from('<I',data,q+20)[0]))
rs=next(s for s in sections if s['name']=='.rsrc'); base=rs['ptr']; rvabase=rs['va']
# enumerate PE resource tree: directory -> type -> name -> language -> data entry
entries=[]
def walk(rel,level,path):
 pos=base+rel; cnt=struct.unpack_from('<HH',data,pos+12);total=sum(cnt)
 for i in range(total):
  q=pos+16+i*8; name,off=struct.unpack_from('<II',data,q)
  key=name if name<0x80000000 else 'string'
  if off&0x80000000:walk(off&0x7fffffff,level+1,path+[key])
  else:
   de=base+off;rva,size=struct.unpack_from('<II',data,de);entries.append((path+[key],de,rva,size))
walk(0,0,[])
rows=list(csv.DictReader(open(P/'rol_setting_fase12/recursos.csv',encoding='utf-8-sig')))
new_va=align(max(s['va']+align(s['vs'],0x1000) for s in sections),0x1000)
new_ptr=align(len(data),0x1000);blob=bytearray();changes=[]
for r in rows:
 if r['tipo']!='5':continue
 original_offset=int(r['offset']);orig_size=int(r['tamanho']);match=[e for e in entries if e[0]==[5,int(r['id']),1041] and e[3]==orig_size and (e[2]-rvabase+base)==original_offset]
 if len(match)!=1:raise RuntimeError(f'not unique resource {r} {match}')
 translated=(P/'rol_setting_fase16'/f'dialog_{r["id"]}_ptbr.bin').read_bytes()
 blob+=b'\0'*(align(len(blob),4)-len(blob));offset=len(blob);blob+=translated
 _,de,_,_=match[0];struct.pack_into('<II',data,de,new_va+offset,len(translated))
 changes.append({'id':r['id'],'old_size':orig_size,'new_size':len(translated),'new_rva':new_va+offset,'sha256':hashlib.sha256(translated).hexdigest()})
new_raw=align(len(blob),0x1000)
assert sec+40*(n+1)<min(s['ptr'] for s in sections)
if len(data)<new_ptr:data+=b'\0'*(new_ptr-len(data))
data+=blob+b'\0'*(new_raw-len(blob))
q=sec+40*n;data[q:q+8]=b'.ptbr\0\0\0';struct.pack_into('<IIIIIIHHI',data,q+8,len(blob),new_va,new_raw,new_ptr,0,0,0,0,0x40000040)
struct.pack_into('<H',data,pe+6,n+1);struct.pack_into('<I',data,opt+56,align(new_va+len(blob),0x1000))
# PE checksum not essential, zero stale checksum
struct.pack_into('<I',data,opt+64,0)
exe=O/'setting_PTBR_fase17.exe';exe.write_bytes(data)
# verify all changed entries now point to exact blobs
for change in changes:
 found=[e for e in entries if e[0]==[5,int(change['id']),1041]]
 assert len(found)==1
 _,de,_,_=found[0];rva,size=struct.unpack_from('<II',data,de)
 assert rva==change['new_rva'] and size==change['new_size']
 assert hashlib.sha256(data[new_ptr+rva-new_va:new_ptr+rva-new_va+size]).hexdigest()==change['sha256']
(O/'validacao.json').write_text(json.dumps({'resources':changes,'original_sha256':hashlib.sha256(bytes(zipfile.ZipFile(P/'rol-20261021T232919Z-1-001.zip').read('rol/setting.exe'))).hexdigest(),'patched_sha256':hashlib.sha256(data).hexdigest(),'windows_execution_tested':False},indent=2),encoding='utf-8')
print('ok',len(data),len(changes),len(blob),exe)
