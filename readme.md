# 概要
いろいろ使えるGrepReplaceツールです。対象ディレクトリ以下の全ファイルを検索 → 処理を実施します。  
単純な置換はもちろん、条件をオプションで指定することで、細かい処理を行うことができます。  

### 特長
1. __スクリプトなので、もし気に入らない箇所があれば、自分でカスタマイズ可能です。__  
1. 置換回数や置換範囲、置換対象行を限定できるため、考え方次第で強力な置換ができます。  
(エディタ職人にはきっと不要なツールですが、お手軽に使えるので、有用だと思います。)

### 共通機能
1. 処理結果を確認したいときは、以下の方法を使うことが可能です。  
 * バックアップしておいて、実行結果とコンペアする。
 * `-b` オプションを使って、バックアップを作成し、before / afterを比べる
 * git使いなら、リポジトリ配下で処理実行 -> 差分を比較後、間違っていたら、`git reset --hard` する
1. 検索やフィルタ、範囲指定に正規表現を利用することができます。 `-r`  
(エディタと、各種置換ツールの便利なところをいいとこ取りしました。)
1. エンコードを指定することができます。 `-e`  
(対象ファイルがutf-8の場合、何もしなくてもいいです。)
1. 意図しないファイルに対して処理を実行しないように、除外リストを用意しています。 __(config/ignore*)__  
(__ディレクトリ名\* / \*ファイル名\* .拡張子\* __ で除外対象を決定しています。 [大文字の小文字区別はする])
1. 決めたディレクトリ, ファイル, 拡張子だけを処理対象にすることもできます。 (`-ed` `-ef` `-ee`)  
*除外リストと同じルールです。*
1. 一時的に除外リストが邪魔になったときは、除外リストを無効化してください。(`-id` `-if` `-ie`)

### 環境準備
#### pythonスクリプトをそのまま使う場合
1) pythonをインストールしてください。___Python3系___です。  
~~(python2系にしたいなら、3to2してみてください。必要ならやるかも。)~~  
python2対応したものを作成しました。動作未検証です。
 * 以下のどちらでも動きます。  
 [公式版](https://www.python.org/downloads)  
 [Anaconda](https://www.continuum.io/downloads "Minicondaでもよい")  

2) 適当な場所にscriptを格納してください。  
例 c:\work\python_script\grep_replace

#### 実行ファイル形式
python3が入れられない環境のために、実行ファイルを用意する予定。  
~~(python2系への対応よりは、こちらを優先してやりたい。)~~  
cxfreezeでうまいことバイナリ化できていないので、やむなくpy2系を先行リリース

# 日常的な使い方
1) 適当なコマンドラインツールで、script格納場所までcdします。  
cmd.exeでも、powershellでも、git bashでも動きます。  
 * 便利ツール  
 [conemu](https://conemu.github.io "コンソールエミュレータが便利です。")  

2) `python grep_replace.py` ... と処理を実施してください。

    以降の引数について
        argparseに対応しました。詳しくは詳細動作説明を見てください。

### あると便利なもの
 [Git for Windows](https://git-for-windows.github.io)  
 [WinMerge 日本語版](http://www.geocities.co.jp/SiliconValley-SanJose/8165/winmerge.html
 "公式より、いろいろ考慮されています。")  
 テキストエディタ(お好きなもの)  
 ___生成されたデータが意図通りであるかは、必ず自分で確認してください。___

# 自動実行について
手順を順番に書いて、バッチファイルにすることができます。(拡張子を、*.cmd or *.batとする)  
経験上のノウハウとして、`timeout 5` (5秒待つ)を組み合わせたほうが、ファイルシステム的に  
助かることが多いです。python3に対応してからは、まだそれほど重い処理を試していませんが……

# 詳細動作説明
    > python grep_replace.py -h
で、共通オプションの使い方が分かります。
    > python grep_replace.py XXX
___XXX___が、主要機能(サブコマンド)の呼び出しです。

|サブコマンド|短縮|機能|
|---|---|---|
|replace|rp|置換処理|
|replace_scope|rs|置換処理(範囲)|
|replace_list|rl|リスト置換処理|
|rename|rn|リネーム|
|delete_line|dl|行削除|
|delete_file|df|ファイル削除|
|addition_list|al|リスト追加処理|

    -h, --help     argparseを使うと、コマンドラインツールがきれいに作成できます。
                   (ヘルプメッセージも、サブコマンド単位で発行できます。)
    -v, --version  バージョンを表示します。
    -b, --backup   バックアップを作る機能です。バージョン管理していないディレクトリを
                   対象にする場合や、元の環境からの差分を確認するときに使います。
    -r, --regexp   検索 / 置換に正規表現を使うことができます。
    -e, --encode   エンコードを指定して対象ファイルを開きます。
                   したがって、rename, delete_fileには関係ないです。

## python grep_replace.py rp
対象ディレクトリ内の検索文字列を置換文字列で置き換えます。

置換回数を指定したいときは、-c(--counter)に数字を入力してください。  
0回は、無指定と同じです。対象ファイルの上から順番に、n回置換を行います。

    例:
        //testディレクトリの22を30に置き換える。(2回)
        python grep_replace.py rp test 22 30 -c 2
        22 22 22   --->  30 30 30          // -c 1
        22 23 24   --->  30 23 24          // -c 2
        22 23 24 22      22 23 24 22            .
        22 24 22         22 24 22               .
        22 25 22         22 25 22               .

検索文字列ではなく、フィルタ指定文字列との一致によって、置換対象行とするには-f(--filter)を使います。

    例:
        //bbbがある行で、 Data[0をData[4に置換
        python grep_replace.py rp test Data[0 Data[4 -f bbb
        aaa=1,ccc.Data[0]        aaa=1,ccc.Data[0]  //フィルタなしだと、Data[4になってしまう。
        aaa=2,ccc.Data[1]        aaa=2,ccc.Data[1]
        aaa=3,ccc.Data[2]        aaa=3,ccc.Data[2]
        bbb=4,ccc.Data[0]   ---> bbb=4,ccc.Data[4]
        bbb=5,ccc.Data[1]        bbb=5,ccc.Data[1]
        bbb=6,ccc.Data[2]        bbb=6,ccc.Data[2]
        ccc=4,ccc.Data[0]        ccc=4,ccc.Data[0]  //フィルタなしだと、Data[4になってしまう。
        ccc=5,ccc.Data[1]        ccc=5,ccc.Data[1]
        ccc=6,ccc.Data[2]        ccc=6,ccc.Data[2]

-nfオプション: filterの反対版。見つかったら置換対象行としません。

    例:
        // # でコメントアウトした行は、置換しない
        python grep_replace.py rp test target replace -nf "#"
        #target        #target
        target   --->  replace

__検索 / 置換に正規表現を使いたいときは、-r(--regexp)を追加してください。__  
フィルタにも、正規表現が適用されます。また、範囲開始行 / 終端判定も同様です。

    例:
        //zを1つ以上含む文字列を、repに変換する。
        python grep_replace.py rp test z+ rep -r
        aaa.Data[0]        aaa.Data[0]
        ab                 ab
        cde                cde
        keyword            keyword
        z             ---> rep
        zz            ---> rep
        zzz           ---> rep
        zzz_abc_zz    ---> rep_abc_rep
    例2:
        //Pt00→Pt[0]... ゼロサプレスしつつ、配列表記にする正規表現
        python grep_replace.py rp -r test Pt0*([\d]+) Pt[\1]

## python grep_replace.py rs
replaceの処理に、範囲指定を追加したものです。

    例:
        python grep_replace.py rs test "print bbb.Data[1]" "//print bbb.Data[1]" -s "func hoge()" }
        func hoge() // }まで実行        func hoge() // }まで実行
        {                               {
            bbb.Data[1] = 10                bbb.Data[1] = 10
            print bbb.Data[1]      --->     //print bbb.Data[1]
            bbb.Data[2] = "test"            bbb.Data[2] = "test"
            print bbb.Data[2]               print bbb.Data[2]
        }                               }
        func hogehoge()                 func hogehoge()
        {                               {
            bbb.Data[1] = 20                bbb.Data[1] = 20
            print bbb.Data[1]               print bbb.Data[1]
            bbb.Data[2] = "test"            bbb.Data[2] = "test"
            zzz = ccc.Data[2]               zzz = ccc.Data[2]
        }                               }
        【NOTE】
            ●scopeで、C#の自動プロパティ public string Name { get; set; }
              のような行内置換を考えると、処理が複雑になってしまうため、
              あえて開始行 = 終了行とならないようにしている。
              (replace_scopeを修正すればどうにでもなるが、範囲指定の使い方を考えると、
              あまり特別な処理を加えるつもりがない。)

## python grep_replace.py rl
先頭文字列を見つけたら、終端文字列までをスキップし、変わりにリストの情報を書き込みます。

    例:
        python grep_replace.py rl test -s "func hoge()" }
        func hoge()              <---    -------------------
        {                                replace_list.txtに書かれている内容
            bbb.Data[1] = 10             -------------------
            print bbb.Data[1]
            bbb.Data[2] = "test"
            print bbb.Data[2]
        }                        <---
        func hogehoge()                  func hogehoge()
        {                                {
            bbb.Data[1] = 20                 bbb.Data[1] = 20
            print bbb.Data[1]                print bbb.Data[1]
            bbb.Data[2] = "test"             bbb.Data[2] = "test"
            zzz = ccc.Data[2]                zzz = ccc.Data[2]
        }                                }
        【NOTE】
            ●使い道は、多岐にわたります。
                対象リストで必ず置き換えるので、こちらは、開始行 = 終了行もありです。
                ■ある行からある行を消したいときに、リストを工夫すれば、行数の増減は思いのままです。
                ■特定のキーワードを埋め込みたいときなどにも活躍しそうです。

## python grep_replace.py rn
ファイルのリネームを行います。

    例:
        python grep_replace.py rn test vol0 vol1
        python grep_replace.py rn -r test v.* vol1
        python grep_replace.py -r rn t2 v.* vol1
        testdata01_vol0.txt → testdata01_vol1.txt
        testdata02_vol0.txt → testdata02_vol1.txt
        testdata03_vol0.txt → testdata03_vol1.txt
        testdata04_vol0.txt → testdata04_vol1.txt
        testdata05_vol0.txt → testdata05_vol1.txt
        testdata06_vol0.txt → testdata06_vol1.txt
        testdata07_vol0.txt → testdata07_vol1.txt

## python grep_replace.py dl
検索文字列を基点に、削除開始行、削除行数で指定した行を削除します。

    例:
        //keywordを見つけた行から1行目を基点に、2行削除
        python grep_replace.py dl test keyword -s 1 2
        a                          a
        ab                         ab
        cde                        cde
        keyword1       <----       keyword1
        z                  1
        keyword2           2
        zzz                        zzz
        hoge                       hoge
        hogehoge                   hogehoge

        【NOTE】
            ●削除対象行は、再検索しません

## python grep_replace.py df
対象ディレクトリ内の全ファイルを削除します。

     例:
        //backで始まるディレクトリで、ファイル名にtestが含まれる、
        //拡張子.logで始まるファイルを削除する(back01\any_test01.logなど)
        //ファイル名:re.search(), ディレクトリ名, 拡張子:re.match()、
        //大文字小文字を区別しない: re.I(re.IGNORECASE)
        python grep_replace.py df test -ed back -ef test -ee .log

## python grep_replace.py al
対象ファイルに、追加リストの中身を追記します。  
先頭に追記するときは、-t(--top)を追加してください。(何も指定しない場合は、末尾に追記します。)

     例:
        python grep_replace.py al test
                                     <---    -------------------
                                             addition_list.txtに書かれている内容(-t)
                                             -------------------
        hoge
        hoge
                                     <---    -------------------
                                             addition_list.txtに書かれている内容
                                             -------------------
