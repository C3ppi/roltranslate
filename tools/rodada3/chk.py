import sys,json,importlib.util,textwrap
def enc_ok(f):
    try: f.encode('cp932'); return all(ord(c)<128 or c in '←→↑↓±' for c in f)
    except Exception: return False
def load(f):
    s=importlib.util.spec_from_file_location('m',f); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m.T
def fmt(t,orig,width=None):
    if width is None:
        mx=max(len(l.encode('cp932')) for l in orig.split('\n'))
        width=max(30,min(mx,56)-2)
    if '%' in t:
        return t.replace('||','\n\n')
    if '||' in t or '\n' in t or len(t)>width:
        paras=t.split('||'); out=[]
        for p in paras:
            lines=[]
            for ln in p.split('\n'):
                lines.append('\n'.join(textwrap.wrap(ln,width)) if ln else '')
            out.append('\n'.join(lines))
        return '\n\n'.join(out)
    return t
if __name__=='__main__':
    todo=json.load(open('/home/claude/rt/work/todo.json'))
    T={}
    for a in sys.argv[1:]: T.update(load(a))
    bad=0
    for i,t in sorted(T.items()):
        o=todo[i]; budget=len(o.encode('cp932'))
        f=fmt(t,o)
        if not enc_ok(f) or len(f.encode('cp932','replace'))>budget:
            bad+=1; print('OVER',i,len(f),budget,t[:60])
    print('checked',len(T),'over',bad)
