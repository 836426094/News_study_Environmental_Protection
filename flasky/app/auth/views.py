#coding=utf-8


import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
sys.path.append('E:\\oldcomputer\\Ronhe\\flasky')
# print sys.path
from flask import render_template, redirect, request,url_for, flash,session,make_response,Response

from . import auth
from ..models import User,handle_mysql
from .forms import LoginForm, RegistrationForm,ChangePasswordForm
from flask_login import logout_user, login_required, login_user

g_user_datanum={'user':0}

from .forms import PasswordResetForm,PasswordResetRequestForm,ChangeEmailForm
#邮件认证
from flask_login import current_user
#
try:
    from ...app import db
    # from flask.ext.sqlalchemy import SQLAlchemy
    # db=SQLAlchemy()
except:

    try:from Ronhe.flasky.app import db
    except:
        from flask_sqlalchemy import SQLAlchemy
        db=SQLAlchemy()
handle_mysql=handle_mysql()

from ..email2 import yibu_send_email
from ..EMAILS import Email

send_email=Email()

#注册检查  检查用户提交的邮箱或者号码是否在多个网站中使用了
from .forms import check_data
@auth.route('/zcjc',methods=['get','post'])
def Registered_detection():
    form = check_data()
    if form.validate_on_submit():
        print form

        data=[
            ['1',u'京东',u'京东是中国的综合网络零售商,是中国电子商务领域受消费者欢迎和具有影响力的电子商务网站之一','https://www.jd.com/'],
            ['2',u'淘宝',u'淘宝网是亚太地区较大的网络零售、商圈，由阿里巴巴集团在2003年5月创立。淘宝网是中国深受欢迎的网购零售平台，拥有近5亿的注册用户数，每天有超过6000万的固定访客，同时每天的在线商品数已经超过了8亿件，平均每分钟售出4.8万件商品。','https://temai.taobao.com']
        ]
        return render_template('chayicha/chayicha_result.html', data=data)

    return render_template('auth/zcjc.html', form=form)



#注册
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # from Ronhe.flasky.app import db
    # from flask.ext.sqlalchemy import SQLAlchemy
    # db=SQLAlchemy()
    if form.validate_on_submit():
        # print 'register：',form.email.data,form.username.data,form.password.data
        # User.query.get(2)

        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data
                    )
        user.passwd=form.password.data

        try:
            db.session.add(user)
            db.session.commit()
            # token = user.generate_confirmation_token()
        except Exception,e:
            print  Exception,e
            db.session.rollback()
            # db.session.commit()

        # token = user.generate_confirmation_token()
        # #获得加密的token 问题 ：发现rollback之后 使用的token无效
        # text=render_template('auth/email/confirm.txt',user=user,token=token)
        # yibu_send_email(title=u'注册用户认证',text=text,to_userlist=[form.email.data])
        #
        # flash('A confirmation email has been sent to you by email.')

        return redirect(url_for('main.index'))
        # return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


#每次请求前运行  运行ping方法刷新用户访问时间
@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


#注册但是未确认邮箱的
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():#validate_on_submit()函数会验证表单数据，然后尝试登入用户。
        user0 = User.query.filter_by(email=form.email.data).first()  #查找用户  get()#all()#
        user=handle_mysql.find_user_data(form.email.data)
        print u'user',user #,user.password,user.email
        unum=int(str(form.email.data).replace('u','').replace('@qq.com',''))
        g_user_datanum['user']=unum
        global g_user_datanum
        print 'globle g_user_datanum:',g_user_datanum
        print form.password.data
        # print user.verify_password(form.password.data)
        # response=Response(url_for('crawlers.news'))
        # response.set_cookie('user',str(unum))
        # print response.data


        try:
            if user0 is not None and form.email.data==user[0][2] and form.password.data==user[0][3]:
                print user,form.remember_me.data
                login_user(user0, form.remember_me.data)
                session['email']=form.email.data

                # login_html=render_template('auth/login.html')



                # return redirect(request.args.get('next') or url_for('main.index'))#
                # return redirect(request.args.get('next') or url_for('crawlers.news'))#
                login_html=redirect(url_for('crawlers.news'))
                respo=make_response(login_html)
                respo.set_cookie('user',str(unum))
                print 'if_ check seccess'
                return respo#
            else:
                print 'check passwd filed to else'
                if user0 is not None and user0.verify_password(form.password.data):
                    login_user(user0, form.remember_me.data)
                    session['email']=form.email.data


                    # login_html=render_template('news/news.html')
                    # login_html=render_template('news/news.html')
                    login_html=redirect(url_for('crawlers.news'))
                    respo=make_response(login_html)
                    import datetime
                    outdate=datetime.datetime.today() + datetime.timedelta(days=1) ##超时时间

                    respo.set_cookie('user',str(unum),expires=outdate)
                    print 'else_ check seccess'


                    return respo


                    # return redirect(request.args.get('next') or url_for('main.index'))#
                    #
                    # return redirect(request.args.get('next') or url_for('crawlers.news'),Response=response)#

        except IndexError,e:
            print e,'other check way!'
            if user is not None and user0.verify_password(form.password.data):
                login_user(user0, form.remember_me.data)
                # return redirect(request.args.get('next') or url_for('main.index'))#
                login_html=render_template('auth/login.html')
                respo=make_response(login_html)
                respo.set_cookie('user',str(unum))
                print 'if_ check seccess'
                return respo

        #flash('Invalid username or password.')
        flash(u'账户或密码错误.')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()#调用Flask-Login中的logout_user()函数，删除并重设用户会话。随后会显示一个Flash消息，确认这次操作，再重定向到首页，这样登出就完成了。
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


#
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


#
@auth.route('/confirm')
@login_required
def resend_confirmation():

    token = current_user.generate_confirmation_token()
    # token = user.generate_confirmation_token()  #获得加密的token
    text=render_template('auth/email/confirm.txt',user=current_user,token=token)
    yibu_send_email(title=u'confirm',text=text,to_userlist=[current_user.email])

    # send_email(current_user.email, 'Confirm Your Account',
    #            'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


#更改密码认证
@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm() #创建form实例
    # from Ronhe.flasky.app import db
    # from flask.ext.sqlalchemy import SQLAlchemy
    # db=SQLAlchemy()
    if form.validate_on_submit():#如果表格不为空，执行下列语句
        if current_user.verify_password(form.old_password.data):#如果现在的用户旧密码验证正确，执行下列语句
            current_user.password = form.password.data#表格中的密码赋值给用户中的密码
            current_user.passwd=form.password.data
            # db.session.query(User).filter_by(email=session.get('email')).update({'password': form.password.data})
            try:
                db.session.add(current_user)#加入数据库会话，自动提交到数据库
                db.session.commit()
                flash('Your password has been updated.')
            except Exception,e:
                db.session.rollback()
                flash('Your password has  been updated.  (rollback) :'+str(Exception)+':'+str(e))
            return redirect(url_for('main.index'))

        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)


#重设密码
@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            text=render_template('auth/email/reset_password.txt',user=user,token=token)
            yibu_send_email(title=u'reset',text=text,to_userlist=[form.email.data])
            next=request.args.get('next')
            print next

            # send_email(user.email, 'Reset Your Password',
            #            'auth/email/reset_password',
            #            user=user, token=token,
            #            next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

#重设邮箱
@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)

#更改邮箱
@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)

            text=render_template('auth/email/change_email.txt',user=current_user,token=token)
            yibu_send_email(title=u'reset',text=text,to_userlist=[current_user.email])

            # send_email(new_email, 'Confirm your email address',
            #            'auth/email/change_email',
            #            user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)


@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))

