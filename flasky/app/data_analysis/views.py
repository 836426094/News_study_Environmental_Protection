#coding=utf-8


from flask import render_template, redirect, request, url_for, flash,jsonify
from flask_login import login_user,logout_user,login_required
from ..models import User,handle_mysql
from . import data_analysis
# from .forms import LoginForm, RegistrationForm
from datetime import datetime
# from flasky.app import db

handle_mysql=handle_mysql()

import random
data = [random.randint(0,100) for i in range(5)]

@data_analysis.route('/DataAnalysis')
@login_required
def DataAnalysis():

    return render_template('data_analysis/data_index.html',current_time=datetime.utcnow(),
                           ldata=[random.randint(0,100) for i in range(5)],
                           sdata=[random.randint(0,100) for i in range(5)],
                           xdata=[random.randint(0,100) for i in range(5)],
                           xiaoliang=[random.randint(0,100) for i in range(6)]
                           )




@data_analysis.route('/daili')
# @login_required
def daili():
    if request.method=="POST":
        return 'ok'
    return render_template('data_analysis/daili.html')


data=[600, 200, 360, 100, 150, 200]
@data_analysis.route('/j')
# @login_required
def json_data():
    # return 1
    return jsonify(data)
    # return render_template('data_analysis/daili.html')


#重设密码
@data_analysis.route('/posthtml', methods=['GET', 'POST'])
def posthtml():

    # if form.validate_on_submit():
    if request.method=='POST':
        form=request.form
        # user = User.query.filter_by(email=form.email.data).first()
        # if user:
        print form
            # token = user.generate_reset_token()
            # text=render_template('auth/email/reset_password.txt',user=user,token=token)
            # yibu_send_email(title=u'reset',text=text,to_userlist=[form.email.data])
            # next=request.args.get('next')
            # print next

            # send_email(user.email, 'Reset Your Password',
            #            'auth/email/reset_password',
            #            user=user, token=token,
            #            next=request.args.get('next'))
        # flash('An email with instructions to reset your password has been '
        #       'sent to you.')
        # return redirect(url_for('auth.login'))
        return 'Successful!'
    return u'链接...'



# @data_analysis.route('/')
# def index():
#     return render_template('index.html')




