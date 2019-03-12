#coding=utf-8


import sqlite3

from configfile import sqllitfilepath

import datetime

#建表
def jianbiao():
    try:

        # cur.execute("create table catalog (id integer primary key,pid integer,name varchar(10) UNIQUE,nickname text NULL)")
        # gametype        VARCHAR (100),
        # score           VARCHAR (50),
        sql="""
     CREATE TABLE footballdatas (
            times                   DECIMAL (10, 3),
            timesdaxiao             VARCHAR (30),
            home_team               VARCHAR (100),
            SB                      VARCHAR (32),
            SBdaxiao                VARCHAR (30),
            visit_team              VARCHAR (100),
            Banchangjinqiushu       DECIMAL (10, 3),
            Banchangjinqiushudaxiao VARCHAR (30),
            gun                     VARCHAR (30),
            zhishu1                 DECIMAL (10, 3),
            zhishu1daxiao           VARCHAR (30),
            zhishu2                 DECIMAL (10, 3),
            zhishu2daxiao           VARCHAR (30),
            run_HZ_s                DECIMAL (10, 3),
            id                      INTEGER         PRIMARY KEY
                                                    DEFAULT (0),
            zhongpan                DECIMAL (10, 3),
            zanting                 VARCHAR (32),
            quit                    INTEGER (0)     DEFAULT (0)，
            Miyao                   VARCHAR (512)
        );

        """
        cur.execute(sql)
        # print u'表格成功，路径为：',sqllitfilepath
    except Exception,e:
        print u'sqlite3 in path',sqllitfilepath
        print Exception,e
        pass

# jianbiao()

class handle_sqlite():

    def __init__(self):
        # sqllitfilepath=os.getcwd()+'\\footboodDb.db'
        #也可以创建数据库在内存中。
        # con = sqlite3.connect(":memory:")
        # print sqllitfilepath
        # self.sqllitfile=sqllitfilepath
        # print sqllitfilepath
        self.conn = sqlite3.connect(sqllitfilepath)#"E:/test.db"
        self.cur=self.conn.cursor()
        self.create_table()
        pass
    def create_table(self):
        try:
            news_data='''
            create table news_data (
                    ID					int(20),
                    url	                varchar(250),
                    title	            varchar(250),
                    datatate	        varchar(100),
                    keyword	            varchar(100),
                    org_name	        varchar(100),
                    two_h_product	    varchar(100),
                    keywords	        varchar(250),
                    involving_org	    varchar(100),
                    two_h_products	    varchar(250),
                    content	            longtext,
                    content2	        longtext,
                    get_date	        varchar(100),
                    get_keyword_date	varchar(100),
                    status	            varchar(10),
                    hege	            varchar(10),
                    guid	            varchar(100),
                    source_site	        varchar(200),
                    wuran	            varchar(100),
                    fengxian	        varchar(100),
                    shengtai	        varchar(100),
                    ziyuan	            varchar(100),
                    xuanjiao	        varchar(100),
                    guanli	            varchar(100),
                    shuihj_2	        int(11) DEFAULT 0,
                    kongqi_2	        int(11) DEFAULT 0,
                    shenghj_2	        int(11) DEFAULT 0,
                    turang_2	        int(11) DEFAULT 0,
                    feiwu_2	            int(11) DEFAULT 0,
                    shengwu_2	        int(11) DEFAULT 0,
                    other_2             int(11) DEFAULT 0,
                    score				int(11) DEFAULT 0
                    );
                    '''
            self.cur.execute(news_data)
            self.conn.commit()
            print 'news_data created success.'
            news_result='''
                create table news_result (
                    ID					int(20),
                    url	                varchar(250),
                    title	            varchar(250),
                    datatate	        varchar(100),
                    keyword	            varchar(100),
                    org_name	        varchar(100),
                    two_h_product	    varchar(100),
                    keywords	        varchar(250),
                    involving_org	    varchar(100),
                    two_h_products	    varchar(250),
                    content	            longtext,
                    content2	        longtext,
                    get_date	        varchar(100),
                    get_keyword_date	varchar(100),
                    status	            varchar(10),
                    hege	            varchar(10),
                    guid	            varchar(100),
                    source_site	        varchar(200),
                    wuran	            varchar(100),
                    fengxian	        varchar(100),
                    shengtai	        varchar(100),
                    ziyuan	            varchar(100),
                    xuanjiao	        varchar(100),
                    guanli	            varchar(100),
                    shuihj_2	        int(11) DEFAULT 0,
                    kongqi_2	        int(11) DEFAULT 0,
                    shenghj_2	        int(11) DEFAULT 0,
                    turang_2	        int(11) DEFAULT 0,
                    feiwu_2	            int(11) DEFAULT 0,
                    shengwu_2	        int(11) DEFAULT 0,
                    other_2             int(11) DEFAULT 0,
                    score				int(11) DEFAULT 0

                    );
            '''
            self.cur.execute(news_result)
            self.conn.commit()
            print 'table news_result created success.'
        except Exception,e:
            print u'sqlite3 in path',sqllitfilepath
            print Exception,e

    def insertdata(self,sql):

        # times,timesdaxiao,home_team,SB,SBdaxiao,visit_team,Banchangjinqiushu,Banchangjinqiushudaxiao,gun,zhishu1,zhishu1daxiao,zhishu2,zhishu2daxiao,run_HZ_s=

        sql='''insert into footballdatas (times,timesdaxiao,home_team,SB,SBdaxiao,visit_team,Banchangjinqiushu,
                Banchangjinqiushudaxiao,gun,zhishu1,zhishu1daxiao,zhishu2,zhishu2daxiao,run_HZ_s)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''%('80','80','80','80','80','80','80','80','80','80','80','80','80','80')

        self.cur.execute(sql)
        self.conn.commit()

        # sql='Update footballdatas set times="%s" WHERE id=1'%(50)
        # cur.execute(sql)
        # cx.commit()
        # sql='''insert into footballdatas (times,timesdaxiao,home_team,SB,SBdaxiao,visit_team,Banchangjinqiushu,
        # Banchangjinqiushudaxiao,gun,zhishu1,zhishu1daxiao,zhishu2,zhishu2daxiao,run_HZ_s)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''%('80','80','80','80','80','80','80','80','80','80','80','80','80','80')
        # cur.execute(sql)
        # cx.commit()
        # print 'update ok'

    def Updata(self,sql):
        # sqlw='Update footballdatas set times="%s" WHERE id=1'%(80)
        self.cur.execute(sql)
        self.cx.commit()
    def select(self,idnum):
        sql='select * from footballdatas WHERE id="%s"'%idnum
        self.cur.execute(sql)
        data=self.cur.fetchall()[0]
        # datas=data
        # for i in data:
        #     datas.append(i)
        return data
    def drop_table(self):

        self.cur.execute('DROP TABLE IF EXISTS jd')
        self.conn.commit()
        print u'删除表成功'

    def inert(self):
        inserttime=str(datetime.datetime.now()).split('.')[0]
        sql_log='insert into t_fang_mx_log VALUES ("%s","%s","%s","%s","%s")'%(oid,web,price,hangqing,inserttime)
        self.cur.execute(sql_log)
        self.conn.commit()

    def findalldata(self,oid):
        # sql='select buytime,order_number,promotion_way,number,buyer,address,phone_number,total_amount,trade_name from jd'
        sql='select buytime,number,buyer,address,total_amount,phone_number from jd WHERE oid="%s"'%oid
        self.cur.execute(sql)
        da=self.cur.fetchall()
        data=[]
        for i in da:
            data.append(i)
        return data
    def find_user_data(self,email):
        # sql='select buytime,order_number,promotion_way,number,buyer,address,phone_number,total_amount,trade_name from jd'
        sql='select * from users WHERE email="%s"'%email
        self.cur.execute(sql)
        da=self.cur.fetchall()
        data=[]
        for i in da:
            data.append(i)
        return data


    def insert_many(self,datalist):
        # data=(callphone[0],holse[0],start_time[0],end_time[0],call_type,nativefee[0],otherfee[0],internet_traffic[0].strip('K'),calldate,oid)
        # datalist.append(data)

        sql='insert into xiciips (ip,port,adress,anonymous,types,speed,Connection_time,Survival_time,validation_time,timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        # print u'将插入',len(datalist),type(tuple(datalist)),u'条数据'
        try:
            self.cur.executemany(sql,datalist)  #datalist可以是list 也可以是tuple类型 datalist中的元素类别为:tuple(元组)
            self.conn.commit()
        except Exception,e:
            print u'数据库插入失败：',Exception,e
    def updata(self,name):
        sql='update status SET status=0 WHERE NAME = "%s"'%name
        self.cur.execute(sql)
        self.conn.commit()

    def find_all(self,sql):
        # sql='select * from users WHERE email="%s"'%email
        self.cur.execute(sql)
        da=self.cur.fetchall()
        data=[]
        for i in da:
            data.append(i)
        return data
    def find_return_cur(self,sql):
        self.cur.execute(sql)
        return self.cur

    def hand_free(self):
        return self.cur,self.conn



# sql="""
# select * from footballdata where
# yc_home_shuiwei<0.84 and yc_home_shuiwei>0.74 and
# yc_pankou<0.8 and yc_pankou>0.7 and
# yc_visting_shuiwei<1.001 and yc_visting_shuiwei>0.991 and
# yz_home_shuiwei<0.950 and yz_home_shuiwei>0.940 and
# yz_pankou<0.8 and yz_pankou>0.7 and
# yz_visting_shuiwei<0.891 and yz_visting_shuiwei>0.791
# ;
# """


