from bs4 import BeautifulSoup as BS
import urllib.request as req
import datetime
import os
import csv

url = 'https://finance.naver.com/marketindex/exchangeList.naver'
html= req.urlopen(url)

# HTML 파싱하기
soup = BS(html, 'html.parser')
# print(soup.prettify())
# print(soup)

# tobody tr td-1, td-2
# print(soup.select('tbody > tr')[0].select_one('td').get_text().strip())
trs = soup.select('tbody > tr')
# 데이터 전체 저장 리스트
exchange_list = []
for tr in trs:
    # 하나의 통화 list로 저장
    one_exchange = []
    sale = tr.select_one('td.sale').get_text().strip()
    title = tr.select_one('td.tit').get_text().strip()
    exchange_list.append(f"{title},{sale}")
    # print(f"{title}: {sale}")
    # print('-'*30)
print(exchange_list)


# 폴더 만들기
base_path = 'exchange_data'
os.makedirs(base_path, exist_ok=True)
# 1. 파일명생성
getdate = datetime.now().strftime('%Y-%m-%d-%H') + '.csv'

with open(f"{base_path}/{getdate}", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(exchange_list)