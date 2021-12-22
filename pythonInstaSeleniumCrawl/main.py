from selenium import webdriver
from bs4 import BeautifulSoup
import re
from selenium.webdriver.common.by import By
import time
import pandas as pd

# 좋아요 수가 200이 넘는 게시물의 본문 내용, 작성일자, 위치정보, 해시태그 가져오는 함수
def get_content(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    # 좋아요
    try:
        like = int(soup.select('a.zV_Nj')[0].text[4:-1])
    except:
        like = 0
    # 본문 내용
    try:
        content = soup.select('div.C4VMK > span')[0].text
    except:
        content = ' '
    # 해시태그
    tags = re.findall(r'#[^\s#,\\]+', content)
    # 작성일자
    date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10]
    # 위치
    try:
        place = soup.select('div.M30cS')[0].text
    except:
        place = ' '
    data = [content, date, like, place, tags]
    return data

# 다음 게시물 클릭하는 함수
def move_next(driver):
    driver.find_element(By.CSS_SELECTOR, "body > div._2dDPU.QPGbb.CkGkG > div.EfHg9 > div > div > div.l8mY4.feth3 > button > div > span > svg").click()
    time.sleep(5)

# 크롬 브라우저 연결하여 인스타그램 사이트 열기
instaFirstURL = 'https://www.instagram.com'
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get(url=instaFirstURL)
driver.implicitly_wait(time_to_wait=5)

# 인스타그램 로그인하기
id = "사용자 아이디"
password = "사용자 비밀번호"

driver.find_element(By.NAME, "username").send_keys(id)
driver.find_element(By.NAME,"password").send_keys(password)
driver.find_element(By.CSS_SELECTOR, "button.sqdOP.L3NKy.y3zKF").click()
driver.implicitly_wait(time_to_wait=10)

# "로그인 정보 저장 나중에 하기" 버튼 클릭하기
driver.find_element(By.CSS_SELECTOR, "div.cmbtv").click()
driver.implicitly_wait(time_to_wait=20)

# "알림 설정 나중에 하기" 버튼 클릭하기
driver.find_element(By.CSS_SELECTOR, "button.aOOlW.HoLwm").click()
driver.implicitly_wait(time_to_wait=20)

# 해시태그 검색창에 "맛집" 검색하기
instaHashtagUrl = "https://www.instagram.com/explore/tags/{}/".format("맛집")
driver.get(url=instaHashtagUrl)
driver.implicitly_wait(time_to_wait=15)

# 좌측 최상단 게시물 클릭하기
driver.find_element(By.CSS_SELECTOR, "div.v1Nh3.kIKUG._bz0w").click()
driver.implicitly_wait(time_to_wait=5)

# 결과 담을 리스트 results 초기화하기
results = []

# 수집할 게시물의 수를 변수 target에 설정하기
target = 100

# 크롤링하기
for i in range(target):
    try:
        data = get_content(driver)
        results.append(data)
        move_next(driver)
    except:
        time.sleep(5)
        move_next(driver)


# 결과를 데이터프레임으로 저장하기
results_df = pd.DataFrame(results)
results_df.columns = ['content', 'date', 'like', 'place', 'tags']
results_df = results_df[results_df.like > 200]
sorted_results_df = results_df.sort_values(by='like', ascending=False)
sorted_results_df.to_excel('hotFoodRestaurant.xlsx')

# 크롬 브라우저 닫기
driver.close()

