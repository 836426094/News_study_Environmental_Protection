#coding=utf-8

from ..models import User,AnonymousUser
# from flask.ext.httpauth import HTTPBasicAuth
from flask import g,jsonify
from flask_httpauth import HTTPBasicAuth
from .errors import unauthorized
auth = HTTPBasicAuth()
from . import api
from .errors import forbidden


# 生成认证令牌
@auth.verify_password
def verify_password(email, password):
    if email == '':
        g.current_user = AnonymousUser()#由于这个路由也在蓝本中，所以添加到before_request处理程序上的认证机制也会用在这个路由上。为了避免客户端使用旧令牌申请新令牌，要在视图函数中检查g.token_used变量的值，如果使用令牌进行认证就拒绝请求。这个视图函数返回JSON格式的响应，其中包含了过期时间为1小时的令牌。JSON格式的响应也包含过期时间。

        return True
    user = User.query.filter_by(email = email).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)

@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')



#在before_request处理程序中进行认证
#现在，API蓝本中的所有路由都能进行自动认证。而且作为附加认证，before_request处理程序还会拒绝已通过认证但没有确认账户的用户。
@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and \
             not g.current_user.confirmed:
        return forbidden('Unconfirmed account')

#生成认证令牌
@api.route('/token')
def get_token():#于这个路由也在蓝本中，所以添加到before_request处理程序上的认证机制也会用在这个路由上。为了避免客户端使用旧令牌申请新令牌，要在视图函数中检查g.token_used变量的值，如果使用令牌进行认证就拒绝请求。这个视图函数返回JSON格式的响应，其中包含了过期时间为1小时的令牌。JSON格式的响应也包含过期时间。

    if g.current_user.is_anonymous() or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})