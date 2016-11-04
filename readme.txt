[概要]
	いろいろ使えるGrepReplaceツールです。
	よくあるフリーソフトや、エディタでのGrep置換とは違うアプローチをしています。

[特長]
	スクリプトなので、カスタマイズが効く。(何をしているのか見える)
	置換回数や置換範囲、置換対象行が設定できるため、考え方次第で強力な置換ができる。

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
	2) python grep_replace.py サブコマンド ... として処理を実施してください。
	
	●引数について
		■argparseに対応しました。

[あると便利なもの]
	★WinMerge 日本語版
		公式より、いろいろ考慮されています。
	★エディタ
		生成されたデータが意図通りであるか調査してください。

[詳細動作説明]

	★deleteLine.py
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

	★replace.py
		検索文字列を置換文字列で置き換えます。
	例:
		対象となるファイルが以下の構成だとします。
		aaa.Data[0]
		ab
		cde
		keyword
		z
		zz
		zzz

		ここで、検索文字列に"Data[0"、置換文字列に"Data[1"を指定した場合、
		aaa.Data[1]
		ab
		cde
		keyword
		z
		zz
		zzz
		とします。
		
		【NOTE】
			●引数は""でくくってください。

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
			●マッチ(正規表現で検索にひっかかった状態)した文字列をそのまま置き換えるので、
			  rep
			  reprep
			  repreprep
			  とはならないです。
			  しかし、zzz_abc_zz が rep_abc_repとなります。(見つかったもの全体を置換する。)
			●[とか(が入っていると、正規表現のキーワードとして認識されてしまうので、
			  エスケープ※してください。
				※[→\[ (→\(
			●置換文字列には、正規表現を使えないです。

	★replace_RegExp_Add.py
		検索文字列(正規表現)の後ろに、追加文字列をくっつけます。
	例:
		対象となるファイルが以下の構成だとします。
		aaa.Data[0] = ab
		print ab
		cde = ab + aaa.Data[0] + "\n"
		bbb.Data[1] = z
		print z
		ccc.Data[2] = z + aaa.Data[3]
		zzz = ccc.Data[2]

		ここで、検索文字列に"Data\[[^\]*]\]"、追加文字列に".Value"を指定した場合、
		aaa.Data[0].Value = ab
		print ab
		cde = ab + aaa.Data[0].Value + "\n"
		bbb.Data[1].Value = z
		print z
		ccc.Data[2].Value = z + aaa.Data[3].Value
		zzz = ccc.Data[2].Value
		とします。

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

[コマンドラインについて]
	テキストで、手順を順番に書いて、バッチファイルの出来上がり。
	ファイル名を、*.cmd or *.batとすれば、定型の処理は自動化できます。
