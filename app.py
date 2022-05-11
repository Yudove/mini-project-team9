import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('mongodb+srv://slldfg8:qaz741852@cluster0.2uvii.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

musics =soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for music in musics:
    a = music.select_one('td.info > a.title.ellipsis').text.strip()
    if a[0:3] == '19금': a = a[4:].strip()
    singer = music.select_one('td.info > a.artist.ellipsis').text
    album = music.select_one('td.info > a.albumtitle.ellipsis').text
    cover = music.select_one('td:nth-child(3) > a > img')['src']

    doc = {'title': a,
           'singer': singer,
           'album': album,
           'cover':cover}
    db.musics.insert_one(doc)



@app.route('/')
def home():
   return render_template('mainpage.html')

@app.route('/index')
def mypage():
   return render_template('index.html')

@app.route('/detail')
def review():
    return render_template('detail.html')






@app.route('/musiclist', methods=['GET'])
def web_musiclist_get():
         music_list = list(db.musics.find({}, {'_id': False}))

         return jsonify({'musics': music_list})


@app.route('/test', methods=['POST'])
def test_post():
        title_receive = request.form['title_give']
        print(title_receive)
        return jsonify({'result':'success', 'msg': '이 요청은 잘받았어요!'})





if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)



#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td:nth-child(3) > a > span
#body-content > div.newest-list > div > table > tbody > tr:nth-child(2) > td:nth-child(3) > a > span