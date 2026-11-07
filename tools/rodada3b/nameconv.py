import re
from names_tr import D
KEYS=sorted(D,key=len,reverse=True)
LV=re.compile(r'^(.*?)(\s*(?:Lv|LV|lv)\s*\d+.*)$')
def tr(n):
    lv=''
    m=LV.match(n)
    if m:
        n,lv=m.group(1),m.group(2)
        for a,b in (('取り巻き','Aide'),('ラスボス','FinalBoss'),('中ボス','MidBoss'),('ボス','Boss')): lv=lv.replace(a,b)
    pre=''
    if n[:1] in 'sx' and n[1:] and ord(n[1])>127: pre=n[0]; n=n[1:]
    best=None
    for k in KEYS:
        if n.startswith(k):
            rest=n[len(k):]
            if all(ord(c)<128 for c in rest):
                best=(k,rest);break
            # allow JP suffix in D too
            for k2 in KEYS:
                if rest==k2 or (rest.startswith(k2) and all(ord(c)<128 for c in rest[len(k2):])): best=(k,rest);break
            if best:break
    if not best: return None
    k,rest=best
    out=D[k]
    if rest:
        if rest[0].isascii():
            sfx=rest
        else:
            sfx=rest
            for k2 in KEYS:
                if rest.startswith(k2): sfx=D[k2]+rest[len(k2):];break
        out=out+('' if sfx.startswith((' ','(')) else ' ')+sfx
    return (pre+out if pre else out)+lv
