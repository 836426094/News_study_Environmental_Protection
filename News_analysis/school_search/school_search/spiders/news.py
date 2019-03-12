#coding=utf-8
from scrapy import Spider, Request
from school_search.items import SchoolSearchItem
from bs4 import BeautifulSoup
import re
from lxml import etree
import requests

from ..db import Spider as spidercontrl
from ..db import SpiderLog
from ..db import Query
from ..db import SchoolSearchDb
import datetime
import time
import json
import sys
pat = re.compile(r'CDATA\[(.*?)\]')



class NewsSpider(Spider):



    name = 'news'
    # start_url = 'http://www.ynnu.edu.cn/dwr/call/plaincall/portalAjax.getNewsXml.dwr'
    # start_url = 'http://www.ynnu.edu.cn/'

    start_url = []
    # f=open('E:\\oldcomputer\\Orders\\school_search\\school_search\\school_search\\spiders\\allurl.json','r')
    # allurl=json.load(f)
    # f.close()
    # start_url = allurl

    zhonglei = ['string:100400020405', 'string:100400020401',
                'string:100400020406', 'string:100400020404', 'string:1004000203']
    body = {
        'callCount': 1,
        'page': '/columnnewslist/100400020405.html',
        'httpSessionId': '6C6997F85D8DC2332F84BBB952F73356',
        'scriptSessionId': '54CB1AF777E225FBD349882D255C0673797',
        'c0-scriptName': 'portalAjax',
        'c0-methodName': 'getNewsXml',
        'c0-id': 0,
        'c0-param0': 'string:10040002',
        'c0-param1': 'string:100400020401',
        'c0-param2': 'string:news_',
        'c0-param3': 'number:10000',
        'c0-param4': 'number:1',
        'c0-param5': 'null:null',
        'c0-param6': 'null:null',
        'batchId': 0,
    }
    item = SchoolSearchItem()

    def set_start_url(self):
        quchong={}
        L=SchoolSearchDb.select(SchoolSearchDb.url)
        # # print len(L),type(L)
        for i in L:
            alt=i.url.strip()
            quchong[alt]=''
        #     if alt in quchong:
        #         print alt
        #     else:continue

        start = ['http://www.ynnu.edu.cn/sdxw1/xyxw.htm','http://www.ynnu.edu.cn/sdxw1/ywjj.htm',
                 'http://www.ynnu.edu.cn/sdxw1/tztg.htm','http://www.ynnu.edu.cn/sdxw1/mtsd.htm'
                 ]
        start_url=[]

        # print start_url
        for url in start:
            html=requests.get(url).content
            # print html
            shu=etree.HTML(html)
            allurlnum=shu.xpath('//*[@id="fanye140645"]/text()')
            allurlnum=int(allurlnum[0].replace(u'\xa0','').split('/')[1])
            # print allurlnum
            for num in range(allurlnum,allurlnum/2,-1):
                if 'xyxw' in url:alt='http://www.ynnu.edu.cn/sdxw1/xyxw/'  #校园新闻http://www.ynnu.edu.cn/sdxw1/xyxw/208.htm
                elif 'ywjj' in url:alt='http://www.ynnu.edu.cn/sdxw1/ywjj/' #要闻聚焦 http://www.ynnu.edu.cn/sdxw1/ywjj/157.htm
                elif 'tztg' in url:alt='http://www.ynnu.edu.cn/sdxw1/tztg/' #通知通告 http://www.ynnu.edu.cn/sdxw1/tztg/64.htm
                elif 'mtsd' in url:alt='http://www.ynnu.edu.cn/sdxw1/mtsd/' #媒体通知 http://www.ynnu.edu.cn/sdxw1/mtsd/157.htm
                urllink=alt+str(num)+'.htm'
                start_url.append(urllink)
                # print len(start_url),urllink

        #提取页面中的 文章的url
        allurl=[]
        n=0
        for url in start_url:
            html=requests.get(url).content
            # print html
            shu=etree.HTML(html)
            alts=shu.xpath('//tr/td/a[@class="c140645"]/@href')
            # print len(alts),alts
            for u in alts:
                u=u.replace('../..','http://www.ynnu.edu.cn')
                n+=1
                print n,len(allurl),u#,len(quchong)
                if u in quchong:
                    continue
                else:
                    quchong[u]=''
                    allurl.append(u)
                    # if len(allurl)==5:
                    #     return allurl
                    # return allurl
        return allurl


    def start_requests(self):
        start_url=self.set_start_url()
        dbnews=spidercontrl.get(name='news')
        for url in start_url:
            spid=spidercontrl.get(name='news')
            if spid.command.strip()=='close...':
                sys.exit()
            else:
                now=str(datetime.datetime.now()).split('.')[0].strip()
                print u'endtiming:',dbnews.endtiming,now
                if dbnews.endtiming.strip()==now:
                    sys.exit()
                else:

                    yield Request(url, self.parse)

    def parse(self, response):
        spid=spidercontrl.get(name='news')
        print spid.command.strip()
        if spid.command.strip()=='close...':
            sys.exit()

        print u'采集的url:',response.url
        title = response.xpath(
            '//h1[@align="center"]/text()').extract()[0].split('\n ')
        title = title[len(title) - 1]
        self.item['title'] = title.replace(u'\xe9','')
        self.item['url'] = response.url
        # self.item['content'] = response.body_as_unicode()
        soup = BeautifulSoup(response.body, 'lxml')
        self.item['content'] = soup.get_text(strip=True)

        yield self.item



# if __name__=="__main__":
#     set_start_url()