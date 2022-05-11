# from main import * # main에 선언된 모든 값을 가져와요 , __init__ file에 선언된 라이브러리를 가져와 사용할 수 있습니다
# from flask import Blueprint

from flask import Flask, render_template, request, jsonify, Blueprint
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi
ca = certifi.where()\
    # ,tlsCAFile=ca

client = MongoClient('localhost',27017)
db = client.dbsparta

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

chart =soup.select('#body-content > div.newest-list > div > table > tbody > tr')

# 블루프린트 변수만들어요
# blueprint=Blueprint("mypage",__name__, url_prefix="/mypage")


#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number

# db가 없어서 크롤링 한 코드
for music in chart:
    a = music.select_one('td.info > a.title.ellipsis').text.strip()
    if a[0:3] == '19금':
        a = a[4:].strip()
    rank = music.select_one('td.number').text[:2].strip()
    cover = music.select_one('td:nth-child(3) > a > img')['src']
    singer = music.select_one('td.info > a.artist.ellipsis').text
    album = music.select_one('td.info > a.albumtitle.ellipsis').text
    doc = {'title': a,
           'rank': rank,
           'cover': cover,
           'singer': singer,
           'album': album}
    db.chart.insert_one(doc)

    print(rank)


# 로컬5000 부르면 메인페이지(테스트)를 불러와요
@app.route('/')
def home():
   return render_template('mainpagetest.html')


# @app.route('/musiclist', methods=['GET'])
# def web_musiclist_get():
#          music_list = list(db.chart.find({}, {'_id': False}))
#          return jsonify({'chart': music_list})


# @app.route('/test', methods=['POST'])
# def test_post():
#         title_receive = request.form['title_give']
#         print(title_receive)
#         return jsonify({'result':'success', 'msg': '이 요청은 잘받았어요!'})

# 마이페이지로 이동해요
@app.route('/mypage')
def mypage():
    return render_template('mypage.html')

# db에 들어온 정보들을 플레이리스트로 저장해서 넘겨줘요
@app.route('/playlist', methods=['GET'])
def web_playlist_get():
    play_list = list(db.chart.find({}, {'_id': False}))
    return jsonify({'playlist': play_list})


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)


