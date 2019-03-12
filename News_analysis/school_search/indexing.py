#coding=utf-8


# 建立索引模块
import os
from whoosh.index import create_in
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
from whoosh.index import open_dir
import json
from school_search.db import SchoolSearchDb

def jianli():
    # 使用结巴中文分词
    analyzer = ChineseAnalyzer()

    # 创建schema, stored为True表示能够被检索
    schema = Schema(title=TEXT(stored=True, analyzer=analyzer), url=ID(stored=True),
                    content=TEXT(stored=True, analyzer=analyzer))

    # 存储schema信息至'indexdir'目录下
    # indexdir = 'indexdir/'
    # indexdir = 'E:\\oldcomputer\\Orders\\school_search\\indexdir\\'
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

indexdir = 'indexdir/'
# indexdir = 'E:\\oldcomputer\\Orders\\school_search\\indexdir\\'
jianli()

if __name__ == '__main__':

    ix = open_dir(indexdir)
    # 创建一个检索器
    searcher = ix.searcher()
    # 检索标题中出现'云南'的文档
    results = searcher.find('title', u'优秀班主任')
    print results
    for r in results:
        print(r.fields())
        print(r.score)
        print('\n')
