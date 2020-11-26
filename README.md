# LegoMS
B3ST 知能ロボット演習のLegoMS演習

## 概要
LEGO Mindstorms EV3の演習で使用したプログラムソース

## Link
[講義ページ](https://www.katolab.nitech.ac.jp/lecture/intelli-robot/lego/index.html)

[ルール一覧](https://www.katolab.nitech.ac.jp/lecture/intelli-robot/lego/rule2016/)

## main
**リリース版** 全てのコースを突破可能（なはず）

## feature
**beta版** 爆速化max250で突破可能（なはず）

## develop
さらに爆速化max300したが、どこをどうしたのか訳わからなくなったので無視．

## develop_2
新developブランチ．
問題点は以下．

0. **[センサの閾値が決まらない問題]** センサの値をprintしてログして検討
1. **[カーブで行きすぎる問題]**
    mainのwhileのwaitを短く→ カーブ制御（）の中身にあるwaitを短く
2. **[異常値で全部白を迎えると角度を換えられる問題]**
    1) detect_blackのなかで二度センサ値を確かめる処理
    2) if(last_detected == L(orR))の後のrobot_driveをwhile(!L&!C&!R)で包む
3. **[何らかの原因で斜めに十字路に差し掛かった時に終了条件を満たせず直進し続けてしまう]**
    1) 十字路だったときの条件をCのセンサだけに緩和 & 左右にずれたときの角度調整もする（!C&Rを検知してたらspeed0で左に振る、!C&Lを検知してたら右に振る、複数回試行してダメだったらflag立てて終了？）
    2) スピードをtake_careに落とす

99. **[到着時の音楽が一生決まらない問題]** 助けてください．