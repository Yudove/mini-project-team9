from main import * # main에 선언된 모든 값을 가져와요 , __init__ file에 선언된 라이브러리를 가져와 사용할 수 있습니다
from flask import Blueprint

app = Flask(__name__)

SECRET_KEY = 'likeMusic'
blueprint = Blueprint("mypage", __name__, url_prefix="/")

# 마이페이지로 이동해요
@blueprint.route('/mypage')
def mypage():
    token_receive = request.cookies.get('mytoken')
    id = request.args.get('id')

    # 로그인한 사용자의 id를 가져와 playlist 목록 가져오기
    mypli = list(db.mymusic.find({'id':id}))

    if token_receive:
        # mypage.html로 token, id, mypli 값을 보내겠다. -> html에서 {{ id }} 이런 식(파이썬 코드)으로 가져다 쓸 수 있음.
        return render_template('mypage.html', token=token_receive, id=id, mypli=mypli)
    return render_template('loginForm.html')

# db에 들어온 정보들을 플레이리스트로 저장해서 넘겨줘요
@blueprint.route('/playlist', methods=['GET'])
def web_playlist_get():
    play_list = list(db.chart.find({}, {'_id': False}))
    return jsonify({'playlist': play_list})
