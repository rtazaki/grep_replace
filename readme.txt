[概要]
    いろいろ使えるGrepReplaceツールです。
    よくあるフリーソフトや、エディタでのGrep置換とは違うアプローチをしています。

[特長]
    スクリプトなので、カスタマイズが効きます。(何をしているのか見えているため。)
    置換回数や置換範囲、置換対象行が設定できるため、考え方次第で強力な置換ができます。

[環境準備]
    1) pythonをインストールしてください。Python3系です。
       公式版でも、Anacondaでも動きます。
        https://www.python.org/downloads/
        https://www.continuum.io/downloads
    2) 次に適当な場所にscriptを格納してください。
        例 c:\work\python_script\grep_replace

[日常の使い方]
    1) 適当なコマンドラインツールで、script格納場所までcdします。
       cmd.exeでも、powershellでも、git bashでも動きます。
       conemuが便利です。
        https://conemu.github.io/
    2) python grep_replace.py ... と処理を実施してください。

    ●引数について
        ■argparseに対応しました。

[あると便利なもの]
    ★Git for Windows
        https://git-for-windows.github.io/
    ★WinMerge 日本語版
        http://www.geocities.co.jp/SiliconValley-SanJose/8165/winmerge.html
        公式より、いろいろ考慮されています。
    ★エディタ
        生成されたデータが意図通りであるか調査してください。

[詳細動作説明]
    > python grep_replace.py -h
        で、共通のオプションの使い方が分かります。
    > python grep_replace.py XXX の部分が、主要機能の呼び出しです。
  サブコマンド一覧
    replace (rp)        置換処理
    replace_scope (rs)  置換処理(範囲)
    replace_list (rl)   リスト置換処理
    rename (rn)         リネーム
    delete_line (dl)    行削除
    delete_file (df)    ファイル削除
    addition_list (al)  リスト追加処理

  -h, --help     argparseを使うと、コマンドラインツールがきれいに作成できます。
                 (ヘルプメッセージも、サブコマンド単位で発行できます。)
  -v, --version  バージョンを表示します。
  -b, --backup   バックアップを作る機能です。バージョン管理していないフォルダを
                 対象にする場合や、元の環境からの差分を確認するときに使います。
  -r, --regexp   検索 / 置換に正規表現を使うことができます。
  -e, --encode   エンコードを指定して対象ファイルを開きます。
                 したがって、rename, delete_fileには関係ないです。

    ★python grep_replace.py rp
        対象ディレクトリ内の検索文字列を置換文字列で置き換えます。

        置換回数を指定したいときは、-c(--counter)に数字を入力してください。
        0回は、無指定と同じです。対象ファイルの上から順番に、n回置換を行います。
    例:
        //testフォルダの22を30に置き換える。(2回)
        python grep_replace.py rp test 22 30 -c 2
        22 22 22   --->  30 30 30          // -c 1
        22 23 24   --->  30 23 24          // -c 2
        22 23 24 22      22 23 24 22            .
        22 24 22         22 24 22               .
        22 25 22         22 25 22               .

        検索文字列ではなく、フィルタ指定文字列との一致によって、置換対象行とする
        には-f(--filter)を使います。
    例:
        //bbbがある行で、 Data[0をData[4に置換
        python grep_replace.py rp test Data[0 Data[4 -f bbb
        aaa=1,ccc.Data[0]        aaa=1,ccc.Data[0]
        aaa=2,ccc.Data[1]        aaa=2,ccc.Data[1]
        aaa=3,ccc.Data[2]        aaa=3,ccc.Data[2]
        bbb=4,ccc.Data[0]   ---> bbb=4,ccc.Data[4]
        bbb=5,ccc.Data[1]        bbb=5,ccc.Data[1]
        bbb=6,ccc.Data[2]        bbb=6,ccc.Data[2]
        ccc=4,ccc.Data[0]        ccc=4,ccc.Data[0]
        ccc=5,ccc.Data[1]        ccc=5,ccc.Data[1]
        ccc=6,ccc.Data[2]        ccc=6,ccc.Data[2]
        【NOTE】
            ●timestampが10:00:00,11:00:00のデータを対象として、XXXをYYYに置換する。
              //や# でコメントアウトされている行のXXXをYYYに置換する。
              など、結構使い道はある。
            ★-nfオプション: filterの反対版。見つかったら置換対象行としない。

        検索 / 置換に正規表現を使いたいときは、-r(--regexp)を追加してください。
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
        【NOTE】
            ●上記フィルタにも、正規表現が適用されます。また、下の範囲開始行 / 終端判定も同様です。

    ★python grep_replace.py rs
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
            ●scopeで、C#の自動プロパティ
              public string Name { get; set; } のような行内置換を
              考えると、処理が複雑になってしまうため、あえて開始行 = 終了行と
              ならないようにしている。
              (例題の // }と区別がつかないのと、flgがTrue->Falseになったときだけは、
              置換処理を行う としなければならない。)
              そのほかのコマンドで代用が効くはずなので、このままとしておく。

    ★python grep_replace.py rl
        先頭文字列を見つけたら、終端文字列までをスキップし、変わりにリストの情報を書き込む。
    例:
        python grep_replace.py rl test -s "func hoge()" }
        func hoge()              <---    -------------------
        {                                ReplaceList.txtに書かれている内容
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
                ■ある行からある行を消したいときに、リストを工夫すれば、行数の増減は思いのままです。
                ■特定のキーワードを埋め込みたいときなどにも活躍しそうです。

    ★python grep_replace.py rn
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

    ★python grep_replace.py dl
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

    ★python grep_replace.py df
        対象ディレクトリ内の全ファイルを削除します。
     例:
        //backで始まるディレクトリで、ファイル名にtestが含まれる、
        //拡張子.logで始まるファイルを削除する(back01\any_test01.logなど)
        //ファイル名:re.search(), フォルダ名, 拡張子:re.match()、大文字小文字を区別しない
        python grep_replace.py df test -ed back -ef test -ee .log

    ★python grep_replace.py nl
        対象ファイルに、追加リストの中身を追記します。
        先頭に追記するときは、-t(--top)を追加してください。
        (何も指定しない場合は、末尾に追記します。)
     例:
        python grep_replace.py nl test

[コマンドラインについて]
    テキストで、手順を順番に書いて、バッチファイル化することができます。
    ファイル名を、*.cmd or *.batとすれば、定型の処理は自動化できます。
