from main import *
from flask import Blueprint


blueprint = Blueprint("detail", __name__, url_prefix="")

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}





# 토큰 디코드
SECRET_KEY = 'likeMusic'

import jwt



# 코딩 시작


@blueprint.route('/detail')
def detail():
    token_receive = request.cookies.get('mytoken')
    return render_template('detail.html', token=token_receive)



@blueprint.route('/review', methods=['POST'])
def test_post():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        comment_receive = request.form['comment_give']
        star_receive = request.form['star_give']
        doc = {
            'id': user_info['id'],
            'comment': comment_receive,
            'star': star_receive
        }
        db.review.insert_one(doc)
        return render_template('detail.html', id=user_info["id"])
    except jwt.exceptions.DecodeError:
        return jsonify({'result':'fail', 'msg':'로그인 페이지로 이동합니다.'})



@blueprint.route('/review', methods=['GET'])
def test_get():
    review_total = list(db.review.find({}, {'_id': False}))
    return jsonify({'reviews':review_total})
