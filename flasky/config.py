#/usr/bin/env python
#coding=utf-8


import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
class Mysql_db(Config):
    DEBUG = True
    MAIL_SERVER = 'c2.icoremail.net'                  #邮件的服务器
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    from_addr = 'qjt@ronhe.com.cn'
    password = '18510179486'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or from_addr
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or password
    SQLALCHEMY_DATABASE_URI = 'mysql://bian:123456@127.0.0.1:3306/car_market'
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/news'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True #SQLALCHEMY_COMMIT_ON_TEARDOWN可以设置为True，来启用自动提交数据库更改在每个请求中
    SQLALCHEMY_TRACK_MODIFICATIONS = True  #UserWarning:SQLALCHEMY_TRACK_MODIFICATIONS增加大量开销,在未来将被禁用默认情况下。设置为True压制这个警告。警告。警告(SQLALCHEMY_TRACK_MODIFICATIONS补充说重要的开销和在未来将被禁用默认情况下。设置为True压制这个警告。”) *重启与统计    TESTING = True

    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_POSTS_PER_PAGE = 5  #用来指定每页显示的数量
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    FLASKY_SLOW_DB_QUERY_TIME=0.5
    FLASKY_DAILIIP_PER_PAGE=10
    # app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    #配置数据库信息  下面代码初始化及配置了一个简单的sqllite数据库

    # from flask.ext.sqlalchemy import SQLAlchemy
    # import os
    # # basedir=os.path.abspath(os.path.dirname(__file__))
    # # print basedir
    # #'sqlite:///c:absolute/path/to/database'  #windows
    # # app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
    # app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://bian:123456@127.0.0.1:3306/car_market'
    # app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    # db = SQLAlchemy(app)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'mysqldb' : Mysql_db,

    'default': DevelopmentConfig
}
