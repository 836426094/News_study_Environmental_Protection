#coding=utf-8
from flask import Flask, render_template, request, redirect, url_for, flash
from whoosh.index import open_dir
from whoosh import qparser,query
from whoosh.fields import TEXT,ID

from school_search.db import Query, Visit, Seed,SpiderLog,Spider,nowruning,myDB
import os
from whoosh.index import create_in

from playhouse.flask_utils import FlaskDB
from runscrapy import yb_runnews,yb_timing_runnews
# indexdir = 'indexdir/'
indexdir = 'E:\\oldcomputer\\Orders\\school_search\\indexdir\\'
import datetime
import time
ix = open_dir(indexdir)

app = Flask(__name__)
import json
@app.route('/')
def index():
    from datetime import datetime
    try:
        visit = Visit.get(visittime=datetime.date(datetime.today()))
        visit.count += 1
        visit.save()
    except:
        Visit.create(count=1,visittime=datetime.date(datetime.today()))

    query_string = request.args.get('query', '').strip()
    filterstring=request.args.get('filterstring', '')
    page=request.args.get('page', '')
    try:
        page=int(page)
    except:page=1
    # print u'获取分页值',page

    if query_string:

        querys = query_string.split(' ')
        for q in querys:
            if q==' ' or len(q.strip())=='':continue
            Query.create(field=q)  #关键词提取存储

        #new start
        myindex=ix
        search=myindex.searcher()
        try:
            qp=qparser.MultifieldParser(
                ['title', 'content'], ix.schema, group=qparser.OrGroup)
            user_query=qp.parse(query_string)

            #Only show documents in the 'rendering' chapter  过滤器 被允许的
            # print (user_query,type(user_query))
            if len(filterstring.strip())==0 or filterstring.strip()=='':
                results = search.search_page(user_query,page,pagelen=10)
            else:
                allow_query=query.Term('content',filterstring)
                results = search.search_page(user_query,page,pagelen=10,filter=allow_query)

            # pass
            pagenum=int(len(results)/10+1)
            pageurllist=['zhanwei']
            for i in range(1,pagenum):
                pageurl='/?query='+query_string+'&filterstring='+filterstring+'&page='+str(i)
                pageurllist.append(pageurl)

            return render_template('result2.html', results=results,pagination=pagenum,pageurllist=pageurllist,nowpage=int(page))
        finally:
            search.close()

    else:
        from datetime import datetime
        return render_template('index.html',current_time=datetime.utcnow())

@app.route('/statistics', methods=['GET', 'POST'])
def statistics():

    date = request.args.get('date', '').strip()
    # page=request.args.get('page', '')
    # try:
    #     page=int(page)
    # except:page=1
    # print u'date:',date,type(date)
    if date:
        date=int(date)
        timeStamp=time.time()
        dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
        threeDayAgo = dateArray - datetime.timedelta(days = date) #date=3 or oth
        # print u'几天以前的：',threeDayAgo
        datedata=str(threeDayAgo).split()[0]
        # datenum=request.args.get('date', '')
        # print u'dada',datenum
        # date=str(datetime.datetime.now()).split()[0]
    else:
        date=3
        timeStamp=time.time()
        dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
        threeDayAgo = dateArray - datetime.timedelta(days = date) #date=3 or oth
        # print u'几天以前的：',threeDayAgo
        datedata=str(threeDayAgo).split()[0]


    querys = [x.field for x in Query.select().where(Query.querytime >= datedata)  ]
    unique_querys = list(set(querys)) #去重并list化去重之后的set
    ret_querys = []
    for q in unique_querys:
        item = {}
        item['value'] = q
        item['count'] = len([x for x in querys if x == q])
        ret_querys.append(item)
    ret_querys = sorted(ret_querys, key=lambda x: x['count'], reverse=True)
    send = Seed.get(id=1)
    # print send.start_url,type(send.start_url)

    #
    Vsts=Visit.select()

    Vststime=[]
    for x in Vsts:
        # print str(x.visittime).strip(),type(str(x.visittime).strip())
        d=str(x.visittime)[-5:].replace('-','.').decode('utf-8')
        # print d,type(d),float(d),type(float(d))
        # d=float(d)
        # print d,type(d),round(d,3),type(round(d,3))
        # d=str(float(d))
        # if len(d.split('.')[1])<2:
        #     d=d+'0'

        d=str(d)
        d=round(float(d), 3)
        d=str("%.2f"%d)
        # d=float(d)
        print d,type(d)
        Vststime.append(d)
        # Vststime.append(d.strip())
    # Vststime='['+Vststime.strip(',')+']'

    Vststime=json.dumps(Vststime)
    print Vststime,type(Vststime)
    Vststime=Vststime.replace('"','')
    # print Vststime

    # Vststime=json.loads(Vststime)
    # print Vststime
    Vstscount = [x.count for x in Vsts]
    # print Vststime
    # print Vstscount
    if request.method == 'POST':
        form = request.form
        # print u'fdafdsa',form
        send.start_url = request.form['start_url']
        send.save()
        flash('修改种子网址成功')
        return redirect(url_for('statistics'))

    else:
        return render_template(
            # 'reportlist.html',
            'statistics.html',
            querys=ret_querys,
            # count=Visit.get(id=1).count,
            count=sum(Vstscount),
            start_url=send.start_url.decode('gbk').encode('utf-8'),
            Vststime=Vststime,
            Vstscount=Vstscount,
            date=date
        )

@app.route('/spiter', methods=['GET', 'POST'])
def spider():
    querys = [x.field for x in Query.select()]
    # print querys
    unique_querys = list(set(querys))
    ret_querys = []
    for q in unique_querys:
        item = {}
        item['value'] = q
        item['count'] = len([x for x in querys if x == q])
        ret_querys.append(item)
    ret_querys = sorted(ret_querys, key=lambda x: x['count'], reverse=True)
    send = Seed.get(id=1)
    try:
        nowrun=nowruning.get(id=1)
        oid=nowrun.oid
        sdlog=SpiderLog.get(oid=oid)
        updatacount=sdlog.updatacount
    except:
        nowrun=nowruning.create(oid=' ')
        updatacount=0

    if request.method == 'POST':
        form = request.form
        print form
        n=0
        for i in form:
            print n,i,form[i]
            n+=1
        s = lambda x:'0' if x==None or x.strip()==''  else x
        try:
            if form['formtype']=='manual':
                news=Spider.get(name='news')
                if form.get('status')=='runing...':
                    news.command='close...'
                    news.running_status='close...'
                    news.save()
                else:
                    news.command='runing...'
                    news.running_status='runing...'
                    news.save()
                    yb_runnews()
            else:
                news=Spider.get(name='news')
                # news.command=s(form.get('nowrun_news'))
                # news.running_status=s(form.get('nowrun_news'))
                news.starttiming_status=s(form.get('news_starttiming_status'))
                news.starttiming=s(form.get('news_starttiming'))
                news.endtiming_status=s(form.get('news_endtiming_status'))
                news.endtiming=s(form.get('news_endtiming'))
                news.save()
                yb_timing_runnews()

        except Exception,e:
            print Exception,e
            Spider.create(name='news',command=s(form.get('nowrun_news')),running_status=s(form.get('nowrun_news')),
                         starttiming_status=s(form.get('news_starttiming_status')),starttiming=s(form.get('news_starttiming')),
                         endtiming_status=s(form.get('news_endtiming_status')),endtiming=s(form.get('news_endtiming')))

        return redirect(url_for('spider'))

    else:
        news=Spider.get(name='news')
        # if news.running_status=='1':
        #     news_status=1
        # else:news_status=0
        # print news.running_status
        return render_template(
            'spider.html',
            querys=ret_querys,
            count=Visit.get(id=1).count,
            start_url=send.start_url,
            news_status=news.running_status,news=news,updatacount=updatacount
        )


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(host='0.0.0.0',port=5000)

    FlaskDB(app,myDB)
    # query=u'考试'
    # mparser = qparser.MultifieldParser(
    #         ['title', 'content'], ix.schema, group=qparser.OrGroup)
    # query = mparser.parse(query)
    # searcher = ix.searcher()
    # results = searcher.search(query)
    # for i in results:
    #     print i
    #
    # # results = '你好'#searcher.search(query)
    # print len(results),type(results)
    # print results