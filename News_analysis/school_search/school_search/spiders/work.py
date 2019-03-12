#coding=utf-8
from scrapy import Spider, Request
from school_search.items import SchoolSearchItem
from bs4 import BeautifulSoup
import datetime
import time
import sys
from ..db import Spider as spidercontrl
from ..db import SpiderLog
from ..db import Query
from ..db import SchoolSearchDb



class WorkSpider(Spider):
    name = 'work'
    base_url = 'http://job.ynnu.edu.cn'
    start_url = 'http://job.ynnu.edu.cn/index.php/News/lists?t=zp&p={page}'
    item = SchoolSearchItem()

    def start_requests(self):
        for i in range(1, 13):
            spid=spidercontrl.get(name='news')
            print spid.command.strip(),'close...'
            if spid.command.strip()=='close...':
                sys.exit()
            else:
                yield Request(self.start_url.format(page=i), self.parse)

    def parse(self, response):
        urls = response.xpath(
            '//*[@id="yinFrame"]/div/div/ul/li/a/@href').extract()
        dbnews=spidercontrl.get(name='news')
        for url in urls:
            spid=spidercontrl.get(name='news')
            print spid.command.strip(),'close...'
            if spid.command.strip()=='close...':
                sys.exit()
            else:
                now=str(datetime.datetime.now()).split('.')[0].strip()
                print u'endtiming:',dbnews.endtiming,now
                if dbnews.endtiming.strip()==now:
                    sys.exit()
                else:
                    # yield Request(url, self.parse)

                    yield Request(self.base_url + url, self.parse_item)

    def parse_item(self, response):
        spid=spidercontrl.get(name='news')
        print spid.command.strip()
        if spid.command.strip()=='close...':
            sys.exit()

        soup = BeautifulSoup(response.body, 'lxml')
        self.item['content'] = soup.get_text(strip=True)
        h4 = soup.find('h4')
        self.item['title'] = h4.string if h4 else ''
        self.item['url'] = response.url


        yield self.item
