# #coding=utf-8
#
# from flask import Flask, render_template
# from flask.ext.bootstrap import Bootstrap
# from flask.ext.mail import Mail
# from flask.ext.moment import Moment  #Flask-Moment是一个集成moment.js到Jinja2模板的Flask扩展。
# from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext.login import login_required  #登入验证  路由保护
#
# try:
#     from config import config
#     # from ..config import config
# except ImportError:
#     from Ronhe.flasky.config import config
#
# from flask.ext.login import LoginManager
#
#
# login_manager = LoginManager()#登陆管理#声明login对象
# from flask.ext.pagedown import PageDown  #使用Markdown和Flask-PageDown支持富文本文章
#
# login_manager.session_protection = 'strong'  #LoginManager对象的session_protection属性可以设为None、'basic'或'strong'，以提供不同的安全等级防止用户会话遭篡改
# login_manager.login_view = 'auth.login'   #设为'strong'时，Flask-Login会记录客户端IP地址和浏览器的用户代理信息，如果发现异动就登出用户。login_view属性设置登录页面的端点。回忆一下，登录路由在蓝本中定义，因此要在前面加上蓝本的名字。
#
# bootstrap = Bootstrap()
# mail = Mail()
# moment = Moment()
# db = SQLAlchemy()
# pagedown = PageDown()
#
# def create_app(config_name):
#     app = Flask(__name__)
#
#     app.config.from_object(config[config_name])  #其中保存的配置可以使用Flask app.config配置对象提供的from_object()方法直接导入程序
#     config[config_name].init_app(app)   #在创建的扩展对象上调用init_app()可以完成初始化过程
#
#     bootstrap.init_app(app)
#     mail.init_app(app)
#     moment.init_app(app)  ##相当于使用Bootstrap  from flask.ext.bootstrap import Bootstrap 。。。 bootstrap=Bootstrap(app)
#     db.init_app(app)
#     login_manager.init_app(app)#初始化绑定到应用
#     pagedown.init_app(app)
#
#     # 附加路由和自定义的错误页面
#     from .main import main as main_blueprint
#     app.register_blueprint(main_blueprint)  #将main蓝本注册到app上
#
#
#
#
#
#     return app
#
#
