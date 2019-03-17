#coding=utf-8

from __future__ import division
# import sys
# sys.setrecursionlimit(100000)  #是递归的遍历深度加深到10W
from flask import render_template, redirect, request, url_for, current_app
from flask_login import login_required

# from ..auth.views import g_user_datanum
from . import crawlers
from ..models import handle_mysql
# from  handle_sqllite as  handle_mysql
# from ..sqllite_models import handle_sqlite
# from ...mymodels import
# from .forms import LoginForm, RegistrationForm
from datetime import datetime
# from flasky.app import db
# from ..models import Dailiips,Status#,news_data_d,news_result_d
# from ..decorators import admin_required, permission_required

import re
# from ..models import rhzxdb





handle_mysql=handle_mysql()

# from ..sqllite_models import handle_sqlite
# handle_sqllite=handle_sqlite()
# print handle_sqllite.sqllitfile

# from .daili.xici_ip.spiters.getdata import mainspiter

from threading import Thread


# from flasky.app.crawlers.forms import rhzx_baseinfo
import codecs
import time
# import chardet
import socket
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
def GetDesktopPath():
    #C:\Users\Machenike\Desktop  取得的值
    return os.path.join(os.path.expanduser("~"), 'Desktop')
# print GetDesktopPath()
driveritem={}

#    15981855109
#        ZHANGYANHUI66
##查询码   x44769

userconfig_usercount=3

def set_g_userdatanum(g_user_datanum):
    cur,conn=handle_mysql.hand_free()
    getcount='select COUNT(*) from news_data;'
    cur.execute(getcount)
    s=cur.fetchone()
    total_row=s[0]

    if g_user_datanum['user']==1:
        g_user_datanum['startnum']=0
        g_user_datanum['limitnum']=int(total_row*1/userconfig_usercount)
        g_user_datanum['getcount_sql']='select COUNT(*) from news_data LIMIT %d, %d;'%(g_user_datanum['startnum'],g_user_datanum['limitnum'])
    elif g_user_datanum['user']==2:
        g_user_datanum['startnum']=int(total_row*1/userconfig_usercount)
        g_user_datanum['limitnum']=int(total_row*2/userconfig_usercount)
        g_user_datanum['getcount_sql']='select COUNT(*) from news_data LIMIT %d, %d;'%(g_user_datanum['startnum'],g_user_datanum['limitnum'])
    elif g_user_datanum['user']==3:
        g_user_datanum['startnum']=total_row*2/userconfig_usercount
        g_user_datanum['limitnum']=total_row*3/userconfig_usercount
        g_user_datanum['getcount_sql']='select COUNT(*) from news_data LIMIT %d, %d;'%(g_user_datanum['startnum'],g_user_datanum['limitnum'])
    elif g_user_datanum['user']==4:
        g_user_datanum['startnum']=total_row*3/userconfig_usercount
        g_user_datanum['limitnum']=total_row*4/userconfig_usercount
        g_user_datanum['getcount_sql']='select COUNT(*) from news_data LIMIT %d, %d;'%(g_user_datanum['startnum'],g_user_datanum['limitnum'])



    elif g_user_datanum['user']==10:
        g_user_datanum['startnum']=0
        g_user_datanum['limitnum']=total_row
        g_user_datanum['getcount_sql']='select COUNT(*) from news_data;'
    else:
        g_user_datanum['startnum']=0
        g_user_datanum['limitnum']=total_row
        # g_user_datanum['getcount_sql']='select COUNT(*) from news_data;'
    # except:
        g_user_datanum['getcount_sql']='login'

        # pass
        # g_user_datanum['getcount_sql']='select COUNT(*) from news_data;'
    return g_user_datanum

@crawlers.route('/news',methods=['GET', 'POST'])
@login_required
# @permission_required(Permission.FOLLOW)
def news():
    print request.data
    # print login_manager.LoginManager._load_user()
    # print login_required.func_globals
    status='news'
    userdata=request.cookies.get('user')
    g_user_datanum={}
    g_user_datanum['user']=int(userdata)
    g_user_datanum=set_g_userdatanum(g_user_datanum)
    print 'groble g_user_datanum:',g_user_datanum
    #加上用户的起始查询数值
    userstartnum=g_user_datanum['startnum']

    # status=Status.check_status(status)
    # print status
    page = request.args.get('page', 1, type=int)#渲染的页数从请求的查询字符串（ request.args）中获取，如果没有明确指定，则默认渲
    # 染第一页。参数 type=int 保证参数无法转换成整数时，返回默认值。
    #paginate() 方法的返回值是一个 Pagination 类对象，这个类在 Flask-SQLAlchemy 中定义。
    # 这个对象包含很多属性， 用于在模板中生成分页链接，因此将其作为参数传入了模板。

    print page
    # pagination = news_data.query.order_by(news_data.ID.desc()).paginate(
    #     page, per_page=current_app.config['FLASKY_DAILIIP_PER_PAGE'],
    #     error_out=False)
    #判断传回的页数对不对
    page,per_page=paginate_zdy(page,10)
    limitpage=10


    if page==0:
        page=1+userstartnum
    if page==1:
        startpage=0+userstartnum

    elif page>=2:
        startpage=(page-1)*limitpage+userstartnum
    print startpage,limitpage
    # sql='select a.ID,a.url,a.title,a.datatate,b.content2 from news_data a INNER JOIN news_result b on a.ID=b.ID ORDER BY a.ID LIMIT %d, %d'%(startpage,limitpage)
    # sql='select a.ID,a.url,a.title,a.datatate,a.content from news_data a ORDER BY a.ID LIMIT %d, %d'%(startpage,limitpage)
    sql='select a.ID,a.url,a.title,a.datatate,a.content from news_data a ORDER BY a.ID LIMIT %d, %d'%(startpage,limitpage)
    print sql
    cur=handle_mysql.find_return_cur(sql)
    curs=cur.fetchall()
    posts=[]
    for i in curs:
        ilist=list(i)
        html=ilist[4]
        # print u'查询出来的数：',ilist[0],ilist[1],ilist[2],ilist[3]
        contend=get_rid_of_html(html,xpahttype=1)
        dr = re.compile(r'\n',re.S)
        # dd = dr.sub('<br/>',contend)
        dd = dr.sub(' ',contend)
        ilist[4]=dd

        # ilist[4]=contend
        # print ilist
        # dd=dd.decode('gbk', 'ignore').encode('utf-8')
        # print dd
        posts.append(ilist)

    posts=Character_insert_and_select(posts)

    # print u'pagination:',pagination
    # posts = pagination.ID #当前页中的记录
    # print posts

    # 分页
    pagelist=[]
    if page<=5:
        uppage='/crawlers/news?page=1'
        nextpage='/crawlers/news?page=11'

        for i in range(1,10):
            t=[]
            alt='/crawlers/news?page='+str(i)
            t.append(i)
            t.append(alt)
            pagelist.append(t)

    else:
        uppage='/crawlers/news?page='+str(page-5)
        nextpage='/crawlers/news?page='+str(page+6)
        for i in range(page-4,page+5):
            t=[]
            alt='/crawlers/news?page='+str(i)
            t.append(i)
            t.append(alt)
            pagelist.append(t)

    # getcount='select COUNT(*) from news_data a inner JOIN news_result b on a.ID=b.ID;'
    # getcount='select COUNT(*) from news_data;'
    # try:
    getcount=g_user_datanum['getcount_sql']
    print u'now getcount is ',getcount
    if getcount=='login':
        print 'get count is login '
        return redirect(url_for('auth.logout'))
    else:
        pass

    # cur.execute(getcount)
    # s=cur.fetchone()
    # total_row=s[0]
    # total_row=g_user_datanum['limitnum']
    lnum=g_user_datanum['limitnum']
    startnum=g_user_datanum['startnum']
    total_row=lnum-startnum
    pagecount=total_row/limitpage
    print u'now get pagecount is limitnum',pagecount,',startnum is %d,limitnum is %d;'%(startnum,lnum),
    if pagecount>int(pagecount):
        pagecount=int(pagecount+1)
    else:
        pagecount=int(pagecount)
    print 'pagecount is ',pagecount
    # except:
    #     print 'get count Error '

        # return render_template('auth/login.html')
        #
        # return render_template('auth/unconfirmed.html')
        # return redirect(url_for('auth.login'))
        # return redirect(url_for('auth.logout'))




    #给新闻打分部分
    print request.method
    prompt_info='false'

    title=''
    contend=''
    if request.method=='POST':
        print ' --post--data'
        formdata=request.form

        if formdata:
            formdata=dict(formdata)
            # print formdata
            print formdata
            # UPDATE table_name SET field1=new-value1, field2=new-value2 [WHERE Clause]
            updatesql='update news_result set '
            ID=0
            for k in formdata:
                if k=='ID':
                    ID=formdata[k][0]
                    continue
                elif k=='title':
                    title=formdata[k][0]
                    continue

                print k,':',formdata[k][0]
                setstring=k+'='+str(formdata[k][0])+','
                updatesql=updatesql+setstring
            # title=formdata.get('title')[0]
            # contend=formdata.get('title')[0]

            print ID
            if ID!=0:
                delsql='delete from news_result WHERE ID=%s'%ID
                #DELETE FROM `news_result` WHERE (`ID`='967433')

                sql='insert into  news_result (ID,url,title,datatate,content) SELECT ID,url,title,datatate,content from news_select_middle WHERE ID=%s'%ID
                cur,conn=handle_mysql.hand_free()
                cur.execute(delsql)
                cur.execute(sql)
                conn.commit()

                updatesql=updatesql.strip(',')
                print updatesql
                updatesql=updatesql+' where ID='+str(ID)
                print updatesql
                try:
                    cur,conn=handle_mysql.hand_free()
                    cur.execute(updatesql)
                    conn.commit()
                    print str(ID)+' update success'
                    prompt_info=u'ID为：'+ID+u'的新闻提交成功'
                except:
                    prompt_info=u'请选择新闻以及新闻属性在提交！'
            else:
                prompt_info=u'请选中一则新闻!'
        else:
            prompt_info=u'请选择新闻和分类'
        print prompt_info
    return render_template('news/news.html', posts=posts,prompt_info=prompt_info,
                           current_time=datetime.utcnow(),page=page,pagelist=pagelist,
                           status=status,uppage=uppage,nextpage=nextpage,rowcount=pagecount,
                           title=title,contend=contend)


@crawlers.route('/news_export',methods=['GET', 'POST'])
@login_required
def news_export():
    status='news_export'
    # status=Status.check_status(status)
    # print status
    page = request.args.get('page', 1, type=int)#渲染的页数从请求的查询字符串（ request.args）中获取，如果没有明确指定，则默认渲
    # 染第一页。参数 type=int 保证参数无法转换成整数时，返回默认值。
    #paginate() 方法的返回值是一个 Pagination 类对象，这个类在 Flask-SQLAlchemy 中定义。
    # 这个对象包含很多属性， 用于在模板中生成分页链接，因此将其作为参数传入了模板。
    # print 'groble g_user_datanum:',g_user_datanum
    print page
    limitpage=15
    if page==0:
        page=1
    if page==1:
        startpage=0

    elif page>=2:
        startpage=(page-1)*limitpage
    print startpage,limitpage
    #给新闻打分部分
    print request.method

    formdata_return={}
    filedir_name=''
    update_status='0'  #更新提示符
    updatesql0=''
    if request.method=='POST':
        print ' --post--data---',datetime.now()
        startpage=0
        page=1
        formdata=request.form
        if formdata:
            formdata=dict(formdata)

            # print formdata
            print formdata
            # UPDATE table_name SET field1=new-value1, field2=new-value2 [WHERE Clause]


            ID=0

            for k in formdata:
                formdata_return[k]=formdata[k][0]
                if k=='ID' or k=='export' or k=='update':
                    print u'观察id export update:',k,':',formdata[k]

                    continue
                print k,':',formdata[k][0]
                #UPDATE tbl_name SET col_name1=value1, col_name2=value2, … WHERE id=...


                setstring=' a.'+k+'='+str(formdata[k][0])+'  and'
                filedir_name=filedir_name+"_"+k
                updatesql0=updatesql0+setstring
            updatesql=' where '+updatesql0.strip('and')

            print "Handle web form's data to select sql:",updatesql


            print 'Return to web - "form_return" is:',formdata_return

            if formdata_return.get('update')=='1':
                ID=formdata_return.get('ID')
                real_updatesql='update news_result set '+updatesql0.strip('and')
                real_updatesql=real_updatesql.strip('and')+' where ID='+str(ID)
                real_updatesql=real_updatesql.replace('a.','').replace(' and ',',')
                print "Handle web form's data to update sql:",real_updatesql
                print 'Will be update news data,the sql is:',real_updatesql
                cur,conn=handle_mysql.hand_free()

                cur.execute(real_updatesql)
                conn.commit()
                update_status=u'id为%s的新闻属性修改成功!'%str(ID)
                print update_status
            # cur,conn=handle_mysql.hand_free()
            # cur.execute(updatesql)
            # conn.commit()
            # print str(ID)+' update success'
            if formdata_return.get('export')=='all':

                print 'updatesql',[updatesql]
                if updatesql.strip()=='where': #如果什么条件都不选就点击导出全部的话
                    # sql='select a.ID,a.url,a.title,a.datatate,b.content2 from news_data a INNER JOIN news_result b on a.ID=b.ID  ORDER BY a.ID '
                    sql='select a.ID,a.url,a.title,a.datatate,a.content,a.hege,a.wuran,a.fengxian,a.shengtai,' \
                        'a.ziyuan,a.xuanjiao,a.guanli,a.shuihj_2,a.kongqi_2,a.shenghj_2,a.turang_2,a.feiwu_2,a.shengwu_2,a.other_2,a.score ' \
                        'from news_result a ORDER BY a.ID '
                    print '--4 if sql     --',sql
                else:
                    if updatesql.strip()=='where':
                        updatesql=''
                    sql='select a.ID,a.url,a.title,a.datatate,a.content,a.hege,a.wuran,a.fengxian,' \
                        'a.shengtai,a.ziyuan,a.xuanjiao,a.guanli,a.shuihj_2,a.kongqi_2,a.shenghj_2,' \
                        'a.turang_2,a.feiwu_2,a.shengwu_2,a.other_2,a.score ' \
                        'from news_result a '+updatesql+' ORDER BY a.ID'

                    print '--4 else sql     --',sql

                getcount='select COUNT(*) from news_result a '+updatesql

                getcount=getcount.strip('where ')
                print '--4 if getcount--',getcount
                print u'采集全部',
            else:
                # if updatesql.strip()=='where': #如果什么条件都不选就点击导出全部的话
                #     sql='select a.ID,a.url,a.title,a.datatate,b.content2 from news_data a INNER JOIN news_result b on a.ID=b.ID  ORDER BY ID DESC'
                # else:
                if updatesql.strip()=='where':
                    updatesql=''

                sql='select a.ID,a.url,a.title,a.datatate,a.content,a.hege,a.wuran,a.fengxian,a.shengtai,a.ziyuan,a.xuanjiao,a.guanli,a.shuihj_2,a.kongqi_2,a.shenghj_2,a.turang_2,a.feiwu_2,a.shengwu_2,a.other_2,a.score	 from news_result a '+updatesql+' ORDER BY a.ID LIMIT %d, %d'%(startpage,limitpage)

                getcount='select COUNT(*) from news_result a '+updatesql
                sql=sql.strip('where ')
                getcount=getcount.strip('where ')
                print '--3 else sql     --',sql
                print '--3 else getcount--',getcount
        else:
            sql='select a.ID,a.url,a.title,a.datatate,a.content,a.hege,a.wuran,a.fengxian,a.shengtai,a.ziyuan,a.xuanjiao,a.guanli,a.shuihj_2,a.kongqi_2,a.shenghj_2,a.turang_2,a.feiwu_2,a.shengwu_2,a.other_2,a.score	 from news_result a ORDER BY a.ID LIMIT %d, %d'%(startpage,limitpage)
            getcount='select COUNT(*) from news_result a'
            print '--2 else sql     --',sql
            print '--2 else getcount--',getcount
    else:
        sql='select a.ID,a.url,a.title,a.datatate,a.content,a.hege,a.wuran,a.fengxian,a.shengtai,a.ziyuan,a.xuanjiao,a.guanli,a.shuihj_2,a.kongqi_2,a.shenghj_2,a.turang_2,a.feiwu_2,a.shengwu_2,a.other_2,a.score	 from news_result a ORDER BY a.ID LIMIT %d, %d'%(startpage,limitpage)
        getcount='select COUNT(*) from news_result'

        print '--1 else sql     --',sql
        print '--1 else getcount--',getcount
    # sql='select a.ID,a.url,a.title,a.datatate,a.content from news_data a ORDER BY ID DESC LIMIT %d, %d'%(startpage,limitpage)

    dirname=''
    if formdata_return.get('export'):
        zhuomian=GetDesktopPath()
        timesting=str(datetime.now()).split()[0].replace('-','_')
        dirname=zhuomian+'\\'+timesting+'_'+filedir_name
        print dirname
        if os.path.exists(dirname):
            pass
        else:
            os.makedirs(dirname)
            print 'makedir successful!'


    formdata_return2={}
    cur=handle_mysql.find_return_cur(sql)
    curs=cur.fetchall()

    posts=[]
    for i in curs:
        ilist=list(i)
        html=ilist[4]
        formdata_return2[ilist[0]]={}
        iddict=formdata_return2[ilist[0]]
        iddict['title']=ilist[2]
        iddict['hege']=ilist[5]
        iddict['wuran']=ilist[6]
        iddict['fengxian']=ilist[7]
        iddict['shengtai']=ilist[8]
        iddict['ziyuan']=ilist[9]
        iddict['xuanjiao']=ilist[10]
        iddict['guanli']=ilist[11]
        iddict['shuihj_2']=ilist[12]
        iddict['kongqi_2']=ilist[13]
        iddict['shenghj_2']=ilist[14]
        iddict['turang_2']=ilist[15]
        iddict['feiwu_2']=ilist[16]
        iddict['shengwu_2']=ilist[17]
        iddict['other_2']=ilist[18]
        iddict['score']=ilist[19]

        if formdata_return.get('export'):
            title=ilist[2].strip()
            # print ilist
            try:
                title=title.replace('-','').replace('?','').replace('*','')\
                    .replace('<','').replace('>','').replace('"','').replace('|','').replace(': ','').replace('\\','').replace('\ / ','')
                ilist[2]=title
                # txtname=dirname+'\\'+title+'.txt'
                txtname=u'%s\\%s.txt'%(dirname,title)
                # print txtname,[txtname]
                # print 'html',[html[:100]]

                f = codecs.open(txtname,'w+','utf8','ignore')
                # f = open(filename,'w+')
                # remove = re.compile('\s')
                # for x in content_list :
                #     x = re.sub(remove,'',x)
                #     f.write(x)
                #     f.write('\n')

                f.write(html)
                f.close()
            except Exception,e:

                print '----------',TypeError,e
                continue

            update_status=u'新闻导出成功，导出文件路径为:%s'%(dirname)
            print update_status
        # dr = re.compile(r'\t',re.S)
        # html = dr.sub('<br/>',html)
        ilist[4]=html
        posts.append(ilist)


    # print 'form_return2',formdata_return2


    # print u'pagination:',pagination
    # posts = pagination.ID #当前页中的记录
    # print posts

    # 分页的部分开始
    # getcount='select COUNT(*) from news_data a inner JOIN news_result b on a.ID=b.ID'+updatesql
    # getcount='select COUNT(*) from news_data a inner JOIN news_result b on a.ID=b.ID;'
    print getcount
    cur.execute(getcount)
    s=cur.fetchone()
    total_row=s[0]
    pagecount=total_row/limitpage

    if pagecount>int(pagecount):
        pagecount=int(pagecount+1)
    else:
        pagecount=int(pagecount)

    print u'总数',total_row,u'页数：',pagecount
    pagelist=[]
    if pagecount<10 and page<5:
        uppage='/crawlers/news_export?page=1'
        nextpage='/crawlers/news_export?page='+str(pagecount)

        for i in range(1,pagecount):
            t=[]
            alt='/crawlers/news_export?page='+str(i)
            t.append(i)
            t.append(alt)
            pagelist.append(t)
    elif pagecount>10 and page<5:
        uppage='/crawlers/news_export?page=1'
        nextpage='/crawlers/news_export?page=11'

        for i in range(1,10):
            t=[]
            alt='/crawlers/news_export?page='+str(i)
            t.append(i)
            t.append(alt)
            pagelist.append(t)

    else:
        uppage='/crawlers/news_export?page='+str(page-5)
        nextpage='/crawlers/news_export?page='+str(page+6)
        for i in range(page-4,page+5):
            t=[]
            alt='/crawlers/news_export?page='+str(i)
            t.append(i)
            t.append(alt)
            pagelist.append(t)

    # 分页的部分结束

    return render_template('news/news_export.html', posts=posts,formdata_return=formdata_return,
                           current_time=datetime.utcnow(),page=page,pagelist=pagelist,formdata_return2=formdata_return2,
                           status=status,uppage=uppage,nextpage=nextpage,rowcount=pagecount,prompt_info=update_status)




# @login_required
def news_export_backup():
    status='news_export'
    # status=Status.check_status(status)
    # print status
    page = request.args.get('page', 1, type=int)#渲染的页数从请求的查询字符串（ request.args）中获取，如果没有明确指定，则默认渲
    # 染第一页。参数 type=int 保证参数无法转换成整数时，返回默认值。
    #paginate() 方法的返回值是一个 Pagination 类对象，这个类在 Flask-SQLAlchemy 中定义。
    # 这个对象包含很多属性， 用于在模板中生成分页链接，因此将其作为参数传入了模板。

    print page
    limitpage=15
    if page==0:
        page=1
    if page==1:
        startpage=0

    elif page>=2:
        startpage=(page-1)*limitpage
    print startpage,limitpage
    #给新闻打分部分
    print request.method
    updatesql=''
    formdata_return={}
    filedir_name=''
    if request.method=='POST':
        print ' --post--data'
        startpage=0
        page=1
        formdata=request.form
        if formdata:
            formdata=dict(formdata)

            # print formdata
            print formdata
            # UPDATE table_name SET field1=new-value1, field2=new-value2 [WHERE Clause]


            ID=0

            for k in formdata:
                formdata_return[k]=formdata[k][0]
                if k=='ID' or k=='export':
                    # ID=formdata[k][0]
                    continue
                print k,':',formdata[k][0]

                setstring=' b.'+k+'='+str(formdata[k][0])+'  and'
                filedir_name=filedir_name+"_"+k
                updatesql=updatesql+setstring
            updatesql=' where '+updatesql.strip('and')
            print updatesql
            updatesql=updatesql  #+' where ID='+str(ID)
            print updatesql
            print 'form_return',formdata_return
            # cur,conn=handle_mysql.hand_free()
            # cur.execute(updatesql)
            # conn.commit()
            # print str(ID)+' update success'
            if formdata_return.get('export')=='all':

                if updatesql.strip()=='where': #如果什么条件都不选就点击导出全部的话
                    sql='select a.ID,a.url,a.title,a.datatate,a.content2 from news_data a INNER JOIN news_result b on a.ID=b.ID  ORDER BY a.ID '
                else:
                    sql='select a.ID,a.url,a.title,a.datatate,b.content2 from news_data a INNER JOIN news_result b on a.ID=b.ID '+updatesql+' ORDER BY a.ID LIMIT %d, %d'%(startpage,limitpage)

                getcount='select COUNT(*) from news_data a inner JOIN news_result b on a.ID=b.ID'+updatesql

                getcount=getcount.strip('where ')
                print u'采集全部',
            else:
                # if updatesql.strip()=='where': #如果什么条件都不选就点击导出全部的话
                #     sql='select a.ID,a.url,a.title,a.datatate,b.content2 from news_data a INNER JOIN news_result b on a.ID=b.ID  ORDER BY ID DESC'
                # else:
                sql='select a.ID,a.url,a.title,a.datatate,b.content2 from news_data a INNER JOIN news_result b on a.ID=b.ID '+updatesql+' ORDER BY a.ID LIMIT %d, %d'%(startpage,limitpage)

                getcount='select COUNT(*) from news_data a inner JOIN news_result b on a.ID=b.ID'+updatesql
                sql=sql.strip('where')
                getcount=getcount.strip('where')
        else:
            sql='select a.ID,a.url,a.title,a.datatate,b.content2 from news_data a INNER JOIN news_result b on a.ID=b.ID ORDER BY a.ID LIMIT %d, %d'%(startpage,limitpage)
            getcount='select COUNT(*) from news_data a inner JOIN news_result b on a.ID=b.ID'
    else:
        sql='select a.ID,a.url,a.title,a.datatate,b.content2 from news_data a INNER JOIN news_result b on a.ID=b.ID ORDER BY a.ID LIMIT %d, %d'%(startpage,limitpage)
        getcount='select COUNT(*) from news_data a inner JOIN news_result b on a.ID=b.ID'
    # sql='select a.ID,a.url,a.title,a.datatate,a.content from news_data a ORDER BY ID DESC LIMIT %d, %d'%(startpage,limitpage)

    dirname=''
    if formdata_return.get('export'):
        zhuomian=GetDesktopPath()
        timesting=str(datetime.now()).split()[0].replace('-','_')
        dirname=zhuomian+'\\'+timesting+'_'+filedir_name
        print dirname
        if os.path.exists(dirname):
            pass
        else:
            os.makedirs(dirname)
            print 'makedir successful!'

    print sql
    cur=handle_mysql.find_return_cur(sql)
    curs=cur.fetchall()
    posts=[]
    for i in curs:
        ilist=list(i)
        html=ilist[4]
        if formdata_return.get('export'):
            title=ilist[2].strip()
            txtname=dirname+'\\'+title+'.txt'
            f = codecs.open(txtname,'w+','utf8','ignore')
            # f = open(filename,'w+')
            # remove = re.compile('\s')
            # for x in content_list :
            #     x = re.sub(remove,'',x)
            #     f.write(x)
            #     f.write('\n')

            f.write(html)
            f.close()

        dr = re.compile(r'\t',re.S)
        dd = dr.sub('<br/>',html)
        ilist[4]=dd
        posts.append(ilist)





    # print u'pagination:',pagination
    # posts = pagination.ID #当前页中的记录
    # print posts

    # 分页的部分开始
    # getcount='select COUNT(*) from news_data a inner JOIN news_result b on a.ID=b.ID'+updatesql
    # getcount='select COUNT(*) from news_data a inner JOIN news_result b on a.ID=b.ID;'
    print getcount
    cur.execute(getcount)
    s=cur.fetchone()
    total_row=s[0]
    pagecount=total_row/limitpage

    if pagecount>int(pagecount):
        pagecount=int(pagecount+1)
    else:
        pagecount=int(pagecount)

    print u'总数',total_row,u'页数：',pagecount
    pagelist=[]
    if pagecount<10 and page<5:
        uppage='/crawlers/news_export?page=1'
        nextpage='/crawlers/news_export?page='+str(pagecount)

        for i in range(1,pagecount):
            t=[]
            alt='/crawlers/news_export?page='+str(i)
            t.append(i)
            t.append(alt)
            pagelist.append(t)
    elif pagecount>10 and page<5:
        uppage='/crawlers/news_export?page=1'
        nextpage='/crawlers/news_export?page=11'

        for i in range(1,10):
            t=[]
            alt='/crawlers/news_export?page='+str(i)
            t.append(i)
            t.append(alt)
            pagelist.append(t)

    else:
        uppage='/crawlers/news_export?page='+str(page-5)
        nextpage='/crawlers/news_export?page='+str(page+6)
        for i in range(page-4,page+5):
            t=[]
            alt='/crawlers/news_export?page='+str(i)
            t.append(i)
            t.append(alt)
            pagelist.append(t)

    # 分页的部分结束

    return render_template('news/news_export.html', posts=posts,formdata_return=formdata_return,
                           current_time=datetime.utcnow(),page=page,pagelist=pagelist,
                           status=status,uppage=uppage,nextpage=nextpage,rowcount=pagecount)



@crawlers.route('/run_xicispiter')
@login_required
def run_xicispiters():

    statusobj='xiciips'
    status=Status.change_status(statusobj)
    yibu_run_xici()
    page = request.args.get('page', 1, type=int)#渲染的页数从请求的查询字符串（ request.args）中获取，如果没有明确指定，则默认渲
    # 染第一页。参数 type=int 保证参数无法转换成整数时，返回默认值。
    #paginate() 方法的返回值是一个 Pagination 类对象，这个类在 Flask-SQLAlchemy 中定义。
    # 这个对象包含很多属性， 用于在模板中生成分页链接，因此将其作为参数传入了模板。
    # print page
    pagination = Dailiips.query.order_by(Dailiips.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_DAILIIP_PER_PAGE'],
        error_out=False)
    posts = pagination.items #当前页中的记录


    return render_template('crawlers/news.html', posts=posts,
                           current_time=datetime.utcnow(),pagination=pagination,status=status)



    # return render_template('crawlers/news.html',current_time=datetime.utcnow())


##人行征信
@crawlers.route('/rhzx_grb')
# @login_required
def rhzx_grb():
#     statusobj='xiciips'
#     status=Status.check_status(statusobj)
#     print status
#     page = request.args.get('page', 1, type=int)#渲染的页数从请求的查询字符串（ request.args）中获取，如果没有明确指定，则默认渲
# # 染第一页。参数 type=int 保证参数无法转换成整数时，返回默认值。
#     #paginate() 方法的返回值是一个 Pagination 类对象，这个类在 Flask-SQLAlchemy 中定义。
#     # 这个对象包含很多属性， 用于在模板中生成分页链接，因此将其作为参数传入了模板。
#     print page
#     pagination = Dailiips.query.order_by(Dailiips.timestamp.desc()).paginate(
#         page, per_page=current_app.config['FLASKY_DAILIIP_PER_PAGE'],
#         error_out=False)
#     posts = pagination.items #当前页中的记录
    return render_template('rhzx/get_data.html')

@crawlers.route('/rhzx_headerframe')
def rhzx_headerframe():
    return render_template('rhzx/mofang/headerFrame.html')


@crawlers.route('/rhzx_conframe')
def rhzx_conframe():
    return render_template('rhzx/mofang/conframe.html')


@crawlers.route('/rhzx_leftframe')
def rhzx_leftframe():
    return render_template('rhzx/mofang/leftFrame.html')


@crawlers.route('/rhzx_mainframe')
# @login_required
def rhzx_mainframe():
    return render_template('rhzx/mofang/mainFrame.html')



#人行征信基本信息
@crawlers.route('/rhzx_baseinfo', methods=['GET', 'POST'])
def rhzx_baseinfo():
    if request.method=="GET":
        ip_port=('127.0.0.1',9777)
        sk=socket.socket()  #实例化套接字
        sk.connect(ip_port)  #连接服务�?
        keywords="rhzx#836426094#836426094#15278112919qq#chaxunma"
        sk.sendall(keywords)   #向服务
        imgstring=sk.recv(1024*20)
        print  imgstring,type(imgstring)
        driverid=str(time.time())

        # driveritem[driverid]=sk
        # global driveritem

        return render_template('crawlers/ren_hang_zheng_xin/rhzx_baseinfo.html',imgstring=imgstring,driverid=driverid)

    elif request.method=='POST':
        form=request.form
        print form
        sk=driveritem[form.get('driverid')]

        user=form.get('account')
        passwd=form.get('passwd')
        chaxunma=form.get('chaxunma')
        img=form.get('img')

        sendsting=user+'#'+passwd+'#'+chaxunma+'#'+img
        print sendsting
        sk.send(sendsting)
        time.sleep(1)

        # retrundata=sk.recv(1024)
        # print retrundata
        # del driveritem[form.get('driverid')]
        # global driveritem

        return redirect(url_for('crawlers.rhzx_reportlist'))

        # return render_template('crawlers/ren_hang_zheng_xin/reportlist.html')

@crawlers.route('/rhzx_reportlist', methods=['GET', 'POST'])
def rhzx_reportlist():

    if request.method=="GET":
        rhDb=rhzxdb()
        sql='select * from rhzx WHERE type="report"'
        data=rhDb.findall(sql)
        rhDb.Close()
        # print data
        return render_template('crawlers/ren_hang_zheng_xin/reportlist.html',data=data)


@crawlers.route('/rhzx_report', methods=['GET', 'POST'])
def rhzx_report():

    if request.method=="GET":
        # sql='select * from rhzx WHERE type="report"'
        # data=rhzxDb.findall(sql)
        # print data
        name=request.args.get('report', '').strip()
        return render_template('crawlers/ren_hang_zheng_xin/baogao/%s'%name)


def yibu_run_xici():
    thr = Thread(target=mainspiter, args=[])
    thr.start()
    return thr



@crawlers.route('/xicispiters')
@login_required
def xicispiters():
    statusobj='xiciips'
    status=Status.check_status(statusobj)
    print status
    page = request.args.get('page', 1, type=int)#渲染的页数从请求的查询字符串（ request.args）中获取，如果没有明确指定，则默认渲
    # 染第一页。参数 type=int 保证参数无法转换成整数时，返回默认值。
    #paginate() 方法的返回值是一个 Pagination 类对象，这个类在 Flask-SQLAlchemy 中定义。
    # 这个对象包含很多属性， 用于在模板中生成分页链接，因此将其作为参数传入了模板。
    print page
    pagination = Dailiips.query.order_by(Dailiips.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_DAILIIP_PER_PAGE'],
        error_out=False)
    print u'pagination:',pagination
    posts = pagination.items #当前页中的记录
    print posts
    return render_template('crawlers/crawlers.html', posts=posts,
                           current_time=datetime.utcnow(),pagination=pagination,status=status)

# getcount='select COUNT(*) from news_data a inner JOIN news_result b on a.ID=b.ID;'
# # getcount='select COUNT(*) from news_data a inner JOIN news_result b on a.ID=b.ID;'
# cur,conn=handle_mysql.hand_free()
# cur.execute(getcount)
# s=cur.fetchone()
# total_row=s[0]

def Character_insert_and_select(posts):
    cur,conn=handle_mysql.hand_free()
    dsql='delete from news_select_middle'
    cur.execute(dsql)
    conn.commit()
    print 'delete all success!'

    # sql='insert into news_select_middle  (ip,port,adress,anonymous,types,speed,Connection_time,Survival_time,validation_time,timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    sql='insert into news_select_middle (ID,url,title,datatate,content) VALUES (%s,%s,%s,%s,%s)'
    handle_mysql.insert_many_free(sql,posts)


    sql='select ID,url,title,datatate,content from news_select_middle a ORDER BY ID '
    # print sql
    cur=handle_mysql.find_return_cur(sql)
    curs=cur.fetchall()
    posts2=[]
    for i in curs:
        ilist=list(i)
        # print u'len(ilist)',len(ilist)
        # newlist=[]
        #
        #
        # newlist[0]=ilist[0]
        # newlist[1]=ilist[1]
        # newlist[2]=ilist[2]
        # newlist[3]=ilist[3]
        # newlist[4]=ilist[4]
        # for i2 in ilist:
        #     newlist[ilist.index(i2)]=i2

        # html=ilist[4]
        # contend=get_rid_of_html(html)
        # dr = re.compile(r'\n',re.S)
        # dd = dr.sub('<br/>',contend)
        # ilist[4]=dd
        # ilist[4]=contend
        # print ilist
        # dd=dd.decode('gbk', 'ignore').encode('utf-8')
        # print dd
        posts2.append(ilist)


    return posts2

# @data_analysis.route('/daili')
# # @login_required
# def daili():
#
#     return render_template('data_analysis/daili.html')

def abort(num):
    return '<h2>%d</h3>'%num

def paginate_zdy(page=None, per_page=None, error_out=True):
        """Returns ``per_page`` items from page ``page``.

        If no items are found and ``page`` is greater than 1, or if page is
        less than 1, it aborts with 404.
        This behavior can be disabled by passing ``error_out=False``.

        If ``page`` or ``per_page`` are ``None``, they will be retrieved from
        the request query.
        If the values are not ints and ``error_out`` is ``True``, it aborts
        with 404.
        If there is no request or they aren't in the query, they default to 1
        and 20 respectively.

        Returns a :class:`Pagination` object.
        """

        if request:
            if page is None:
                try:
                    page = int(request.args.get('page', 1))
                except (TypeError, ValueError):
                    if error_out:
                        abort(404)

                    page = 1

            if per_page is None:
                try:
                    per_page = int(request.args.get('per_page', 20))
                except (TypeError, ValueError):
                    if error_out:
                        abort(404)

                    per_page = 20
        else:
            if page is None:
                page = 1

            if per_page is None:
                per_page = 20

        if error_out and page < 1:
            abort(404)

        # items = self.limit(per_page).offset((page - 1) * per_page).all()

        # if not items and page != 1 and error_out:
        #     abort(404)

        # No need to count if we're on the first page and there are fewer
        # items than we expected.
        # if page == 1 and len(items) < per_page:
        #     total = len(items)
        # else:
        #     total = self.order_by(None).count()

        # return [page, per_page, total, items]
        return page, per_page


from lxml import etree


def get_rid_of_html(html,xpahttype=1):
    try:
        tree=etree.HTML(html)

        result=tree.xpath('string(.)')
        result=result.replace(u'\xa0','').replace(u'\xa9','').replace('\n',' ')
        # print result
    # except etree.XMLSyntaxError:
    except Exception,e:
        end_result='no data'
        return end_result

    # dr = re.compile(r'<[^>]+>',re.S)
    # content_list = html.xpath('.//div[@class="p_content  "]').xpath('string(.)').extract()

    # content_list = tree.xpath('body/div//p ')#.xpath('string(.)')
    if xpahttype==1:
        content_list = tree.xpath('body/div//p')#.xpath('string(.)')
    else:
        pass

    if content_list:
        print u'news_content_p_list:',len(content_list)
        pass

        # content_list = tree.xpath('//body')#.xpath('string(.)')
    # content_list = tree.xpath('//body')#.xpath('string(.)')

    end_result=''
    for result in content_list:
        result=result.xpath('string(.)')
        result=result.strip('\n\t\r ')

        # print [result]
        # print '-'*100
        # dr = re.compile(r'<(\S*?)[^>]*>.*?|<.*? />|&.*?\;|if.*?|\$[a-z][;.\}\{:\n\f].*$',re.S)
        #第一次筛选，去掉匹配到的字符
        dr = re.compile(r'\$[a-zA-Z0-9]*|[a-zA-Z0-9].*?|[\(\./=/\[\]\"”“\&\\\?？\<\>\- -_——\|\*#\{\}].*?|\n{3,20}|\t{3,20}|https://.*?]',re.S)
        # dr = re.compile(r'\$[a-zA-Z0-9]*\b|[a-zA-Z0-9].*?|[\(\./=/\[\]\"”“&\\\?？<>\- -_——\|\*#\{\}].*?|\n{3,20}|\t{3,20}|//.*?-->',re.S)
        # dr = re.compile(r'\$[a-zA-Z0-9]*|[a-zA-Z0-9].*?|[\(\.=/\[\]\&\\\<\>\- -_——\|\*#\{\}].*?|\n{3,20}|\t{3,20}',re.S)
        # dr = re.compile(r'\$[a-zA-Z0-9]*|[a-zA-Z0-9].*?|[\(\.=/\[\]\&\\\<\>\- -_——\|\*#\{\}].*?|\n{3,20}|\t{3,20}',re.S)
        dd = dr.sub('',result)

        # dr = re.compile(r'\$[a-zA-Z0-9]*|[a-zA-Z0-9].*?|[\(\.=/\[\]\&\\\<\>\- -_——\|\*#\{\}].*?|\n{3,20}|\t{3,20}',re.S)
        # dd = dr.sub('',result)
        # print '-'*100
        # print [dd]
        # print '*'*100
        dr = re.compile(r'\$[a-zA-Z0-9]*|[a-zA-Z0-9].*?|[\(\./=/\[\]\"”“\&\\\?？\<\>\- -_——\|\*#\{\}].*?|\n{3,20}|\t{3,20}|https://.*?]',re.S)
        dd = dr.sub('',dd)




        stripinner=re.compile(r'\n{3,200}|\t{3,200}|\n\t{3,200}|[\u0020-\u9FA5]\\u',re.S)  #去掉3个以上的换行符去掉
        result=stripinner.sub('',dd)
        # result=stripinner.sub('',result)
        # print [result]
        # print '*'*100


        result=result.replace(u'\xa0','').replace(u'\xa9','').replace('\t','').replace('\r','')\
            .replace(u'\ue862','').replace(u'\u2003','').replace(u'\u2022','')\
            .replace(u'\ue861','').replace(u'\ue614','').replace(u'\ue60d','')\
            .replace(u'\ue60e','').replace(u'\ue62e','').replace(u'\ue60f','')\
            .replace(u'\ue633','').replace(u'\ue616','').replace(u'\ue635','')\
            .replace(u'\ue603','').replace(u'\ue634','').replace(u'\ue636','')\
            .replace(u'\ue660','').replace(u'\x93','')

        end_result=end_result+'\n'+result
        # result_len=len(result)
        # if len(end_result)<result_len:
        #     end_result=result.strip('\n\t\r ')
        #     print len(end_result),'->',result_len

        # result=result.replaceAll("[\u0020-\u9FA5]",'')
        # try:
        #     # pass
        #     print end_result
        # except UnicodeDecodeError,e:
        #     print e
        # except UnicodeEncodeError,e:
        #     print e
    # print [end_result]
    # print '-'*50
    try:
        pass
        # print [end_result]
        # print '-'*50
        # print end_result

    except UnicodeDecodeError,e:
        print '1',e
    except UnicodeEncodeError,e:
        print '2',e

    # print '-'*50

    return end_result
    # return unicode(end_result, "gbk")
    # return result