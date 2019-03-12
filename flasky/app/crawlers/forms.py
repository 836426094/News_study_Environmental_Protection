#coding=utf-8


# import sys
# sys.setrecursionlimit(100000)
from flask_wtf import Form
# from flask_wtf import Form

from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length,Email

from wtforms.validators import Regexp, EqualTo
from wtforms import ValidationError



# class LoginForm(Form):
#     email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
#     password = PasswordField('Password', validators=[Required()])
#     remember_me = BooleanField('Keep me logged in')
#     submit = SubmitField('Log In')



#人行征信基础数据提交
class rhzx_baseinfo(Form):
    account = StringField('Account', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    chaxunma = StringField('cxm', validators=[Required()])
    Img_yzm = StringField('yzm', validators=[Required()])
    # remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Submit')

    # email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    # password = PasswordField('Password', validators=[Required()])
    # remember_me = BooleanField('Keep me logged in')
    # submit = SubmitField('Log In')