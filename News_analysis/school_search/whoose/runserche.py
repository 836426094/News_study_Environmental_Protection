#coding=utf-8
from flask import Flask, render_template, request, redirect, url_for, flash
from whoosh.index import open_dir
from whoosh import qparser
from whoosh.fields import TEXT,ID
# from school_search.db import Query, Visit, Seed
import os
from whoosh.index import create_in
# indexdir = 'indexdir/'
indexdir = 'E:\\oldcomputer\\Orders\\school_search\\indexdir\\'

ix = open_dir(indexdir)

app = Flask(__name__)


@app.route('/')
def index():
    visit = Visit.get(id=1)
    visit.count += 1
    visit.save()
    query = request.args.get('query', '')
    if query:
        querys = query.split(' ')
        for q in querys:
            Query.create(field=q)  #。。。
        mparser = qparser.MultifieldParser(
            ['title', 'content'], ix.schema, group=qparser.OrGroup)
        query = mparser.parse(query)
        searcher = ix.searcher()
        results = searcher.search(query)
        for i in results:
            print i

        # results = '你好'#searcher.search(query)
        print len(results),type(results)
        print results
        # for i in results:
        #     print results.index(i),i
        # searcher.close()
        return render_template('result.html', results=results)
    else:
        return render_template('index.html')



@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    querys = [x.field for x in Query.select()]
    unique_querys = list(set(querys))
    ret_querys = []
    for q in unique_querys:
        item = {}
        item['value'] = q
        item['count'] = len([x for x in querys if x == q])
        ret_querys.append(item)
    ret_querys = sorted(ret_querys, key=lambda x: x['count'], reverse=True)
    send = Seed.get(id=1)
    if request.method == 'POST':
        send.start_url = request.form['start_url']
        send.save()
        flash('修改种子网址成功')
        return redirect(url_for('statistics'))
    else:
        return render_template(
            'reportlist.html',
            querys=ret_querys,
            count=Visit.get(id=1).count,
            start_url=send.start_url
        )


if __name__ == '__main__':
    # app.secret_key = 'super secret key'
    # app.config['SESSION_TYPE'] = 'filesystem'
    # app.debug = True
    # app.run()
    query=u'老师'
    mparser = qparser.MultifieldParser(
            ['title', 'content'], ix.schema, group=qparser.OrGroup)
    query = mparser.parse(query)
    searcher = ix.searcher()
    results = searcher.search(query,limit=None)
    n=0
    for i in results:
        n+=1
        print n,i

    # results = '你好'#searcher.search(query)
    print len(results),type(results)
    print results


    print '---------------------'
    print results[0]