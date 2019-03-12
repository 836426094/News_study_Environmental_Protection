#coding=utf-8
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# from flask_login import UserMixin  #这个是为了保持登入验证的

#操作mysql
import pymysql

from datetime import datetime
import hashlib
from sqlalchemy.exc import IntegrityError  #数据库错误
#确认账户
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,request,url_for
# from ..app.exceptions import ValidationError
from flask_login import UserMixin, AnonymousUserMixin#（检查用户是否指定权限）

from . import db, login_manager
from markdown import markdown  #在服务器中处理富文本
import bleach   #在服务器中处理富文本

from random import seed, randint
# import forgery_py
# from ..app.exceptions import ValidationError
# from app.exceptions import ValidationError
# try:
#     from ..app.exceptions import ValidationError
# except:
#     from
# #     from News_study_Environmental_Protection.flasky.app.exceptions import ValidationError

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DECIMAL, Enum, Date, DateTime, Time, Text
from sqlalchemy.dialects.mysql import LONGTEXT


allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p','div','ul','ol','hr','table','tbody','td',
                        'img','blockquote','s','pre','/img'
                        ]

#权限常量
class Permission:
    FOLLOW = 0x01  #
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic') #一对多的关系模型

    @staticmethod
    def insert_roles():  #在数据库中创建角色
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

class Dailiips(db.Model):
    __tablename__ = 'xiciips'
    id=db.Column(db.Integer, primary_key=True)
    ip=db.Column(db.String(32))
    port=db.Column(db.String(32))
    adress=db.Column(db.String(32))
    anonymous=db.Column(db.String(32))
    types=db.Column(db.String(32))

    speed=db.Column(db.String(32))
    Connection_time=db.Column(db.String(32))
    Survival_time=db.Column(db.String(32))
    validation_time=db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # types=db.Column(db.text)

#



class Status(db.Model):
    __tablename__ = 'status'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(10))
    status=db.Column(db.Boolean)
    #自定义的
    @staticmethod
    def change_status(name):
        data=Status.query.filter_by(name=name).first()
        if data is None:
            db.session.add(name=name,status=True)
            return True  #current_user.password
        else:
            # print u'status',data.status
            if data.status == False:
                data.status = True
                db.session.add(data)
                return True
            else:
                return True
    @staticmethod
    def check_status(name):
        data=Status.query.filter_by(name=name).first()
        if data is None:
            db.session.add(name=name,status=False)
            return False  #current_user.password
        else:
            # print u'status',data.status
            if data.status == False:
                # self.status = True
                # db.session.add(self)
                return False
            else:
                return True
        # db.session.add(self)
        # db.session.flush()


    def confirm(self, token):
        print token
        #confirm.txt()方法检验令牌，如果检验通过，则把新添加的confirmed属性设为True。
        #除了检验令牌，confirm.txt()方法还检查令牌中的id是否和存储在current_user中的已登录用户匹配。如此一来，即使恶意用户知道如何生成签名令牌，也无法确认别人的账户
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception,e:
            print u'检验token失败',Exception,e
            return False
        if data.get('confirm.txt') != self.id:
            print u'检验token失败  data.get(confirm.txt) != self.id:'
            return False
        self.confirmed = True
        db.session.add(self)
        print u'检验令牌成功！'
        return True

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body_html = db.Column(db.Text)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')


    # 在Post模型中处理Markdown文本  on_changed_body函数把body字段中的文本渲染成HTML格式，结果保存在body_html中，自动且高效地完成Markdown文本到HTML的转换。
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        # allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
        #                 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
        #                 'h1', 'h2', 'h3', 'p','div','ul','ol','hr','table','tbody','td',
        #                 'img','blockquote','s','pre','/img'
        #                 ]
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))




    #用来生成大量的虚拟信息  已测试分页
    # (venv) $ python manage_old.py shell
    # >>> User.generate_fake(100)
    # >>> Post.generate_fake(100)
    # @staticmethod
    # def generate_fake(count=100):
    #
    #
    #     seed()
    #     user_count = User.query.count()
    #     for i in range(count):
    #         u = User.query.offset(randint(0, user_count - 1)).first()  #每次都获取一个不同的用户
    #         p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
    #                                           timestamp=forgery_py.date.date(True),author_id=u.id)
    #         db.session.add(p)
    #         try:
    #             db.session.commit()
    #         except IntegrityError:
    #             db.session.rollback()

    #把文章转化成json格式的序列化字典
    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id,
                              _external=True),
            'comments': url_for('api.get_post_comments', id=self.id,
                                _external=True),
            'comment_count': self.comments.count()
        }
        return json_post

    #从json格式的数据创建一篇博客文章
    # @staticmethod
    # def from_json(json_post):
    #     body = json_post.get('body')
    #     if body is None or body == '':
    #         raise ValidationError('post does not have a body')
    #     return Post(body=body)


db.event.listen(Post.body, 'set', Post.on_changed_body)

#关注表模型实现
class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


#评论模型
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):

        # allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
        #                 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
        #                 'h1', 'h2', 'h3', 'p','div','ul','ol','hr','table','tbody','td',
        #                 'img','blockquote','s','pre'
        #                 ]
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

db.event.listen(Comment.body, 'set', Comment.on_changed_body)

# 在Flask-SQLAlchemy中，Model是对SQLAlchemy的Base的包装,
# 在Flask-SQLAlchemy中，我们将Base改为db.Model.
class User(UserMixin,db.Model):#UserMixin,
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True)
    email = db.Column(db.String(320), unique=True)
    passwd = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(1000))

    name = db.Column(db.String(64))  #用户的真实姓名
    location = db.Column(db.String(64)) #所在地
    about_me = db.Column(db.Text())   #自我介绍  该类型不需要指定最大长度
    member_since = db.Column(db.DateTime(), default=datetime.utcnow) #注册日期
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)  #最后访问日期

    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id')) #添加给User模型的role_id列被定义为外键，且建立关系。db.ForeignKey()的参数roles.id指定的列应该理解为在roles表的行中持有id值的列
    avatar_hash = db.Column(db.String(32)) #存储用户头像
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    #用户关注的
    followed = db.relationship('Follow',
                            foreign_keys=[Follow.follower_id],
                            backref=db.backref('follower', lazy='joined'),
                            lazy='dynamic',
                            cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                            foreign_keys=[Follow.followed_id],
                            backref=db.backref('followed', lazy='joined'),
                            lazy='dynamic',
                            cascade='all, delete-orphan')

    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    #关注关系的辅助方法 开始
    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    #获得所有关注用户的文章
    @property
    def followed_aposts(self):
        return Post.query.join(Follow, Follow.followed_id == Post.author_id)\
            .filter(Follow.follower_id == self.id)
    #关注关系的辅助方法 结束



    #赋予角色
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        # 使用缓存的MD5散列值生成Gravatar URL
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    # 使用缓存的MD5散列值生成Gravatar URL 用户头像 生成Gravatar URL
    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)


    #检查用户是否有指定的权限开始

    def can(self, permissions): #can()方法在请求和赋予角色这两种权限之间进行位与操作。如果角色中包含请求的所有权限位，则返回True，表示允许用户执行此项操作。
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    #检查管理员权限的功能经常用到，因此使用单独的方法is_administrator()实现。出于一致性考虑，我们还定义了AnonymousUser类，并实现了can()方法和is_administrator()方法。
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def is_MODERATE_COMMENTS(self):
        return self.can(Permission.MODERATE_COMMENTS)
    #检查用户是否有指定的权限结束

     #刷新用户访问的最后时间

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        # db.session.commit()

    #生成令牌
    def generate_confirmation_token(self, expiration=3600):
        #generate_confirmation_token()方法生成一个令牌，有效期默认为一小时。
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm.txt': self.id})

    # 检验令牌
    def confirm(self, token):
        print token
        #confirm.txt()方法检验令牌，如果检验通过，则把新添加的confirmed属性设为True。
        #除了检验令牌，confirm.txt()方法还检查令牌中的id是否和存储在current_user中的已登录用户匹配。如此一来，即使恶意用户知道如何生成签名令牌，也无法确认别人的账户
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception,e:
            print u'检验token失败',Exception,e
            return False
        if data.get('confirm.txt') != self.id:
            print u'检验token失败  data.get(confirm.txt) != self.id:'
            return False
        self.confirmed = True
        db.session.add(self)
        print u'检验令牌成功！'
        return True


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter   #注册认证步骤 1
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    #认证
    def verify_password(self, password):
        # print 'verify:',password
        # print self.password_hash
        # print check_password_hash(self.password_hash, password)
        return check_password_hash(self.password_hash, password)

    #自定义的
    def save(self,user):
        if self.query.filter_by(email=user.email).first() is not None:
            return False  #current_user.password
        # self.email = user.email
        self.password = user.password
        # self.avatar_hash = hashlib.md5(
        #     self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

        # db.session.add(self)
        # db.session.flush()


    #验证重设密码
    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})
    #重设密码
    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True
    #验证重设邮件
    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    #重设邮件
    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False

        self.email = new_email
        self.avatar_hash = hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    #把用户转化成json格式的序列化字典
    def to_json(self):
        json_user = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts': url_for('api.get_user_posts', id=self.id, _external=True),
            'followed_posts': url_for('api.get_user_followed_posts',
                                      id=self.id, _external=True),
            'post_count': self.posts.count()
        }
        return json_user


    def __repr__(self):
        return '<User %r>' % self.username

    #用来生成大量的虚拟信息  已测试分页
    # (venv) $ python manage_old.py shell
    # >>> User.generate_fake(100)
    # >>> Post.generate_fake(100)
    @staticmethod
    def generate_fake(count=100):

        from random import seed
        import forgery_py #生成虚拟信息

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                                                            username=forgery_py.internet.user_name(True),
                                                            password=forgery_py.lorem_ipsum.word(),
                                                            confirmed=True,
                                                            name=forgery_py.name.full_name(),
                                                            location=forgery_py.address.city(),
                                                            about_me=forgery_py.lorem_ipsum.sentence(),
                                                            member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


#检查用户是否有指定的权限开始
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser
#检查用户是否有指定的权限结束

#当登陆成功后，该函数会自动从会话中存储的用户 ID 重新加载用户对象。它应该接受一个用户的 unicode ID 作为参数，并且返回相应的用户对象。
# 加载用户的回调函数接收以Unicode字符串形式表示的用户标识符。如果能找到用户，这个函数必须返回用户对象；否则应该返回None。

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

import os
sqlconfig_filepath=os.getcwd()+'\\sql_config.txt'

# print sqlconfig_filepath
try:
    print sqlconfig_filepath
    sqlconfig={}
    f=open(sqlconfig_filepath,'r')
    lines=f.readlines()
    for l in lines:
        # print lines.index(l),l
        try:
            lsplit=l.strip().split('=')
            sqlconfig[lsplit[0]]=lsplit[1]
        except:continue
    f.close()
    print sqlconfig
    print 'sqlconfig read success'
except:
    sqlconfig={u'passwd': u'123456', u'host': u'127.0.0.1', u'charset': u'utf8', u'db': u'car_market', u'user': u'bian'}
    # sqlconfig={host='127.0.0.1',user='bian',passwd='123456',db='car_market',charset='utf8'}
    conf='''host=127.0.0.1
user=bian
passwd=123456
db=car_market
charset=utf8'''
    f=open(sqlconfig_filepath,'w+')
    f.write(conf)
    f.close()
    print 'sqlconfig create success'




class handle_mysql():
    def __init__(self):
        # self.conn=pymysql.connect(host='127.0.0.1',user='bian',passwd='123456',db='car_market',charset='utf8')
        self.host=sqlconfig.get('host')
        self.user=sqlconfig.get('user')
        self.passwd=sqlconfig.get('passwd')
        self.db=sqlconfig.get('db')
        self.charset=sqlconfig.get('utf8')
        self.conn=pymysql.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,charset='utf8')

        # self.conn=pymysql.connect(host=sqlconfig.get('host'),user=sqlconfig.get('user'),
        #                           passwd=sqlconfig.get('passwd'),db=sqlconfig.get('db'),charset=sqlconfig.get('utf8'))
        self.cur=self.conn.cursor()

    def drop_table(self):

        self.cur.execute('DROP TABLE IF EXISTS jd')
        self.conn.commit()
        print u'删除表成功'

    def inert(self):
        inserttime=str(datetime.datetime.now()).split('.')[0]
        sql_log='insert into t_fang_mx_log VALUES ("%s","%s","%s","%s","%s")'%(oid,web,price,hangqing,inserttime)
        self.cur.execute(sql_log)
        self.conn.commit()

    def findalldata(self,oid):
        # sql='select buytime,order_number,promotion_way,number,buyer,address,phone_number,total_amount,trade_name from jd'
        sql='select buytime,number,buyer,address,total_amount,phone_number from jd WHERE oid="%s"'%oid
        self.cur.execute(sql)
        da=self.cur.fetchall()
        data=[]
        for i in da:
            data.append(i)
        return data
    def find_user_data(self,email):
        # sql='select buytime,order_number,promotion_way,number,buyer,address,phone_number,total_amount,trade_name from jd'
        sql='select * from users WHERE email="%s"'%email
        self.cur.execute(sql)
        da=self.cur.fetchall()
        data=[]
        for i in da:
            data.append(i)
        return data


    def insert_many(self,datalist):
        # data=(callphone[0],holse[0],start_time[0],end_time[0],call_type,nativefee[0],otherfee[0],internet_traffic[0].strip('K'),calldate,oid)
        # datalist.append(data)

        sql='insert into xiciips (ip,port,adress,anonymous,types,speed,Connection_time,Survival_time,validation_time,timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        # print u'将插入',len(datalist),type(tuple(datalist)),u'条数据'
        try:
            self.cur.executemany(sql,datalist)  #datalist可以是list 也可以是tuple类型 datalist中的元素类别为:tuple(元组)
            self.conn.commit()
        except Exception,e:
            print u'数据库插入失败：',Exception,e
    def insert_many_free(self,sql,datalist):
        try:
            self.cur.executemany(sql,datalist)  #datalist可以是list 也可以是tuple类型 datalist中的元素类别为:tuple(元组)
            self.conn.commit()
            print 'insert into news_select_middle successed'
        except Exception,e:
            print u'数据库插入失败：',Exception,e
    def updata(self,name):
        sql='update status SET status=0 WHERE NAME = "%s"'%name
        self.cur.execute(sql)
        self.conn.commit()

    def find_all(self,sql):
        # sql='select * from users WHERE email="%s"'%email
        self.cur.execute(sql)
        da=self.cur.fetchall()
        data=[]
        for i in da:
            data.append(i)
        return data
    def find_return_cur(self,sql):
        self.cur.execute(sql)
        return self.cur

    def hand_free(self):
        return self.cur,self.conn

# connlocal=pymysql.connect(host='127.0.0.1',user='bian',passwd='123456',db='car_market',charset='utf8')
# curlocal=connlocal.cursor()
# conn=pymysql.connect(host='127.0.0.1',user='bian',passwd='123456',db='car_market',charset='utf8')
# cur=conn.cursor()

class handle_mysql_backup():

    pass
    def drop_table(self):

        cur.execute('DROP TABLE IF EXISTS jd')
        conn.commit()
        print u'删除表成功'

    def inert(self):
        inserttime=str(datetime.datetime.now()).split('.')[0]
        sql_log='insert into t_fang_mx_log VALUES ("%s","%s","%s","%s","%s")'%(oid,web,price,hangqing,inserttime)
        cur.execute(sql_log)
        conn.commit()

    def findalldata(self,oid):
        # sql='select buytime,order_number,promotion_way,number,buyer,address,phone_number,total_amount,trade_name from jd'
        sql='select buytime,number,buyer,address,total_amount,phone_number from jd WHERE oid="%s"'%oid
        cur.execute(sql)
        da=cur.fetchall()
        data=[]
        for i in da:
            data.append(i)
        return data
    def find_user_data(self,email):
        # sql='select buytime,order_number,promotion_way,number,buyer,address,phone_number,total_amount,trade_name from jd'
        sql='select * from users WHERE email="%s"'%email
        cur.execute(sql)
        da=cur.fetchall()
        data=[]
        for i in da:
            data.append(i)
        return data

    def insert_many(self,datalist):
        # data=(callphone[0],holse[0],start_time[0],end_time[0],call_type,nativefee[0],otherfee[0],internet_traffic[0].strip('K'),calldate,oid)
        # datalist.append(data)

        sql='insert into xiciips (ip,port,adress,anonymous,types,speed,Connection_time,Survival_time,validation_time,timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        # print u'将插入',len(datalist),type(tuple(datalist)),u'条数据'
        try:
            cur.executemany(sql,datalist)  #datalist可以是list 也可以是tuple类型 datalist中的元素类别为:tuple(元组)
            conn.commit()
        except Exception,e:
            print u'数据库插入失败：',Exception,e
    def updata(self,name):
        sql='update status SET status=0 WHERE NAME = "%s"'%name
        cur.execute(sql)
        conn.commit()

    def find_all(self,sql):
        # sql='select * from users WHERE email="%s"'%email
        cur.execute(sql)
        da=cur.fetchall()
        data=[]
        for i in da:
            data.append(i)
        return data
    def find_return_cur(self,sql):
        cur.execute(sql)
        return cur

# import MySQLdb

# class rhzxdb():
#     def __init__(self):
#
#         self.connlocal= MySQLdb.connect(
#                     # host='192.168.1.144',
#                     host='localhost',
#                     port = 3306,
#                     # user='root',
#                     user='bian',
#                     passwd='123456',
#                     # db ='rh_qxt',
#                     db ='reposts',
#                     charset="UTF8"
#                     )
#         self.curlocal=self.connlocal.cursor()
#
#
#
#     def Insert(self,sql):
#         self.curlocal.execute(sql)
#         self.connlocal.commit()
#         print 'insert Success'
#     def findall(self,sql):
#         # sql='select * from users WHERE email="%s"'%email
#         self.curlocal.execute(sql)
#         da=self.curlocal.fetchall()
#         data=[]
#         for i in da:
#             data.append(i)
#         return data
#
#
#     def htmlpath(self,name):
#         sql="insert into rhzx (id,type,value,num) VALUES ('%s','%s','%s','%s')"%(self.lsh,'report',name,self.num)
#         self.Insert(sql)
#
#     def Close(self):
#         # driver.close()
#         self.curlocal.close()
#         self.connlocal.close()
#
# # if __name__=="__main__":
# #     driver=webdriver.PhantomJS()
# #     html=driver.get('http://localhost:63342/JavaScripy_Lenning/Ronhe/ren_hang_zheng_xin/grb_baogao.html')
# #     html=driver.page_source
# #     parsing=parsing(html)
# #     parsing.jibenxinxi()
# #     parsing.xinxigaiyao()
# #     parsing.xinxigaiyao2()
# #     parsing.jilu()
#
#
#     # infos=shu.xpath('//*[@class="p"]/text()')
#     # for i in infos:
#     #     print infos.index(i),i.replace(' ','').replace('\t','').replace('\r','').replace('\n','_').strip('\n')
#         # info=info.split(u'：')
#         #
#         # if len(info)==2:
#         #     print info[0],info[1]
#         #     datatype=info[0].strip()
#         #     value=info[1].strip()
#         #     sql="insert into rhzx (id,type,value,num) VALUES ('%s','%s','%s','%s')"%(lsh,datatype,value,num)
#         #     print sql
#         #     # curlocal.execute(sql)
#         #     # connlocal.commit()
#         #     print 'insert Success'