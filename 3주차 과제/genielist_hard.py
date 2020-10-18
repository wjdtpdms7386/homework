import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) : 1순위 노래 리스트의 위치
# body-content > div.newest-list > div > table > tbody > tr:nth-child(2) : 2순위 노래 리스트의 위치

songs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info : 1순위 영화 전체 위치
# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number : 순위
# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis : 제목명
# body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis : 가수이름

# print(songs[11].select_one('td.number').text.strip().split('\n')[0])  # 순위
# print(songs[11].select_one('td.info > a.title.ellipsis').text.strip())  # 제목명
# print(songs[11].select_one('td.info > a.artist.ellipsis').text.strip())  # 가수이름

# songs (tr들) 의 반복문을 돌리기

for song in songs:

    a_rank = song.select_one('td.number').text.strip().split('\n')[0]
    a_title = song.select_one('td.info > a.title.ellipsis').text.strip()
    a_singer = song.select_one('td.info > a.artist.ellipsis').text.strip()
    print(a_rank, a_title, a_singer)

    doc = {
        'rank': a_rank,
        'title': a_title,
        'singer': a_singer
    }
    db.hwsongs.insert_one(doc)
