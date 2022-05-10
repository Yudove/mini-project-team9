from flask import Flask, render_template, request, jsonify
detail = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.p2v10.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


# 코딩 시작


@detail.route('/review')
def home():
    return render_template('detail.html')


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