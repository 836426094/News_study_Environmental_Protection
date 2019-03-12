#coding=utf-8
from flask import Flask, request, Response

app = Flask(__name__)


@app.route('/')
def hello_world():
    resp = Response("saber's home")
    resp.set_cookie('username', 'saber')
    return resp


@app.route('/del/')
def delete_cookie():
    resp = Response("Saber's home 2")
    resp.delete_cookie('username')
    return resp

if __name__ == '__main__':
    app.run(debug=True)