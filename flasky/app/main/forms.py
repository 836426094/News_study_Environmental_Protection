#coding=utf-8


#flask-Moment 本地化时间和日期
# from flask.ext.moment import Moment
# moment=Moment(app)

#定义表单类  重定向和用户会话session
# from flask.ext.wtf import Form
# from flask_wtf import Form
from flask_wtf import FlaskForm as Form
from flask import session,redirect,url_for,flash #用户会话和重定向 flash 提示消息
from ..models import User,Role
from wtforms import StringField, SubmitField,FileField,TextAreaField,PasswordField,BooleanField,SelectField
from wtforms.validators import Required,IPAddress,Email,URL,Length,Regexp,ValidationError,DataRequired
# from flask.ext.pagedown.fields import PageDownField  #启用Markdown的文章表单
from flask_pagedown.fields import PageDownField  #启用Markdown的文章表单



class NameForm(Form):
    #此处定义的form表单不能出现一个中文字符 否则宝编码错误
    name = StringField('What is your name?', validators=[Required()])
    passwd=PasswordField('Password:')
    # textcont = TextAreaField('hehe')
    Em=StringField('Email',validators=[Email()])
    # IP=StringField('IPAdress',validators=[IPAddress()])
    # url=StringField('URL',validators=[URL()])
    # file=FileField(u'文件上传:')
    submit = SubmitField('Submit')

#普通用户资料编辑表单
class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField(u'保存')

#管理员级别的资料编辑器
class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)#<select>进行SelectField包装
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


#博客文章表单
class PostForm(Form):

    # body = TextAreaField("What's on your mind?", validators=[Required()])
    #若想把首页中的多行文本控件转换成Markdown富文本编辑器，PostForm表单中的body字段要进行修改 启用Markdown的文章表单
    body = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')
    # body=TextAreaField(u'说说你的感想',validators=[DataRequired(u'内容不能为空！')])
    # submit = SubmitField(u'提交')

#评论输入表单
class CommentForm(Form):
    body = StringField(u'', validators=[Required()])
    submit = SubmitField('Submit')