import requests
import json
import pprint
import numpy as np

def geekScore_return(slug):
    phone_specifications_url = 'https://api-mobilespecs.azharimm.site/v2/' + slug
    phone_specifications = requests.get(phone_specifications_url)
    phone_detail = json.loads(phone_specifications.text)
    #スペックスコアを取得
    try:
        phone_specs = phone_detail['data']['specifications'][13]['specs']
    except IndexError as ie:
        #print('スペックスコアの情報がありませんでした。: {}'.format(ie))
        return 0
    except NameError as ne:
        #print('名前エラー: {}'.format(ie))
        return 0
    except Exception as ex:
        #print('other: {}'.format(ex))
        return 0

    #ベンチマークスコア
    phone_score = phone_specs[0]

    #スコアのみ
    phone_score = phone_score['val']
    phone_score = str(phone_score)
    phone_score = phone_score.replace("[","")       #[削除
    phone_score = phone_score.replace("]","")       #]削除
    phone_score = phone_score.replace("'","")       #アポストロフィ削除
    phone_score = phone_score[2:]
    phone_score = phone_score.split('\\n')       #アポストロフィ削除

    if( "(v5.1)" not in str(phone_score)):
        #print("最新のベンチマークアプリで計測されていないので比較することができません。")
        geekBench = 0
    else:
        #print(phone_score)
        geekBench = str(phone_score[1])[-11:-7]
        #print(geekBench)

    return geekBench

#近い値
def getNearestValue(list, num):
    """
    概要: リストからある値に最も近い値を返却する関数
    @param list: データ配列
    @param num: 対象値
    @return 対象値に最も近い値
    """

    # リスト要素と対象値の差分を計算
    # 最小値のインデックスを取得
    idx = np.abs(np.asarray(list) - num).argmin()
    return idx




