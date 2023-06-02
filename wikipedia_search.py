
# coding:utf-8

# ==========================
# インポートモジュール
# ==========================
import wikipedia

# ==========================
# 処理
# ==========================


def wikipedia_search(search_keyword):
    print(search_keyword + " について検索中...")
    wikipedia.set_lang("ja")  # 言語を日本語に
    result = wikipedia.search(search_keyword)  # 検索
    if not result:
        print("ページは見つかりませんでした")
        engFlag = True
        while(engFlag):
            number = input("英語で検索してみますか? (y/n) :")
            if(number == 'y'):
                wikipedia.set_lang("en")  # 言語を英語に
                result = wikipedia.search(search_keyword)  # 検索
                if not result:
                    print("ページは見つかりませんでした / Not Found")
                engFlag = False
            elif(number == 'n'):
                engFlag = False
            else:
                print("y/nで答えてください")
    else:
        print("\n" + wikipedia.summary(search_keyword, sentences=0))
        print("<関連ワード>\n" + str(result) + "\n")
        pageFlag = True
        while(pageFlag):
            number = input("詳細な情報を表示しますか (y/n) :")
            if(number == 'y'):
                print("\n" + wikipedia.page(search_keyword).content)  # 検索
                pageFlag = False
            elif(number == 'n'):
                pageFlag = False
            else:
                print("y/nで答えてください")