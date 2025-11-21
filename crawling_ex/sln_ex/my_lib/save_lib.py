import os
from datetime import datetime
import csv

# 데이터 저장 함수 정의부
def save_data(data_keyword, head, movie_lists):

   now = datetime.now()
   timestamp = now.strftime("%Y-%m-%d-%H")
   folder = f"{data_keyword}_datas"
   filename = f"{data_keyword}{timestamp}.csv"
   filepath = os.path.join(folder, filename)
   os.makedirs(folder, exist_ok=True)
      # csv 저장
   with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        # 1차원 리스트 저장
        writer.writerow(head)
        # 2차원 리스트로ㅗ 만들어서 저장(수집한 데이터)
        writer.writerows(movie_lists)
   print("CSV 저장 완료:", filepath)