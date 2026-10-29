import re
B={'ア':'a','イ':'i','ウ':'u','エ':'e','オ':'o','カ':'ka','キ':'ki','ク':'ku','ケ':'ke','コ':'ko','サ':'sa','シ':'shi','ス':'su','セ':'se','ソ':'so','タ':'ta','チ':'chi','ツ':'tsu','テ':'te','ト':'to','ナ':'na','ニ':'ni','ヌ':'nu','ネ':'ne','ノ':'no','ハ':'ha','ヒ':'hi','フ':'fu','ヘ':'he','ホ':'ho','マ':'ma','ミ':'mi','ム':'mu','メ':'me','モ':'mo','ヤ':'ya','ユ':'yu','ヨ':'yo','ラ':'ra','リ':'ri','ル':'ru','レ':'re','ロ':'ro','ワ':'wa','ヲ':'o','ン':'n','ガ':'ga','ギ':'gi','グ':'gu','ゲ':'ge','ゴ':'go','ザ':'za','ジ':'ji','ズ':'zu','ゼ':'ze','ゾ':'zo','ダ':'da','ヂ':'ji','ヅ':'zu','デ':'de','ド':'do','バ':'ba','ビ':'bi','ブ':'bu','ベ':'be','ボ':'bo','パ':'pa','ピ':'pi','プ':'pu','ペ':'pe','ポ':'po','ヴ':'vu','・':' ','　':' ',' ':' '}
SM={'ァ':'a','ィ':'i','ゥ':'u','ェ':'e','ォ':'o'}
YO={'ャ':'ya','ュ':'yu','ョ':'yo'}
def conv(s):
    out=[];i=0;dbl=False
    while i<len(s):
        c=s[i]
        if c=='ッ': dbl=True; i+=1; continue
        if c=='ー':
            i+=1; continue
        base=B.get(c)
        if base is None: return None
        nx=s[i+1] if i+1<len(s) else ''
        if nx in YO and c in 'キシチニヒミリギジビピ':
            pre={'シ':'sh','チ':'ch','ジ':'j'}.get(c)
            if pre: base=pre+YO[nx][1:]
            else: base=base[:-1]+YO[nx]
            i+=1
        elif nx in SM:
            v=SM[nx]
            if c=='ウ' and v!='u': base='w'+v
            elif c=='ヴ': base='v'+v
            elif c in 'フ': base='f'+v
            elif c=='シ': base='she' if v=='e' else 'sh'+v
            elif c=='ジ': base='je' if v=='e' else 'j'+v
            elif c=='チ': base='che' if v=='e' else 'ch'+v
            elif c=='テ' and v=='i': base='ti'
            elif c=='デ' and v=='i': base='di'
            elif c=='ツ': base='ts'+v
            else: base=base[:-1]+v if base[-1] in 'aiueo' else base+v
            i+=1
        if dbl and base[0] not in 'aiueo': base=base[0]+base
        dbl=False
        out.append(base); i+=1
    r=''.join(out)
    return ' '.join(w.capitalize() for w in r.split(' '))
if __name__=='__main__':
    for t in ['クラニィ','ゴブリンガード','ヴェーロ','シュナイン','ルカロッタ','ジェトゥ','スカルフェンサー','ファロガ','ディトマン','ハンター']: print(t,conv(t))
