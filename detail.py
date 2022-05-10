from flask import Flask, render_template, request, jsonify
detail = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.p2v10.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')
musics = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

#body-content > div.newest-list > div > table > tbody > tr:nth-child(1)

#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.albumtitle.ellipsis
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td:nth-child(3) > a > img

for music in musics:
    a = music.select_one('td.info > a.title.ellipsis').text
    singer = music.select_one('td.info > a.artist.ellipsis').text
    album = music.select_one('td.info > a.albumtitle.ellipsis').text
    cover = music.select_one('td:nth-child(3) > a > img')['src']

    doc = {
        'title': a,
        'singer': singer,
        'album': album,
        'cover': cover
    }
    db.musics.insert_one(doc)

# 코딩 시작


@detail.route('/reviewform')
def home():
    return render_template('detail.html')

@detail.route('/detail', methods=['GET'])
def music_get():
    music_total = list(db.musics.find({}, {'_id': False}))

    return jsonify({'musics':music_total})

@detail.route('/review', methods=['POST'])
def test_post():

    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']
    doc = {
        'comment':comment_receive,
        'star':star_receive
    }
    db.review.insert_one(doc)
    return jsonify({'msg': '리뷰가 등록되었습니다.'})

@detail.route('/review', methods=['GET'])
def test_get():
    review_total = list(db.review.find({}, {'_id': False}))

    return jsonify({'reviews':review_total})

if __name__ == '__main__':
    detail.run('0.0.0.0', port=5000, debug=True)