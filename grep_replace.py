import argparse
import shutil
import datetime
import os
import re
#import pdb; pdb.set_trace()

class GrepReplace:
    def __init__(self):
        '''
        親パーサに、全サブコマンドで使うものをまとめて配置
        グループは、ヘルプを見たときに分かれて表示させるための工夫。
        '''
        parent_parser = argparse.ArgumentParser(add_help=False)
        parent_parser.add_argument("-v", "--version", action="version", version="Grep to Replace 1.1.0")
        parent_parser.add_argument("-b", "--backup", action="store_true", help="バックアップを作る")
        parent_parser.add_argument("-r", "--regexp", action="store_true", help="検索 / 置換に正規表現を使う")
        parent_parser.add_argument("-e", "--encode", nargs="?", default="utf-8", help="エンコードを指定して対象ファイルを開く")
        p2 = parent_parser.add_argument_group("target details")
        p2.add_argument("-ed", "--enable-directories", nargs="+", help="有効ディレクトリ[1個以上]")
        p2.add_argument("-ef", "--enable-files", nargs="+", help="有効ファイル[1個以上]")
        p2.add_argument("-ee", "--enable-extensions", nargs="+", help="有効拡張子[1個以上]")
        p2.add_argument("-id", "--ignore-directories", action="store_false", help="無視ディレクトリリストを使わない")
        p2.add_argument("-if", "--ignore-files", action="store_false", help="無視ディレクトリリストを使わない")
        p2.add_argument("-ie", "--ignore-extensions", action="store_false", help="無視拡張子リストを使わない")

        parser = argparse.ArgumentParser(
            parents = [parent_parser],
            formatter_class = argparse.RawDescriptionHelpFormatter,
description =
"""
Grep and Replace Utillity
""",
epilog =
"""
------------------------------------------------------------------------------
バックアップを取りたいときは、-b(--backup)を追加してください。
影響チェックしたいときや、バージョン管理システムを導入できない環境のために、
このオプションは残してあります。

検索 / 置換に正規表現を使いたいときは、-r(--regexp)を追加してください。

エンコードを指定して対象ファイルを開くときは、-e(--encode)を指定してください。
(対象ファイルがutf-8の場合、何もしなくてもいいです。)
cp932, shift-jis: コマンドプロンプトの出力など(dir /s /b > リダイレクト.txt)
utf-16, utf-16-le: PowerShellの出力など(ls | Out-File out.txt)
なお、replace_list, addition_listは、utf-8のままでも大丈夫です。
(考えて追加してくれるようです。)

有効キーワードは、指定した(ディレクトリ | ファイル | 拡張子)のみ処理します。
無効リストは、除外する(ディレクトリ | ファイル | 拡張子)の一覧です。
したがって、有効キーワードにも無効リストにも該当するものは、無視されます。
それでは困る場合に、リストを無効化するオプションを使います。
もしくは、config/ignore_*sを編集して、直接無効化を解除してください。
"""
        )

        '''
        各機能はここに追加
        '''
        subparsers = parser.add_subparsers(metavar="サブコマンド一覧", dest="subcommand")


        s1 = subparsers.add_parser("replace", aliases=["rp"], help="置換処理",
            parents = [parent_parser],
            formatter_class = argparse.RawDescriptionHelpFormatter,
description =
"""
対象ディレクトリ内の検索文字列を置換文字列で置き換えます。

置換回数を指定したいときは、-c(--counter)に数字を入力してください。
0回は、無指定と同じです。上から順番に、n回置換を行います。

検索文字列ではなく、フィルタ指定文字列との一致によって、置換対象行とする
には-f(--filters)を使います。反対に、見つかったら置換対象行としないには
-nf(--no-filters)を使います。
"""
        )
        s1.add_argument("target", help="対象ディレクトリ")
        s1.add_argument("find", help="検索文字列")
        s1.add_argument("replace", help="置換文字列")
        s1.add_argument("-c", "--counter", type=int, help="置換カウンタ")
        s1.add_argument("-f", "--filters", nargs="+", help="フィルタ[1個以上]")
        s1.add_argument("-nf", "--no-filters", nargs="+", help="除外フィルタ[1個以上]")


        s2 = subparsers.add_parser("replace_scope", aliases=["rs"], help="置換処理(範囲)",
            parents = [parent_parser],
            formatter_class = argparse.RawDescriptionHelpFormatter,
description =
"""
対象ディレクトリ内の検索文字列を置換文字列で置き換えます。
範囲を限定するために、-s(--scope)に、開始文字列, 終了文字列を入れてください。

置換回数を指定したいときは、-c(--counter)に数字を入力してください。
0回は、無指定と同じです。置換回数 = スコープ回数です。

検索文字列ではなく、フィルタ指定文字列との一致によって、置換対象行とする
には-f(--filters)を使います。反対に、見つかったら置換対象行としないには
-nf(--no-filters)を使います。
"""
        )
        s2.add_argument("target", help="対象ディレクトリ")
        s2.add_argument("find", help="検索文字列")
        s2.add_argument("replace", help="置換文字列")
        s2.add_argument("-s", "--scope", nargs=2, required=True, help="範囲指定[開始, 終了]")
        s2.add_argument("-c", "--counter", type=int, help="置換カウンタ")
        s2.add_argument("-f", "--filters", nargs="+", help="フィルタ[1個以上]")
        s2.add_argument("-nf", "--no-filters", nargs="+", help="除外フィルタ[1個以上]")


        s3 = subparsers.add_parser("replace_list", aliases=["rl"], help="リスト置換処理",
            parents = [parent_parser],
            formatter_class = argparse.RawDescriptionHelpFormatter,
description =
"""
対象ディレクトリ内の開始文字列 ~ 終了文字列を、置換リストで置き換えます。

置換回数を指定したいときは、-c(--counter)に数字を入力してください。
0回は、無指定と同じです。置換回数 = スコープ回数です。
"""
        )
        s3.add_argument("target", help="対象ディレクトリ")
        s3.add_argument("-s", "--scope", nargs=2, required=True, help="範囲指定[開始, 終了]")
        s3.add_argument("-c", "--counter", type=int, help="置換カウンタ")


        s4 = subparsers.add_parser("rename", aliases=["rn"], help="リネーム",
            parents = [parent_parser],
            formatter_class = argparse.RawDescriptionHelpFormatter,
description =
"""
対象ディレクトリ内の検索ファイル名を置換ファイル名でリネームします。
"""
        )
        s4.add_argument("target", help="対象ディレクトリ")
        s4.add_argument("find", help="検索ファイル名")
        s4.add_argument("replace", help="置換ファイル名")


        s5 = subparsers.add_parser("delete_line", aliases=["dl"], help="行削除",
            parents = [parent_parser],
            formatter_class = argparse.RawDescriptionHelpFormatter,
description =
"""
検索文字列を見つけたら、削除開始行から、削除行数までを削る。
削除開始行, 削除行数は、検索文字列からの相対位置で指定する。(含マイナス)
""",
epilog =
"""
【例】
-3 AAA
-2 BBB
-1 CCC
 0 検索文字列
 1 DDD
 2 EEE
 3 FFF
 ・ 0,  0: 何もしない。
 ・ 0, -3: 何もしない。(削除行数 < 0のため)
 ・-3,  3: 検索文字列の上3行を削る。(AAA - CCCまで)
 ・-2,  5: 上下を削ることが可能。   (BBB - EEEまで)
 ・-4,  1: FFFが削られます。        (リスト終端)
 ※rangeの仕様に従います。
 また、削除対象行は、再検索対象外とします。
【例】
 AAA
 検索文字列(上)
 CCC
 検索文字列(下)
 DDD
 EEE
 FFF
 ・1, 1: CCC, DDDを削る。
(検索文字列(上)から、1文字目~1文字削除, 検索文字列(下)から、1文字目~1文字削除)
 ・1, 2: CCC, 検索文字列(下)を削る。
(検索文字列(上)から2文字削ると、検索文字列(下)は削られることになる為。)
"""
        )
        s5.add_argument("target", help="対象ディレクトリ")
        s5.add_argument("find", help="検索文字列")
        s5.add_argument("-s", "--scope", nargs=2, required=True, type=int, help="[削除開始行, 削除行数]")


        s6 = subparsers.add_parser("delete_file", aliases=["df"], help="ファイル削除",
            parents = [parent_parser],
            formatter_class = argparse.RawDescriptionHelpFormatter,
description =
"""
対象ディレクトリ内の全ファイルを削除します。
(enable_XXを使って、削除するディレクトリ, ファイル, 拡張子を
指定することが可能です。)
"""
        )
        s6.add_argument("target", help="対象ディレクトリ")
#        s6.add_argument("find", help="検索ファイル名")
#        s6.add_argument("-f", "--filters", nargs="+", help="フィルタ[1個以上]")


        s7 = subparsers.add_parser("addition_list", aliases=["al"], help="リスト追加処理",
            parents = [parent_parser],
            formatter_class = argparse.RawDescriptionHelpFormatter,
description =
"""
対象ファイルに、追加リストの中身を追記します。

先頭に追記するときは、-t(--top)を追加してください。
(何も指定しない場合は、末尾に追記します。)
"""
        )
        s7.add_argument("target", help="対象ディレクトリ")
        s7.add_argument("-t", "--top", action="store_true", help="先頭に追記")

        self.args = parser.parse_args()


    def backup(self):
        if self.args.backup:
            bkupdir = self.args.target + datetime.datetime.now().strftime("_%Y%m%d_%H%M%S") + "_bkup"
            shutil.copytree(self.args.target, bkupdir)

    def clear_counter(self):
        if self.args.counter:
            self.counter = self.args.counter

    def iscounter(self):
        if self.args.counter:
            if self.counter > 0:
                self.counter -= 1
                return True
            else:
                return False
        else:
            return True

     def isnofilter(self, line):
        if self.args.no_filters:
            for filter in self.args.no_filters:
                if self.isfind(filter, line):
                    return False
            else:
                return True
        else:
            return True

   def isfilter(self, line):
        if self.args.filters:
            for filter in self.args.filters:
                if self.isfind(filter, line):
                    return True
            else:
                return False
        else:
            if self.isfind(self.args.find, line):
                return True
            else:
                return False

    def isfind(self, find, line):
        if self.args.regexp:
            if re.compile(find).search(line):
                return True
        else:
            if find in line:
                return True

    #有効, 無効を判断して対象一覧を設定する
    def setlists(self):
        self.lists = []
        for root, dirs, files in os.walk(self.args.target):
            name = "directories"
            if self.args.ignore_directories and self.isignore(root, name):
                continue
            if self.args.enable_directories and self.isenable(root, name, self.args.enable_directories):
                continue
            for file in files:
                f, e = os.path.splitext(file)
                name = "files"
                if self.args.ignore_files and self.isignore(f, name):
                    continue
                if self.args.enable_files and self.isenable(f, name, self.args.enable_files):
                    continue
                name = "extensions"
                if self.args.ignore_extensions and self.isignore(e, name):
                    continue
                if self.args.enable_extensions and self.isenable(e, name, self.args.enable_extensions):
                    continue
                self.lists.append(os.path.join(root, file))

    #True 無視リストに含まれている→continue
    def isignore(self, path, name):
        with open("config/ignore_" + name + ".txt", encoding="utf-8") as ignores:
            for ig in ignores:
                if name == "files":
                    if re.compile(ig.replace("\n", ""), re.I).search(path):
                        return True
                else:
                    if re.compile(ig.replace("\n", ""), re.I).match(path):
                        return True
        return False

    #True 有効キーワードに含まれていない→continue
    def isenable(self, path, name, enables):
        for en in enables:
            if name == "files":
                if re.compile(en, re.I).search(path):
                    return False
            else:
                if re.compile(en, re.I).match(path):
                    return False
        return True

    def replace(self):
        for list in self.lists:
            self.clear_counter()
            with open(list, 'r', encoding=self.args.encode) as read_file:
                with open("tempfile", 'w', encoding=self.args.encode) as write_file:
                    for line in read_file:
                        dest = line
                        if self.isfilter(line) and self.isnofilter(line) and self.iscounter():
                            if self.args.regexp:
                                dest = re.sub(self.args.find, self.args.replace, line)
                            else:
                                dest = line.replace(self.args.find, self.args.replace)
                        write_file.write(dest)
            if os.path.isfile("tempfile"):
                os.remove(list)
                os.rename("tempfile", list)

    def replace_scope(self):
        for list in self.lists:
            self.clear_counter()
            flg = False
            with open(list, 'r', encoding=self.args.encode) as read_file:
                with open("tempfile", 'w', encoding=self.args.encode) as write_file:
                    for line in read_file:
                        dest = line
                        if self.isfind(self.args.scope[0], line):
                            flg = self.iscounter()
                        elif self.isfind(self.args.scope[1], line):
                            flg = False
                        if flg:
                            if self.isfilter(line) and self.isnofilter(line):
                                if self.args.regexp:
                                    dest = re.sub(self.args.find, self.args.replace, line)
                                else:
                                    dest = line.replace(self.args.find, self.args.replace)
                        write_file.write(dest)
            if os.path.isfile("tempfile"):
                os.remove(list)
                os.rename("tempfile", list)

    def replace_list(self):
        for list in self.lists:
            self.clear_counter()
            flg = False
            with open(list, 'r', encoding=self.args.encode) as read_file:
                with open("tempfile", 'w', encoding=self.args.encode) as write_file:
                    for line in read_file:
                        dest = line
                        if self.isfind(self.args.scope[0], line):
                            flg = self.iscounter()
                        if self.isfind(self.args.scope[1], line) and flg:
                            flg = False
                            with open("config/replace_list.txt", encoding="utf-8") as add_file:
                                [write_file.write(a) for a in add_file]
                                continue
                        if not flg:
                            write_file.write(dest)
            if os.path.isfile("tempfile"):
                os.remove(list)
                os.rename("tempfile", list)

    def rename(self):
        for list in self.lists:
            d, f = os.path.split(list)
            f, e = os.path.splitext(f)
            if self.args.regexp:
                r = re.sub(self.args.find, self.args.replace, f)
            else:
                r = f.replace(self.args.find, self.args.replace)
            dest = os.path.join(d, r) + e
            os.rename(list, dest)

    def delete_line(self):
        for list in self.lists:
            buf = []
            delflg = []
            with open(list, 'r', encoding=self.args.encode) as read_file:
                for line in read_file:
                    buf.append(line)
                    delflg.append(False)
            for i, line in enumerate(buf):
                if not delflg[i] and self.isfind(self.args.find, line):
                    for j in range(i + self.args.scope[0], i + self.args.scope[0] + self.args.scope[1]):
                        delflg[j] = True
            with open("tempfile", 'w', encoding=self.args.encode) as write_file:
                for i, line in enumerate(buf):
                    if not delflg[i]:
                        write_file.write(line)
            if os.path.isfile("tempfile"):
                os.remove(list)
                os.rename("tempfile", list)

    def delete_file(self):
        [os.remove(list) for list in self.lists]
#        for list in self.lists:
#            d, f = os.path.split(list)
#            f, e = os.path.splitext(f)
#            if self.isfilter(f):
#                os.remove(list)

    def addition_list(self):
        for list in self.lists:
            with open(list, 'r', encoding=self.args.encode) as read_file:
                with open("tempfile", 'w', encoding=self.args.encode) as write_file:
                    if self.args.top:
                        with open("config/addition_list.txt", encoding="utf-8") as add_file:
                            [write_file.write(a) for a in add_file]
                        [write_file.write(line) for line in read_file]
                    else:
                        [write_file.write(line) for line in read_file]
                        with open("config/addition_list.txt", encoding="utf-8") as add_file:
                            [write_file.write(a) for a in add_file]
            if os.path.isfile("tempfile"):
                os.remove(list)
                os.rename("tempfile", list)

    #対象一覧
    def printlists(self):
        print(self.lists)

    #引数一覧
    def printargs(self):
        print(self.args)

    def execute(self):
        #self.printargs()
        self.backup()
        self.setlists()
        #self.printlists
        if self.args.subcommand == "replace" or self.args.subcommand == "rp":
            self.replace()
        if self.args.subcommand == "replace_scope" or self.args.subcommand == "rs":
            self.replace_scope()
        if self.args.subcommand == "replace_list" or self.args.subcommand == "rl":
            self.replace_list()
        if self.args.subcommand == "rename" or self.args.subcommand == "rn":
            self.rename()
        if self.args.subcommand == "delete_line" or self.args.subcommand == "dl":
            self.delete_line()
        if self.args.subcommand == "delete_file" or self.args.subcommand == "df":
            self.delete_file()
        if self.args.subcommand == "addition_list" or self.args.subcommand == "al":
            self.addition_list()
'''
処理先頭はこちら
'''
gr = GrepReplace()
gr.execute()
