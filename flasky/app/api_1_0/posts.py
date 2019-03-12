#coding=utf-8


from . import api
from flask import jsonify,request,g,abort,url_for,current_app
from .. import db
from ..decorators import permission_required
from .errors import forbidden
# from ..auth import auth

from ..models import Post,Permission

#文章资源的get请求的处理程序

#




#文章资源post请求的处理程序
@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, \
           {'Location': url_for('api.get_post', id=post.id, _external=True)}

#文章资源请求put的请求处理程序
@api.route('/posts/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and \
            not g.current_user.can(Permission.ADMINISTER):
        return forbidden('Insufficient permissions')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())


# #这个函数使用列表推导生成所有文章的JSON版本。
# @api.route('/posts/<int:id>')
# @auth.login_required
# def get_post(id):
#     post = Post.query.get_or_404(id)
#     return jsonify(post.to_json())
#
#
# #处理获取文章集合的请求
# @api.route('/posts/')
# @auth.login_required
# def get_posts_all():
#     posts = Post.query.all()
#     return jsonify({ 'posts': [post.to_json() for post in posts] })

# 分页文章资源
@api.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(
                                      page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                      error_out=False)
    posts = pagination.items
    prev = None
    print 'fdakjfddsakfjdsakljfd'
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1, _external=True)
        next = None
        print '1fdakjfddsakfjdsakljfd'

    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1, _external=True)
        print '2'


    print '3fdakjfddsakfjdsakljfd'

    return jsonify({
                     'posts': [post.to_json() for post in posts],
                     'prev': prev,
                     'next': next,
                     'count': pagination.total
                     })

# http --json --auth 836426094@qq.com:123 GET http://127.0.0.1:5000/api/vi.0/posts/
# http --json --auth 774213166@qq.com:123 GET http://127.0.0.1:5000/api/v1.0/posts/