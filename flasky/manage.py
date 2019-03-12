#!/usr/bin/env python
#coding=utf-8
import os

# import os
from app import create_app, db
from app.models import User, Role, Post    #这里需要导入模块
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand #使用 Flask-Migrate 实现数据库迁移


# from flask.ext.restful import reqpaese

app = create_app(os.getenv('FLASK_CONFIG') or 'mysqldb')  #default
manager = Manager(app)
migrate = Migrate(app, db)

#为Python shell定义的上下文
#make_shell_context() 函
# 数注册了程序、数据库实例以及模型,因此这些对象能直接导入 shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role ,Post=Post)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


#以下是测试使用
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade
    from app.models import Role, User

    # 把数据库迁移到最新修订版本
    upgrade()

    # 创建用户角色
    Role.insert_roles()

    # 让所有用户都关注此用户
    User.add_self_follows()

# if __name__ == '__main__':
#     manager.run()
if __name__=="__main__":

    # from .app.configfile import sqllitfilepath
    # print sqllitfilepath
    app.run(host='0.0.0.0',debug=True)


# 用户认证
# 836426094@qq.com  bian314159 bian@314159