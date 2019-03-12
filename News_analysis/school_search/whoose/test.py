#!/usr/bin/env
#coding:utf-8
from whoosh.fields import *
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.qparser import QueryParser


def createIndexs(dirName):
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
    ix = create_in(dirName, schema)
    writer = ix.writer()
    writer.add_document(title=u"First document",
                        path=u"/a",
                        content=u"This is the first document we've added!")
    writer.add_document(title=u"Second document",
                        path=u"/b",
                        content=u"The second one is even more interesting!")
    writer.add_document(title=u"edc document",
                        path=u"/c",
                        content=u"The edc's demo!")
    p = writer.commit()

# def query(dirName,key):
#     ix = open_dir(dirName)
#     with ix.searcher() as searcher:
#         query = QueryParser("title", ix.schema).parse(key)
#         results = searcher.search(query)
#         return {"total":len(results),"items":results}
#
def query(dirName, key,pageLen,pageNum):
    ix = open_dir(dirName)
    with ix.searcher() as searcher:
        parser = QueryParser("title", ix.schema)
        myquery = parser.parse(key)
        print myquery

        results = searcher.search_page(myquery, int(pageNum), pagelen=pageLen)

        output = []
        for item in results:
            output.append(item.fields())

        return {'pageTotal':results.pagecount,
                'pageNum':results.pagenum,
                'pageLen':results.pagelen,
                'total': results.total,
                'ids': output}



if __name__ == '__main__':
    # createIndexs("indexDir")

    # rt = query(indexdir,u'新闻')
    # print rt
    indexdir='E:\\oldcomputer\\Orders\\school_search\\indexdir\\'
    # results = query(dirName=indexdir, key='document OR path:/c',pageLen=1,pageNum=2)
    # print results

    from whoosh.index import create_in
    from whoosh.fields import *
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True),   content=TEXT)
    ix = create_in(indexdir, schema)
    writer = ix.writer()
    writer.add_document(title=u"First document", path=u"/a",
        content=u"This is the first document we've added!")
    writer.add_document(title=u"Second document", path=u"/b",
        content=u"The second one is even more interesting!")
    writer.commit()
    from whoosh.qparser import QueryParser
    with ix.searcher() as searcher:
          query = QueryParser("content", ix.schema).parse("first")
          results = searcher.search(query)

    print results

      # {"title": u"First document", "path": u"/a"}