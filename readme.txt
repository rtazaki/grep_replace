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
    replace (rep, rp)   置換処理
    replace_list (repl, rl)
                        リスト置換処理
    rename (ren, rn, mv)
                        リネーム
    deleteline (del, dl)
                        行削除

	★replace
		対象ディレクトリ内の検索文字列を置換文字列で置き換えます。

		置換回数を指定したいときは、-c(--counter)に数字を入力してください。
		0回は、無指定と同じです。対象ファイルの上から順番に、n回置換を行います。
	例:
		22 22 22
		22 23 24
		22 23 24 22
		22 24 22
		22 25 22


		検索文字列ではなく、フィルタ指定文字列との一致によって、置換対象行とする
		には-f(--filter)を使います。

		範囲を限定したいときは、-s(--scope)に、開始文字列, 終了文字列を入れてください。




	★replace_each.py
		対象文字列を見つけた行で、検索文字列を置換文字列で置き換えます。
	例:
		対象となるファイルが以下の構成だとします。
		aaa=1,ccc.Data[0]
		aaa=2,ccc.Data[1]
		aaa=3,ccc.Data[2]
		bbb=4,ccc.Data[0]
		bbb=5,ccc.Data[1]
		bbb=6,ccc.Data[2]
		ccc=4,ccc.Data[0]
		ccc=5,ccc.Data[1]
		ccc=6,ccc.Data[2]

		ここで、対象文字列に"bbb"、検索文字列に"Data[0"、置換文字列に"Data[4"を指定した場合、
		aaa=1,ccc.Data[0]
		aaa=2,ccc.Data[1]
		aaa=3,ccc.Data[2]
		bbb=4,ccc.Data[4]
		bbb=5,ccc.Data[1]
		bbb=6,ccc.Data[2]
		ccc=4,ccc.Data[0]
		ccc=5,ccc.Data[1]
		ccc=6,ccc.Data[2]
		
		【NOTE】
			●しばしば「ある条件を満たした行だけ」「この文字列をこの文字列に置換したい」ということがあるので、
			  そのときには便利かと。

	★replace_RegExp.py
		置換処理に、正規表現が使えます。
	例:
		対象となるファイルが以下の構成だとします。
		aaa.Data[0]
		ab
		cde
		keyword
		z
		zz
		zzz
		zzz_abc_zz

		ここで、検索文字列に"z+"、置換文字列に"rep"を指定した場合、
		aaa.Data[0]
		ab
		cde
		keyword
		rep
		rep
		rep
		rep_abc_rep
		とします。
		
		【NOTE】
			//Pt00→Pt[0]... ゼロサプレスしつつ、配列にする正規表現
			Pt0*([\d]+) Pt[\1]


	★Replace_Scope.py
		先頭文字列 終端文字列 検索文字列 置換文字列を与えて、
		特定の範囲内のデータを置換します。
	例:
		対象となるファイルが以下の構成だとします。
		func hoge()
		{
			bbb.Data[1] = 10
			print bbb.Data[1]
			bbb.Data[2] = "test"
			print bbb.Data[2]
		}
		func hogehoge()
		{
			bbb.Data[1] = 20
			print bbb.Data[1]
			bbb.Data[2] = "test"
			zzz = ccc.Data[2]
		}
		
		ここで、先頭文字列に"func hoge()"、終端文字列に"}"
		検索文字列に"print bbb.Data[1]"、
		置換文字列に"//print bbb.Data[1]"
		を指定した場合、
		func hoge()
		{
			bbb.Data[1] = 10
			//print bbb.Data[1]
			bbb.Data[2] = "test"
			print bbb.Data[2]
		}
		func hogehoge()
		{
			bbb.Data[1] = 20
			print bbb.Data[1]
			bbb.Data[2] = "test"
			zzz = ccc.Data[2]
		}
		とします。
		
		【NOTE】
			●先頭文字列が、ユニークな(ひとつしか存在しない)場合、
			  その箇所のみが置換されますが、複数ひっかかる場合、
			  その箇所でも置換が実行されます。
			●正規表現化は今のところしていません。
			  (必要なら実施します。)
			●コマンドライン引数でタブを扱えないので、
			  タブを含まない条件を指定してください。

	★ReplaceList.py
		先頭文字列を見つけたら、終端文字列までをスキップし、
		変わりにリストの情報を書き込む。
	例:
		対象となるファイルが以下の構成だとします。
		func hoge()
		{
			bbb.Data[1] = 10
			print bbb.Data[1]
			bbb.Data[2] = "test"
			print bbb.Data[2]
		}
		func hogehoge()
		{
			bbb.Data[1] = 20
			print bbb.Data[1]
			bbb.Data[2] = "test"
			zzz = ccc.Data[2]
		}
		ここで、先頭文字列に"func hoge()"、終端文字列に"print bbb.Data[2]"
		を指定した場合、
		-------------------
		ReplaceList.txtに書かれている内容
		-------------------
		}
		func hogehoge()
		{
			bbb.Data[1] = 20
			print bbb.Data[1]
			bbb.Data[2] = "test"
			zzz = ccc.Data[2]
		}
		とします。
		
		【NOTE】
			●コマンドライン引数でタブを扱えないですが、これなら大丈夫です。
			●使い道は、多岐にわたります。
				■ある行からある行を消したいときに、リストを工夫すれば、行数の増減は思いのままです。
				■特定のキーワードを埋め込みたいときなどにも活躍しそうです。

	★ReplaceList_special.py
		先頭文字列を見つけたら、終端文字列までをスキップし、
		変わりにリストの情報を書き込む。
		ただし、置換した行は再び置換しないようにする。
	例:
		対象となるファイルが以下の構成だとします。
		aaa
		target
		target
		bbb
		ccc
		
		ReplaceList.txtに書かれている内容
		-------------------
		change
		change
		-------------------
		↑targetをchangeで置き換えたい。
		ここで、先頭文字列に"target"、終端文字列に"target"
		を指定した場合、ReplaceListだと
		aaa
		change
		change
		change
		change
		bbb
		ccc
		となってしまい目的が果たせないので、置換した行数を覚えておき、
		aaa
		change
		change
		bbb
		ccc
		とします。
		【NOTE】
			●置換した行数を覚えておく仕組みなので、先頭文字列と終端文字列が同じ場合はこちらのほうが適切な処理が出来ます。
				■上の例だと、最初のtargetをchange*2で置換した後、2番目のtargetを飛ばします。
				■この方式でいけば、複数行にわたって同じ設定になっている箇所をまとめて上書きできます。

	★rename.py
		ファイルのリネームを行います。
	例:
		testdata01_vol0.txt → testdata01_vol1.txt
		testdata02_vol0.txt → testdata02_vol1.txt
		testdata03_vol0.txt → testdata03_vol1.txt
		testdata04_vol0.txt → testdata04_vol1.txt
		testdata05_vol0.txt → testdata05_vol1.txt
		testdata06_vol0.txt → testdata06_vol1.txt
		testdata07_vol0.txt → testdata07_vol1.txt

	★deleteline
		検索文字列を基点に、削除開始行、削除行数で指定した行を削除します。
	例:
		対象となるファイルが以下の構成だとします。
		a
		ab
		cde
		keyword
		z
		keyword
		zzz
		hoge
		hogehoge

		ここで、検索文字列に"keyword"、開始行=1、削除行=2とした場合、
		a
		ab
		cde
		keyword
		zzz
		hoge
		hogehoge
		とします。
		
		【NOTE】
			●削除対象行は、検索対象外になります。
			  zの下のkeywordは、削除対象行です。
			  そのため、zzz, hogeは、削除されずに残っています。

[コマンドラインについて]
	テキストで、手順を順番に書いて、バッチファイル化することができます。
	ファイル名を、*.cmd or *.batとすれば、定型の処理は自動化できます。
