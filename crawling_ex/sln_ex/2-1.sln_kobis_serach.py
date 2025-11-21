# 1. 필요한 라이브러리 로딩
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time  


# 2. 크롬브라우저 옵션 정의
options = webdriver.ChromeOptions()             # 옵션 설정 객체 생성
options.add_argument("window-size=1000,1000")   # 브라우저 크기 설정(가로 x 세로)
options.add_argument("--no-sandbox")              # 샌드박스 사용 안하겠다. 텝별로 분리하겠다. 
options.add_argument("--disable-dev-shm-usage")  # 메모리 부족 방지
# options.add_argument("headless")              # 크롬 창을 안뜨게함.
# options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 3. 크롬 웹드라이브를 통한 크롬브라우저 객체 생성
# 방법1 자동으로 다운로드(현재 크롬 브라우저 버전에 맞게)
# ChromeDriver 경로를 지정하는 Service 객체 생성
# service = Service(ChromeDriverManager().install())

# 방법2 *방법1이 안될 때 메뉴얼하게 다운로드 받아서 지정해야 함.
# 로컬에 다운로드한 chromedriver.exe 경로 지정
# https://googlechromelabs.github.io/chrome-for-testing/
# 메뉴얼하게 지정하는 방법
service = Service("chromedriver_142/chromedriver.exe")

# 크롬 브라우저 객체 생성됨, chrome은 브라우저 객체 식별자
chrome = webdriver.Chrome(service=service, options=options)

# 4. 데이터 수집할 웹 주소
url = "https://www.kobis.or.kr/kobis/business/stat/boxs/findRealTicketList.do"

time.sleep(3) # 간단한 delay, 파이썬 라이브러리
chrome.get(url)

# 지정한 요소가 브라우저에 로딩 될 때까지 기다림, 최대 10초
wait = WebDriverWait(chrome, 10) 
def find(wait, css_selector):
  return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

# 5. 데이터 수집할 부분에 대한 검색 액션
try:
    ## 한국 영화만 선택, 해외 체크박스 해제 액션
    # 셀렉터 지정방법
    # ul.list_idx li input#repNationNoKor 또는 
    # ul.list_idx li label[for = 'repNationNoKor']
    # find(wait, '셀렉터')
    # 지정 셀렉터 요소가 로딩될 때까지 기다리고, 로딩되면 요소 리턴
    # ele = find(wait, 'ul.list_idx li input.chk_comm')
    ele = find(wait, 'label[for = repNationNoKor]')
    ele.click()

    # ele = find(wait, 'input#repNationNoKor')
    # 로딩된 요소 클릭
    btn = find(wait, '.wrap_btn button.btn_blue')
    btn.click()

    # 조회된 데이터에서 필요한 데이터 수집
    # 각 영화 데이터를 list로 추출(tbody tr을 목록으로 추출)
    time.sleep(2) # 크롤링할 데이터 요소가 로딩될 때까지 잠시 기다리기
    # 'table.tbl_comm tbody tr' 해당 셀렉터의 모든 요소를 추출함
    items = chrome.find_elements(By.CSS_SELECTOR,'table.tbl_comm tbody tr')
    # print(items)
    print("영화 제목 | 개봉일 | 예매매출 | 관객수")
    movie_lists = []
    for item in items:
       # 하나의 tr안에서 td가 두번째인 요소의 텍스트 추출
       title = item.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text
       # 하나의 tr안에서 td가 세번째인 요소의 텍스트 추출
       open_date = item.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text
       if not open_date:
          open_date = '-'
       reserve_rate = item.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.rstrip("%")
       sales_price = item.find_element(By.CSS_SELECTOR, "td:nth-child(7)").text.replace(",","")
       print(f"{title} | {open_date} | {reserve_rate} | {sales_price}")
       movie_lists.append([title, open_date, reserve_rate,sales_price])
       print(movie_lists)
       
    #    print(f"{title} | {open_date}")
    # 조회버튼 로딩되면 클릭하기 
    # btn = find(wait, '')
    time.sleep(5)
except Exception as e:
   print('error',e)

print('-'*30)
chrome.close() # tab 모두 종료
chrome.quit() # tab 모두 종료
import os
from datetime import datetime
def save_data(filepath,head, movie_lists):
    import csv
   
    # csv 저장
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        # 1차원 리스트 저장
        writer.writerow(["영화제목","개봉일","예매매출액","예매관람수"])
        # 2차원 리스트로ㅗ 만들어서 저장(수집한 데이터)
        writer.writerows(movie_lists)

    print("CSV 저장 완료:", filepath)

 # 폴더 / 파일명 설정
folder = "movie_datas"
# 파일 저장 함수 호출
# 매번 바뀌는 값이 찾기
head = ["영화제목","개봉일","예매매출액","예매관람수"]
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d-%H")   # → 2025-11-17-13 형태
# 폴더 자동 생성
os.makedirs(folder, exist_ok=True)
# 폴더 / 파일명 설정
folder = "movie_datas"
filename = f"movie_{timestamp}.csv"
# movie_datas/2025-112112
filepath = os.path.join(folder, filename)
save_data()

# time.sleep(2) # 간단한 delay, 파이썬 라이브러리
# items = chrome.find_elements(By.CSS_SELECTOR, ".tbl_comm tbody tr")

# # selenium 방법으로 데이터 수집
# for item in items:
#   title = item.find_element(By.CSS_SELECTOR, "td.tal a").text
#   open_date = item.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
#   reserve_rate = item.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.rstrip("%")
#   sales_price = item.find_element(By.CSS_SELECTOR, "td:nth-child(7)").text.replace(",","")
#   print(f"{title} | {open_date} | {reserve_rate} | {sales_price}")


#### 다양한 엘리먼트 얻는 방법
# 참고 : https://wikidocs.net/177133