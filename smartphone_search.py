import requests
import json
import pprint
import numpy as np

from score import geekScore_return
from score import getNearestValue
from wikipedia_search import wikipedia_search


# ==========================
# 配列やURL
# ==========================

#初期化
phones_score = []
phones_name = []
brands_url = 'https://api-mobilespecs.azharimm.site/v2/brands/'
#人気スマホ欄の初期化
top_phone_name = []
top_phone_score = []
#人気スマホ取得
top_url = 'https://api-mobilespecs.azharimm.site/v2/top-by-fans'
top_res = requests.get(top_url)
top_data = json.loads(top_res.text)
top_data = top_data['data']['phones']
#一部スマホメーカー
detail_url_data = ['apple-phones-48','asus-phones-46','huawei-phones-58','google-phones-107','samsung-phones-9','oppo-phones-82','xiaomi-phones-80','sharp-phones-23','motorola-phones-4']



# ==========================
# 機種検索
# ==========================
print("機種名を入力してください。")
search_phone = input()
search_url = 'http://api-mobilespecs.azharimm.site/v2/search?query=' + search_phone
search_res = requests.get(search_url)
#検索結果
data = json.loads(search_res.text)
my_phone_data = data['data']['phones']
print()

if(len(my_phone_data) == 0):
    print("お探しの機種が見つかりませんでした。")
    exit()
else:
    phone_name = [d.get('phone_name') for d in my_phone_data]
    #スマホを絞る
    if(len(my_phone_data) == 1):
        print(str(phone_name) + "が選択されました。")
    else:
        print("検索の結果、" +str(len(my_phone_data)) +"個の機種が見つかりました。")
        pprint.pprint(phone_name)
        flag = False
        while (flag == False):
            print("機種を1~"+ str(len(my_phone_data))+"の間から「数字」で選択してください。")
            phone_number = input()
            if(1 <= int(phone_number) <= len(my_phone_data)):
                flag = True
                phone_name = str(phone_name[int(phone_number) - 1])
                print(phone_number + "番目の "+ phone_name+ " が選択されました。")
                my_phone_data = my_phone_data[int(phone_number) - 1]
                phone_score =  geekScore_return(my_phone_data['slug'])
                if(phone_score == 0):
                    print("最新のスマホではないためベンチマークスコアを取得できませんでした。")
                    exit()
print()


# ==========================
# 人気スマホについて
# ==========================
print("人気スマホを表示")
#人気スマホの名前とスコアの取得
for i in range(len(top_data)):
    top_phone_score.append(int(geekScore_return(top_data[i]['slug'])))
    top_phone_name.append(top_data[i]['phone_name'])
    print(top_phone_name[i])
    print()

#人気スマホから類似したスコアを選択
n = getNearestValue(top_phone_score,int(phone_score))

print("人気スマホから類似スマホしているスマホの検索が終わりました。\n")
print("選択されたスマホ : " + phone_name + ", スコア : "+phone_score)
print("人気のある類似スマホ : " + top_phone_name[n] +", スコア : " + str (top_phone_score[n]) + "\n")

# ==========================
# Wikipedia
# ==========================
#選択されたスマホをwikipediaで検索
while flag:
    choice = input("選択されたスマホについてWikipediaで検索しますか？ (y/n) : ")
    if choice in ['y', 'ye', 'yes']:
        flag = False
        wikipedia_search(phone_name)
    elif choice in ['n', 'no']:
        flag = False
    else:
        flag = True

#改行とフラグ初期化
print()
flag = True

#類似したスマホをwikipediaで検索
while flag:
    choice = input("人気のある類似したスマホについてWikipediaで検索しますか？ (y/n) : ")
    if choice in ['y', 'ye', 'yes']:
        flag = False
        wikipedia_search(top_phone_name[n])
    elif choice in ['n', 'no']:
        flag = False
    else:
        flag = True

#改行とフラグ初期化
print()
flag = True


# ==========================
# スマホメーカーから取得のflag
# ==========================
while flag:
    choice = input("有名スマホメーカーから比較しますか。注意:時間がかかります。(y/n) : ")
    if choice in ['y', 'ye', 'yes']:
        flag = False
    elif choice in ['n', 'no']:
        flag = False
        print("プログラムを終了します")
        exit(0)
    else:
        flag = True


#改行とフラグ初期化
print()
flag = True


# ==========================
# スマホメーカーから取得
# ==========================
for i in range(len(detail_url_data)):
    #ページ数とカウントを作動させるためにそれぞれ初期化
    page = 1
    page_flag = True
    score_zero_count = 0

    while page_flag:
        #URLまとめ
        url = brands_url + detail_url_data[i] + "?page=" + str(page)
        print(url)
        #データ取得
        phones_res = requests.get(url)
        tmp_phones_data = json.loads(phones_res.text)
        if('error' in tmp_phones_data):
            print("検索にエラーが発生しました")
            print(str(tmp_phones_data))
            exit(0)
        tmp_phones_data = tmp_phones_data['data']['phones']

        #メーカー内のスマホがなくなったら次のメーカーに進む
        #リクエスト軽減のためスペックスコアの情報がないスマホに11個以上になったら次のメーカーに進む
        if(any(tmp_phones_data) == False or score_zero_count > 10):
            page_flag = False
            continue

        #データ保存
        for j in range(len(tmp_phones_data)):
            #スコアと名前を一次保存
            tmp_score = int(geekScore_return(tmp_phones_data[j]['slug']))
            tmp_name = tmp_phones_data[j]['phone_name']
            

            #書くとしているスマホについて
            print("端末名 : " + tmp_name + " のデータを取得中") 
            #自分のスマホと同じスマホにしないためcontinueで飛ばす
            if(tmp_score == phone_score):
                continue
            phones_name.append(tmp_name)
            phones_score.append(tmp_score)
            if(tmp_score == 0):
                score_zero_count += 1
        
        #次のページへ
        page += 1
    

print()
print(str(len(phones_name)) + "個のスマホから選択されます。\n" )


# 有名メーカーで取得したすべてのスマホを表示　（デバッグ用)
for i in range(len(phones_name)):
    print("スマホの名前 : " + str (phones_name[i]))
    print("スマホのスコア : " + str(phones_score[i]))

#類似値のスマホの番号
n = getNearestValue(phones_score,int(phone_score))

print("類似スマホの検索が終わりました。")
print("選択されたスマホ : " + phone_name + ", スコア : " + phone_score)
print("類似スマホ : " + phones_name[n] +", スコア : " + str (phones_score[n]) + "\n")


# ==========================
# 類似したスマホをwikipediaで検索
# ==========================
while flag:
    choice = input("類似したスマホについてWikipediaで検索しますか？ (y/n) : ")
    if choice in ['y', 'ye', 'yes']:
        flag = False
        wikipedia_search(phones_name[n])
    elif choice in ['n', 'no']:
        flag = False
    else:
        flag = True

print("プログラムを終了します")




'''
リクエスト数の関係で廃止
#すべてのスマホの取得
#取得
brands_url = 'https://api-mobilespecs.azharimm.site/v2/brands/'
brands_res = requests.get(brands_url)
brands_data = json.loads(brands_res.text)
if('error' in brands_data):
    print("検索にエラーが発生しました")
    exit(0)

brands_data = brands_data['data']
detail_url_data = []
phones_data = []
phones_score = []
phones_name = []

for i in range(len(brands_data)):
    #ページ分やる
    page = 1
    page_flag = True
    while page_flag:
        detail_url_data.append(brands_data[i]['detail'])
        print(detail_url_data[i])
        phones_res = requests.get(detail_url_data[i])
        phones_data = json.loads(phones_res.text)

        pprint.pprint(phones_data)

        phones_data = phones_data['data']['phones']
        print("メーカーのスマホの数 : " + str(len(phones_data)))
        for j in range(len(phones_data)):
            phones_name.append(phones_data[j]['phone_name'])
            phones_score.append(int(geekScore_return(phones_data[j]['slug'])))
        page += 1

print(len(phones_name))
print()
for i in range(len(phones_name)):
    print("スマホの名前 : " + str (phones_name[i]))
    print("スマホのスコア : " + str(phones_score[i]))

n = getNearestValue(phones_score,int(phone_score))

print("選択されたスマホ : " + phone_name + ", スコア : " + phone_score)
print("類似スマホ : " + phones_name[n] +", スコア : " + str (phones_score[n]))
'''



