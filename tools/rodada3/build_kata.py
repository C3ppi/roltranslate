import sys,json,re
sys.path.insert(0,'/home/claude/rt/work')
from words import seg
OV={'カッパーリング':'Copper Ring','サンラーリ':'Sanrari','フリースタイル':'Freestyle','ブレイズカイリー':'Blaze Kairi','ミミングスソード':"Miming's Sword",'アーロンズロッド':"Aaron's Rod",'ナーゲルリング':'Nagel Ring','レイシェ':'Reishe','プラクティス':'Practice','ベル':'Bell','バンコンバット':'Bancombat','アポリオン ':'Apollyon','シャタグニー ':'Shataguni','カトヤンガ':'Katoyanga','クラスチェンジ':'Class Change','ゼメア':'Zemea','リアンツ':'Riantz','ブローヴァ':'Brova','ダークネスライザー':'Darkness Riser','ヘリシュナイトメア':'Herishu Nightmare','ソードマスター':'Swd Master','ティノ':'Tino','ベース':'Base','ルナン':'Runan','レザーガントレ':'Lthr Gauntlet','ラメラーガントレ':'Lamel. Gauntlet','プラチナガントレ':'Plat. Gauntlet','レザーブーツ':'Lthr Boots','レザーグリーヴ':'Lthr Greaves','アジト':'Lair','レザーグローブ':'Lthr Gloves','キラーブーツ':'Killer Bt','ローズグローブ':'Rose Glove','キラーグローブ':'Killer Glove','キラーブーツ':'Killer Boot','ペンダント':'Pendnt','アルケミスト':'Alchemst','スペルカウンター':'Spell Cntr','ドレインガード':'Drain Grd','ホーリーアロー':'HolyArrow','ヒヒイロカネ':'Hihiiro','アビスターナ':'Abistana'}
def build():
    d=json.load(open('/home/claude/rt/work/remaining.json'))
    kata=re.compile(r'^[゠-ヿー・　 ]+$')
    tmap={}
    for s in d:
        if kata.match(s):
            t=OV.get(s) or seg(s); raw=s.encode('cp932')
            if t and len(t)<=len(raw): tmap[raw]=t.encode()
    return tmap
if __name__=='__main__':
    from crpatch import apply
    tm=build()
    st,used=apply('/home/claude/rt/work/a_fixed.cr','/home/claude/rt/work/a_step1.cr',tm)
    print(st,len(tm))
