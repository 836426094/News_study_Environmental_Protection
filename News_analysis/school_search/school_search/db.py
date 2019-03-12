#coding=utf-8
import peewee
import peewee as pe
from datetime import datetime
# myDB = pe.MySQLDatabase("spider", host="127.0.0.1",
#                         port=3306, user="root", passwd="")
myDB = pe.MySQLDatabase("spiter", host="127.0.0.1",
                        port=3306, user="bian", passwd="123456")


# 爬虫抓取网页表
class SchoolSearchDb(pe.Model):
    title = pe.CharField(default='')
    url = pe.CharField(default='')
    content = pe.TextField(default='')

    class Meta:
        database = myDB


# 查询词表
class Query(pe.Model):
    field = pe.CharField(default='')
    # querytime=pe.DateField(default='')
    querytime = pe.DateField(default=datetime.date(datetime.today()))
    class Meta:
        database = myDB


# 访问量表
class Visit(pe.Model):
    count = pe.IntegerField(default=0)
    visittime = pe.DateField(default=datetime.date(datetime.today()))
    class Meta:
        database = myDB


# 种子链接表
class Seed(pe.Model):
    start_url = pe.CharField(default='')

    class Meta:
        database = myDB

# 爬虫日志
class SpiderLog(pe.Model):
    oid = pe.CharField(default='')
    starttime = pe.DateTimeField(default=datetime.now())#datetime.date(datetime.today())
    # endtime = pe.DateField()
    endtime = pe.DateTimeField(null=True)
    updatacount = pe.IntegerField(default=0)

    class Meta:
        database = myDB
# 当前运行
class nowruning(pe.Model):
    oid = pe.CharField(default='')
    class Meta:
        database = myDB
# 爬虫控制
class Spider(pe.Model):
    name = pe.CharField()
    command=pe.CharField()#手动运行命令
    running_status= pe.CharField() #运行状态

    starttiming_status= pe.CharField()
    starttiming = pe.CharField()#pe.DateField(default=datetime.date(datetime.today()))

    endtiming_status= pe.CharField()#pe.IntegerField(default=0)
    endtiming = pe.CharField()#pe.DateField(default=datetime.date(datetime.today()))

    updatacount = pe.IntegerField(default=0)

    class Meta:
        database = myDB

if __name__ == '__main__':
    try:
        SchoolSearchDb.create_table()
    except pe.InternalError:
        print('schoolsearchdb 表已经存在！')
    except peewee.OperationalError:
            print('query 表已经存在！')
    try:
        Query.create_table()
    except pe.InternalError:
        print('query 表已经存在！')
    except peewee.OperationalError:
            print('query 表已经存在！')

    try:
        Visit.create_table()
        Visit.create(count=0)
    except pe.InternalError:
        print('visit 表已经存在！')
    except peewee.OperationalError:
        print('query 表已经存在！')


    try:
        Seed.create_table()
        Seed.create(start_url='http://www.ynnu.edu.cn/default.html')
    except pe.InternalError:
        print('send 表已经存在！')
    except peewee.OperationalError:
            print('query 表已经存在！')

    try:
        Spider.create_table()
    except pe.InternalError:
        print('send 表已经存在！')
    except peewee.OperationalError:
            print('query 表已经存在！')

    try:
        SpiderLog.create_table()
    except pe.InternalError:
        print('send 表已经存在！')
    except peewee.OperationalError:
            print('query 表已经存在！')
    try:
        nowruning.create_table()
    except pe.InternalError:
        print('send 表已经存在！')
    except peewee.OperationalError:
            print('query 表已经存在！')


    Spider.create(name='news',command='0',running_status='0',
                         starttiming_status='0',starttiming='0',
                         endtiming_status='0',endtiming='0')