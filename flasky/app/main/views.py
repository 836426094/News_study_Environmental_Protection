#coding=utf-8


from datetime import datetime
from flask import render_template, session, redirect, url_for, flash,request,abort,current_app,jsonify
from flask_mail import Mail  #初始化mail
from flask_mail import Message
from . import main
from . forms import NameForm,EditProfileForm,EditProfileAdminForm, PostForm,CommentForm
from .. import db
from .. models import User,Role,Post,Comment
from flask_login import login_required,current_user  #登入验证  路由保护
from ..models import Permission
from ..decorators import admin_required, permission_required
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# @main.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm() #渲染表单使用
#     if form.validate_on_submit():
#         # ...
#         return redirect(url_for('index'))
#     return render_template('index.html',
#                            form=form, name=session.get('name'),
#                            known=session.get('known', False),
#                            current_time=datetime.utcnow())





#“关注”路由和视图函数
@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))

#“关注者”路由和视图函数
@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)

@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)



# #处理博客文章的首页路由
# @main.route('/', methods=['GET', 'POST'])
# def index():
#     form = PostForm()
#     if current_user.can(Permission.WRITE_ARTICLES) and \
#             form.validate_on_submit():
#         # print 'fdsakjfdsljf'
#         post = Post(body=form.body.data,
#                     author=current_user._get_current_object())  #这个有点不太了解
#         db.session.add(post)
#         flash(u'发布成功！')
#         return redirect(url_for('main.index'))
#     posts = Post.query.order_by(Post.timestamp.desc()).all()  #按照时间进行降序排列
#     return render_template('index.html', form=form, posts=posts,name=session.get('name'),
#                            known=session.get('known', False),
#                            current_time=datetime.utcnow())

# 重定向至crawlers.news
@main.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('crawlers.news'))


#处理博客文章的论坛
@main.route('/luntan', methods=['GET', 'POST'])
def luntan():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        # print 'fdsakjfdsljf'
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        flash(u'发布成功！')
        return redirect(url_for('main.luntan'))

    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    page = request.args.get('page', 1, type=int)#渲染的页数从请求的查询字符串（ request.args）中获取，如果没有明确指定，则默认渲
# 染第一页。参数 type=int 保证参数无法转换成整数时，返回默认值。
    #paginate() 方法的返回值是一个 Pagination 类对象，这个类在 Flask-SQLAlchemy 中定义。
    # 这个对象包含很多属性， 用于在模板中生成分页链接，因此将其作为参数传入了模板。
    print page
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items #当前页中的记录
    return render_template('luntan.html', form=form, posts=posts,name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.utcnow(),pagination=pagination)


#文章固定链接
@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


# 编辑博客文章的路由
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('main.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post_v2.html', form=form)

#管理评论的路由 开始
@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)
@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))

@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))
#管理评论的路由 结束


#用户权限测试
@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"

@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "For comment moderators!"

#用户资料界面路由
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)

#资料编辑器开始
#普通用户编辑器
@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    #为表单设置初始值
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

#管理员资料编辑路由
@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)



#API

#请求未找到
@main.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


































@main.route('/form',methods=['GET','POST'])
@login_required
def nameform():
    form=NameForm() #
    if form.validate_on_submit():#返回ture or false
        old_name=session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')

        print '-----',old_name,form.name.data
        user=User.query.filter_by(username=form.name.data).all()
        print u'查询结果为：',user
        if user is None or len(user)==0:
            user=User(username=form.name.data,email=form.Em.data,password=form.passwd.data,role_id=3)
            print user
            print str(user)
            db.session.add(user)
            # db.session.commit()
            session['known']=False
            # if app.config['FLASKY_ADMIN']:
            # if form.Em.data:
            #     send_email(form.Em.data, 'New User',
            #                'mail/new_user', user=user)
            print 'insert ok'
        else:
            session['known'] = True
        session['name']=form.name.data
        session['passwd']=form.passwd.data
        # session['textcont']=form.textcont.data
        session['Em']=form.Em.data
        print session
        return redirect(url_for('main.user',name=session['name'],_external=True))  #注意 注意 main.ys

    return render_template('nameform.html',form=form,name=session.get('name'),
                           known=session.get('known',False))
