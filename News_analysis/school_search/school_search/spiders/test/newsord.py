#coding=utf-8
from scrapy import Spider, Request
from school_search.items import SchoolSearchItem
from bs4 import BeautifulSoup
import re

pat = re.compile(r'CDATA\[(.*?)\]')

class NewsSpider(Spider):

    name = 'newsold'
    # start_url = 'http://www.ynnu.edu.cn/dwr/call/plaincall/portalAjax.getNewsXml.dwr'
    start_url = 'http://www.ynnu.edu.cn/'
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

    def start_requests(self):
        for lei in self.zhonglei:
            self.body['c0-param1'] = lei
            x = ''
            for key, val in self.body.items():
                x += '%s=%s&' % (key, val)
            print(x)
            yield Request(self.start_url, self.parse, 'POST', body=x)

    def parse(self, response):
        items = []
        print response.url
        print response.text
        for found in pat.findall(response.text):
            if 'http://www.ynnu.edu.cn/newsitemcontent/' in found:
                items.append(found)
        items = list(set(items))
        for item in items:
            yield Request(item, self.parse_item)

    def parse_item(self, response):
        title = response.xpath(
            '//*[@id="139746300986343899"]/div[1]/h3/text()').extract()[0].split('\n')
        title = title[len(title) - 1]
        self.item['title'] = title.replace(u'\xe9','')
        self.item['url'] = response.url
        self.item['content'] = response.body_as_unicode()
        yield self.item


