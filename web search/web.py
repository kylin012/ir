# 使用flask构造web界面

from flask import Flask,render_template,request
from module.search import *
import requests
import json
import sqlite3

app = Flask(__name__)
es = Elasticsearch()
ss = hlsearch()

users = {"admin":{"password":"admin", "college":"计算机"}}
hist = {"admin":[]}
collegeq = []

# 初始化页面
@app.route('/')
def initpage():
    return render_template('search.html')

# 搜索页面
@app.route('/search',methods=["GET"])
def search():
    seat = searchtype()
    seat.query = request.values.get('query', default='', type=str)
    seat.st_date = request.values.get('date', default='2000-01-01', type=str)
    seat.fields = request.values.getlist('fields', type=str)
    # 没有选择域的情况下默认包含所有域
    if not seat.fields:
        seat.fields = ['title', 'text', 'mtext']
    seat.from1 = request.values.get('from1', default=0, type=int)
    seat.size1 = request.values.get('size1', default=10, type=int)+1
    seat.method = request.values.get('method', default='match', type=str)
    seat.url = request.values.get('url', default='http', type=str)
    uname = request.values.get('uname')
    his = None
    # 添加一条针对用户学院的推荐
    if uname in users and collegeq == []:
        seat2 = searchtype()
        seat2.query = users[uname]['college']
        seat2.st_date = '2000-01-01'
        seat2.fields = ['title', 'text', 'mtext']
        seat2.from1 = 0
        seat2.size1 = 2
        seat.method = 'match'
        seat.url = 'http'
        res2 = ss.highlight(seat2)
        collegeq.append(res2['pages'][0]['rawtitle'])

    if uname in users:
        seat.college = users[uname]['college']
    res = ss.highlight(seat)
    # 插入记录，可能增加一条针对历史搜索的推荐
    histitle = ''
    if uname in users:
        if seat.query != '':
            hist[uname].insert(0, {"query": seat.query, "firsttitle": res['pages'][0]['rawtitle']})
        # 查询日志最多显示5条记录
        his = hist[uname][:5]
        if len(hist[uname])>1:
            histitle = hist[uname][1]['firsttitle']
    # 增加一条针对锚文本的推荐
    mtexts = res['pages'][0]['rawmtext'].split(",")
    if len(mtexts)>5:
        raw = mtexts[4]
    else:
        raw = mtexts[-1]
    # 增加一条针对本次搜索的推荐
    curr = res['pages'][-1]['rawtitle']
    # 在json文件中存储用户信息和对应的查询日志
    json.dump(users, open('userinfo.json', 'w'))
    json.dump(hist, open("querylog.json", 'w'))
    return render_template('search.html', pages=res['pages'][:-1], rawtitle=curr, rawmtext=raw, query=seat.query, user=uname, history=his, history2=histitle, collegeq=collegeq)

# 匹配文字高亮
def hlsearch(query, html):
    url = "http://localhost:9200/_analyze"
    index1 ={
        "analyzer": "ik_smart",
        "text": query
    }
    res = requests.post(url, json=index1)
    js = json.loads(res.text)
    keywords=[token['token'] for token in js["tokens"]]
    for keyword in keywords:
        html = html.replace(keyword,'<font style="background: #ff9632">'+keyword+'</font>')
    return html

# 网页快照
@app.route('/snapshot', methods=['GET'])
def quickshot():
    url = request.values.get('url')
    query = request.values.get('query')
    conn = sqlite3.connect("nkuinfo\\nkuinfo\\spiders\\mysql.sqlite")
    sql_get_restext = "SELECT p_restext FROM page WHERE p_id ==(SELECT r_id FROM rank WHERE url==?)"
    if url!='http':
        res = conn.execute(sql_get_restext,(url,)).fetchone()[0]
        res.replace('\r\n', '')
        hl = hlsearch(query, res)
        return hl
    return ''

# 注册
@app.route('/signup', methods=['GET'])
def signup():
    uname = request.values.get('uname',type=str)
    password = request.values.get('password')
    college = request.values.get('college')
    if uname =='':
        return "用户名不可为空"
    if uname in users:
        return "该用户名已被占用，请更换用户名"
    users[uname]={
        "password": password,
        "college": college,
    }
    hist[uname]=[]
    return render_template('search.html', pages=[], query="", rawtitle="", user=uname,history=[])

# 登录
@app.route('/login', methods=['GET'])
def login():
    uname = request.values.get('uname')
    password = request.values.get('password')
    if uname not in users:
        return "用户不存在！"
    if password != users[uname]['password']:
        return "密码错误"
    return render_template('search.html', pages=[], query='', rawtitle="", user=uname, history=hist[uname][:5])

if __name__ == '__main__':
    users = json.load(open("userinfo.json"))
    hist = json.load(open("querylog.json"))
    app.run()
