# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from school_search.db import SchoolSearchDb,Spider,SpiderLog

import datetime
import time
import sys
from db import Spider as spidercontrl
from db import SpiderLog
from db import Query
from db import SchoolSearchDb,nowruning



class SchoolSearchPipeline(object):

    def process_item(self, item, spider):
        # print item['title'],type(item['title'])
        # title=unicode(item['title']).encode('utf-8')
        title=item['title'].replace(u'\u2002','').replace(u'\u2022','').replace(u'\xa0','').replace(u'\xa9','')
        # title=unichr(item['title'])
        try:
            print "title:",title,type(title)
        except Exception,e:pass
        s=item['content'].replace(u'\u2002','').replace(u'\u2022','').replace(u'\xa0','').replace(u'\xa9','')
        # print "type(item['content']):",type(item['content']),s
        print item['url']
        # try:
        #     print s
        # except Exception,e:print Exception,e
        db = SchoolSearchDb(title=title, url=item[
                            'url'], content=s)
        db.save()

        running=nowruning.get(id=1)
        oid=running.oid

        Spilog=SpiderLog.get(oid=oid)
        Spilog.updatacount+=1
        Spilog.save()