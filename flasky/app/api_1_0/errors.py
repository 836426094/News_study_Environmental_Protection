#coding=utf-8
from flask import jsonify,request


from Ronhe.flasky.app import ValidationError,db
from .import api
from ..models import Post

def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response

def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


#API蓝本中403状态码的错误处理程序
def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

@api.errorhandler(ValidationError)#这里使用的errorhandler修饰器和注册HTTP状态码处理程序时使用的是同一个，只不过此时接收的参数是Exception类，只要抛出了指定类的异常，就会调用被修饰的函数。注意，这个修饰器从API蓝本中调用，所以只有当处理蓝本中的路由时抛出了异常才会调用这个处理程序。
def validation_error(e):
    return bad_request(e.args[0])


#
# @api.route('/posts/', methods=['POST'])
# def new_post():
#     post = Post.from_json(request.json)
#     post.author = g.current_user
#     db.session.add(post)
#     db.session.commit()
#     return jsonify(post.to_json())