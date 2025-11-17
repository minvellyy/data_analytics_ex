from bs4 import BeautifulSoup as BS
import urllib.request as req
import datetime
import os
import csv

url = 'https://news.naver.com/section/103'
url = 'https://news.naver.com/section/104'
url = 'https://news.naver.com/section/105'

def one_page_scraper(url):
    html= req.urlopen(url)

    # HTML 파싱하기
    soup = BS(html, 'html.parser')
    # print(soup)

    # 데이터 리스트 저장
    lis = soup.select('ul.sa_list > li')
    news_list = []
    # news = soup.select('li.sa_item._SECTION_HEADLINE')
    for li in lis:
        title = li.select_one('strong.sa_text_strong').get_text()
        press = li.select_one('div.sa_text_press').get_text()
        img_url = li.select_one('img')
        if img_url:
            img_url = img_url.get('src') or img_url.get('data-src')
            img_url = img_url.split('?')[0]
        else :
            img_url = 'No Image'

    # 하나의 뉴스 정보를 전체목록 리스트에 추가
        news_list.append([title, press, img_url])
    # print(news_list)

for num in range(100,105+1):
    print(num)
    url = f"https://news.naver.com/section/{num}"
    one_page_scraper(url)

print(news_list)

base_path = 'news_data'
os.makedirs(base_path, exist_ok=True)
getdate = datetime.datetime.now().strftime('%Y-%m-%d-%H') + '.csv'
with open(f"{base_path}/{getdate}", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(news_list)
