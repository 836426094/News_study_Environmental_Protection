#coding=utf-8
import json
from scrapy import cmdline
# 建立索引模块
import os
from whoosh.index import create_in
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
from whoosh.index import open_dir
import multiprocessing
import json
import time
from school_search.db import SchoolSearchDb,Spider,SpiderLog,nowruning
# R=nowruning.get(id='1')

# indexpath=os.getcwd()+'\\keyword.txt'
indexdir = 'indexdir/'
# indexdir = 'E:\\oldcomputer\\Orders\\school_search\\indexdir\\'


def yb_runnews():
    p=multiprocessing.Process(target=run_news)
    p.start()

def yb_timing_runnews():
    while 1:
        news=Spider.get(name='news')
        now=str(datetime.datetime.now()).split('.')[0].strip()
        print news.starttiming,now
        if news.starttiming.strip()==now:
            print 'now run spider'
            p=multiprocessing.Process(target=run_news)
            p.start()
        else:
            if news.starttiming=='0':
                return 0
            else:
                time.sleep(1)
                continue
    time.sleep(1)

import sys
def Timing(T):
    while 1:
        now=str(datetime.datetime.now()).split('.')[0].strip()
        print T,now
        if T.strip()==now:
            return True
        else:
            time.sleep(1)
            continue
    time.sleep(1)


    # p=multiprocessing.Process(target=run_news)
    # p.start()
    # p=multiprocessing.Process(target=run_work,args=())
    # p.start()

def run_work():
    cmdline.execute("scrapy crawl work".split())     #ok

def run_news():
    oid=str(datetime.datetime.now())
    try:
        R=nowruning.get(id='1')
        R.oid=oid
        R.save()
    except Exception,e:
        nowruning.create(oid=oid)

    try:
        SpiderLog.create(oid=oid)
        cmdline.execute("scrapy crawl work".split())     #ok
        # cmdline.execute("scrapy crawl news".split())
    except Exception,e:
        print Exception,e

    finally:
        news=Spider.get(name='news')
        news.command='close...'
        news.running_status='close...'
        news.save()
        nowruns=nowruning.get(id=1)
        oid=nowruns.oid
        spilog=SpiderLog(oid=oid)
        spilog.endtime=datetime.datetime.now()
        spilog.save()
        print 'run over'

def jianli():
    # 使用结巴中文分词
    analyzer = ChineseAnalyzer()

    # 创建schema, stored为True表示能够被检索
    schema = Schema(title=TEXT(stored=True, analyzer=analyzer), url=ID(stored=True),
                    content=TEXT(stored=True, analyzer=analyzer))

    # 存储schema信息至'indexdir'目录下

    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    ix = create_in(indexdir, schema)

    # 按照schema定义信息，增加需要建立索引的文档
    writer = ix.writer()

    for item in SchoolSearchDb.select():
        # print(item.title.replace(u'\u2002','').replace(u'\u2022','').replace(u'\xa0','').replace(u'\xa9',''))
        writer.add_document(title=item.title, url=item.url,
                            content=item.content)
    writer.commit()




if __name__=="__main__":
    # cmdline.execute("scrapy crawl work".split())     #ok
    # cmdline.execute("scrapy crawl news".split())     #ok
    # yb_runnews()
    # yb_timing_runnews()
     # cmdline.execute("scrapy crawl work".split())




    try:
        news=Spider.get(name='news')
        news.command='runing...'
        news.running_status='runing...'
        news.starttiming_status='0'
        news.starttiming='0'
        news.endtiming_status='0'
        news.endtiming='0'
        news.save()
            # yb_timing_runnews()

    except Exception,e:
        print Exception,e
        Spider.create(name='news',command='0',running_status='0',
                     starttiming_status='0',starttiming='0',
                     endtiming_status='0',endtiming='0')
    news=Spider.get(name='news')
    # if form.get('status')=='runing...':
    #     news.command='close...'
    #     news.running_status='close...'
    #     news.save()
    # else:
    news.command='runing...'
    news.running_status='runing...'
    news.save()
    yb_runnews()