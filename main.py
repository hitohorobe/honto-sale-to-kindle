from amazon_paapi import AmazonApi
from bs4 import BeautifulSoup
import requests, pprint, os, time
from requests.models import HTTPError

# amazon api
AMAZON_API_KEY = os.environ.get('AMAZON_API_KEY')
AMAZON_SECRET_KEY = os.environ.get('AMAZON_SECRET_KEY')
AMAZON_TAG = os.environ.get('AMAZON_TAG')
AMAZON_COUNTRY = os.environ.get('AMAZON_COUNTRY')

# bit.ly api
BITLY_TOKEN = os.environ.get('BITLY_TOKEN')
BITLY_API_URL = 'https://api-ssl.bitly.com/v3/shorten'

# ua
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
HEADERS = {'User-Agent': USER_AGENT}

# Amazonの検索対象=kindle
BROWSE_NODE_ID = '2275256051'

# honto url=早川書房のセール
HONTO_URL = 'https://honto.jp/ebook/search_0710_022_09-salesnum7d.html?cid=CTES_hayakawa2208_search_all&prdtp=0&relKw=cp10740583&tbty=2&pgno='

# 追加キーワード
KEYWORD = '早川書房'


def get_max_pgno():
    """hontoのキャンペーンページのページ数を返す"""
    try:
        res = requests.get(headers=HEADERS, url=HONTO_URL)
    except HTTPError as e:
        print(e)
        return False
    
    try:
        soup = BeautifulSoup(res.text, 'html.parser')
        pager = soup.find('ul', attrs={'class', 'stPager dyPreloadLink'})
        pagenums = pager.find_all('li')
        max_pagenum = 0
        for pagenum in pagenums:
            try:
                if int(pagenum.text) > max_pagenum:
                    max_pagenum = int(pagenum.text)
            except Exception as e:
                continue
        return max_pagenum


    except AttributeError as e:
        print(e)
        return False    


def get_book_title_list(pgno):
    """hontoのキャンペーンページから書籍タイトルをぜんぶ取る"""
    try:
        res = requests.get(headers=HEADERS, url=HONTO_URL + str(pgno))
    except HTTPError as e:
        print(e)
        return False
    
    try:
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.find_all('h2', attrs={'class', 'stHeading'})
    except AttributeError as e:
        print(e)
        return False

    title_list = []
    for title in titles:
        title = title.text.replace('\n', '')
        title = title.replace('【期間限定価格】', '')
        if title == '最新の「honto」アプリをご利用の方' or title == '最新の「honto」アプリをダウンロードされる方':
            continue
        title_list.append(title)

    return title_list


def get_asin(title):
    """
    paapiで検索してasinをとる
    """
    amazon = AmazonApi(AMAZON_API_KEY, AMAZON_SECRET_KEY, AMAZON_TAG, AMAZON_COUNTRY, throttling=1.5)
    try:
       search_result = amazon.search_items(
            keywords=title + KEYWORD,
            browse_node_id=BROWSE_NODE_ID,
        )
    except Exception as e:
        print(e)
        return 
    
    if search_result.items[0]:
        return search_result.items[0].asin
    else:
        return 


def make_url(asin_list):
    """
    検索結果URLをつくる
    asin120件を超えると短縮できないため、120件で区切る
    """
    base_url = 'https://www.amazon.co.jp/s?i=digital-text&hidden-keywords='
    url_list = []
    for i,asin in enumerate(asin_list):
        if asin:
            if i%120 == 0:
                url = base_url
                url_list.append(url)
            url_list[-1] += asin + '|' 
    
    return url_list


def short_url(url_list):
    """つくったURLを短縮する"""
    shorten_list = []
    for url in url_list:
        query = {
            'access_token': BITLY_TOKEN,
            'longurl': url + '&tag=' + AMAZON_TAG 
        }
        try:
            res = requests.get(BITLY_API_URL, query)
            if res.status_code == 200:
                shorten_list.append(res.json()['data']['url'])
        except HTTPError as e:
            print(e)

    return shorten_list


if __name__ == '__main__':
    asin_list = []
    max_pagenum = get_max_pgno()
    for pgno in range(1, max_pagenum):
        title_list = get_book_title_list(pgno)
        for title in title_list:
            # api制限対策
            time.sleep(1)       
            asin = get_asin(title)
            print(asin)
            if asin:
                asin_list.append(asin)
    url_list = make_url(asin_list)
    shorten_list = short_url(url_list)
    pprint.pprint(shorten_list)
    