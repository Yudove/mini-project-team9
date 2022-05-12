from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import certifi
import jwt
import datetime
import hashlib

# 회원가입/로그인

client = MongoClient('mongodb+srv://test:sparta@cluster0.p2v10.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

SECRET_KEY = 'likeMusic'

#__init__.py 파일에선 app 객체를 선언하고 각종 모듈, 데이터베이스, 블루프린트 등 값을 설정한다
from . import login       #from . import login : login.py의 내용을 호출하겠다.
from . import detail
from . import main
from . import mypage

app = Flask(__name__)

app.register_blueprint(login.blueprint)
app.register_blueprint(detail.blueprint)
app.register_blueprint(main.blueprint)
app.register_blueprint(mypage.blueprint) # (detail.blueprint) detail.py에서 사용할 blueprint객체를 blueprint로 설정할거야
