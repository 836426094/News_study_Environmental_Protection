#coding=utf-8

from userAgentfile import user_Agent
import random
import requests
from lxml import etree
import json
import time
from configfile import config
import datetime
from flasky.app.models import handle_mysql

handle_mysql=handle_mysql()

# url='http://www.xicidaili.com/nn'
url='http://www.xicidaili.com/nt'
headers={
    # GET /nn HTTP/1.1
'Host':'www.xicidaili.com',
'Connection': 'keep-alive',
'Cache-Control': 'max-age=0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
'Referer': 'http://www.xicidaili.com/',
'Accept-Encoding': 'gzip, deflate, sdch',
'Accept-Language': 'zh-CN,zh;q=0.8',
# 'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWIxNDA4ZDllZTE4M2U2N2I3MWFlMWM3OTkwMWIwZjI2BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMTZVUkRSZFIwWTgrYlR6eWZJbzlZN0pLV20rb3phVXlIU0tmK1JHVGhYTDA9BjsARg%3D%3D--390d5b1d623d26a07ffaf5f7a691d56c28e7c2e1; CNZZDATA1256960793=444393172-1487038685-%7C1487665544','If-None-Match': 'W/"5af76d7f3a24258c1f675fc1687387a7"'
}

#自由配置  使用代理了抓数据
def RequestsProxy_free(url,headerdata,dailiiplist):

        if dailiiplist:
            pass
        else:
            return None
        ip=random.choice(dailiiplist)
        print u'-------------------------------------当前使用的ip:',ip
        sockett=0
        # try:
        #     user_agent=random.choice(user_Agent)#"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
        #     session=requests.session()
        #     session.proxies={'http':'http://'+ip}
        #
        #     if headerdata.get('User-Agent'):
        #         pass
        #     else:
        #         headerdata['User-Agent']=user_agent
        #
        #     html=session.get(url,headers=headerdata,timeout=2)
        #     h=html.text
        #     return h
        # except:
        #     pass
        if headerdata.get('User-Agent'):
            pass
        else:
            headerdata['User-Agent']=random.choice(user_Agent)
        for ip in dailiiplist:
            try:
                # user_agent=random.choice(user_Agent)#"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
                session=requests.session()
                session.proxies={'http':'http://'+ip}
                # header={'User-Agent':user_agent}
                html=session.get(url,headers=headerdata,timeout=5)
                h=html.text
                if 'HTTP' in h:
                    return h
                else:
                    continue
            except:
                sockett+=1
                time.sleep(1)
                if sockett==len(dailiiplist):
                    print 'socket.error:',url,'ip',ip
                    return None
                continue


# html=requests.get(url='http://127.0.0.1:5000/data_analysis/daili',headers=headers).text
def get_iplist_spiter(url,headers,dailiiplist):

    html=RequestsProxy_free(url,headers,dailiiplist)
    if len(dailiiplist)==0 and html==None:
        html=requests.get(url,headers=headers).text
        # try:
        #     print url,html[:100].replace('\n','')
        # except Exception,e:
        #     print type(html),[html]
        #     print Exception,e
    # print '--------------------'
    if html:
        pass
    else:
        return None
    try:
        shu=etree.HTML(html)
        trs=shu.xpath('//tr')
    except Exception,e:
        print u'  匹配不到数据：',Exception,e
        return None
    print u'  数据提取成功：',len(trs)
    ipinfos=[]
    for tr in trs:
        tds=tr.xpath('td')
        ipinfolist=[] #每个ip的信息
        for td in tds:
            sudu=td.xpath('div')
            if sudu:
                data=td.xpath('div/@title')[0]
                # print u'速度',data,
            else:
                data=td.xpath('string(.)').strip().replace('\n','').replace('\t','').replace('\r','').replace(' ','')

            ipinfolist.append(data)
        ipinfos.append(ipinfolist)
        # print ' '
        # for td in tr:
        # print tr.xpath('string(.)').strip().replace('\n','|').replace('\t','').replace('\r','').replace(' ','')
    if len(ipinfos)==0:
        print u'why no data:',html
    return ipinfos
    # for info in ipinfos:
    #     for i in info:
    #         print info.index(i),i,
    #     print ''
    # 0  1 119.181.28.115 2 9999 3 山东济宁 4 高匿 5 HTTP 6 0.209秒 7 0.041秒 8 4分钟 9 17-02-2113:50
    # 0  1 106.46.136.64 2 808 0  4 高匿 5 HTTP 6 2.339秒 7 0.467秒 8 42天 9 17-02-2113:46
    # 0  1 112.67.238.90 2 9999 3 海南海口 4 高匿 5 HTTP 6 0.343秒 7 0.068秒 8 1分钟 9 17-02-2113:45

#运行采集程序 自动筛选出存活时间为小时级别以上的代理存入
def mainspiter():
    filename=config['iplist_filename']
    f=open(filename,'r')
    dailiiplist=json.load(f)
    f.close()
    # print len(dailiiplist),dailiiplist
    ips=[]
    nfk=0
    for i in range(1,3):
        url='http://www.xicidaili.com/nt/'+str(i)
        # print len(dailiiplist)
        print url
        dailiinfos=get_iplist_spiter(url,headers,dailiiplist)  #采集一个页面的代理ip并且返回一个页面的代理ip
        if dailiinfos:
            pass
        else:
            # print u'  采集完了没有数据：',url
            # print dailiinfos
            continue
        # print len(dailiinfos),dailiinfos

        onepagelist=[]
        for ipmsgli in dailiinfos:
            if len(ipmsgli)==0:
                continue
            nfk+=1
            try:
                if u'分钟' in ipmsgli[8] or u'秒' in ipmsgli[8]:
                    continue
                ipaddr=ipmsgli[1]+':'+ipmsgli[2]
                print nfk,
                datelist=[]
                for y in  ipmsgli:
                    datelist.append(y)
                    print ipmsgli.index(y),':',y,
                print ''
                ip,port,adress,anonymous,types,speed,Connection_time,Survival_time,validation_time,timestamp\
                    =datelist[1],datelist[2],datelist[3],datelist[4],datelist[5],datelist[6],datelist[7],datelist[8],datelist[9],datetime.datetime.now()
                datatuple=(datelist[1],datelist[2],datelist[3],datelist[4],datelist[5],datelist[6],datelist[7],datelist[8],datelist[9],datetime.datetime.now())
                onepagelist.append(datatuple)
            except IndexError,e:
                print ''
                print nfk,IndexError,e
                print dailiinfos
                # print u'Error:',ipmsgli
                continue
            ips.append(ipaddr)
            dailiiplist.append(ipaddr)

        handle_mysql.insert_many(onepagelist)

        # print dailiiplist
        # print ips
    if len(ips)>0:
        f=open(filename,'w+')
        json.dump(ips,f)
        f.close()
    handle_mysql.updata('xiciips')
    return ips


def check_ip(dailiiplist):


    filename=config['checkiplist_filename']
    headerdata={
    # GET /?from=navigation HTTP/1.1
    'Host': 'changge.anjuke.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Referer': 'http://changge.anjuke.com/community/?from=navigation',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cookie': 'als=0; isp=true; Hm_lvt_c5899c8768ebee272710c9c5f365a6d8=1487569735; ctid=306; lps=http%3A%2F%2Fwww.anjuke.com%2F%7C; sessid=33673AD9-E6F3-1AE3-078E-CD8093C5C63F; __xsptplusUT_8=1; aQQ_ajkguid=E1C42C0F-3EBA-D191-42EF-1251DB5E307B; twe=2; __xsptplus8=8.26.1487730768.1487732120.4%232%7Cwww.so.com%7C%7C%7C%25E5%25AE%2589%25E5%25B1%2585%25E5%25AE%25A2%7C%23%23wLqI6VGIkhTgnuBpAXqE6yqs3GKtLf_L%23; _ga=GA1.2.1683959185.1480556960; _gat=1; 58tj_uuid=cf1c1ccf-7464-4c04-8802-8de6ed6b9129; new_session=0; init_refer=; new_uv=27',
    }
    url='http://changge.anjuke.com/'
    checkips=[]
    for i in dailiiplist:
        try:
            user_agent=random.choice(user_Agent)#"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
            session=requests.session()
            session.proxies={'http':'http://'+i}
            if headerdata.get('User-Agent'):
                pass
            else:
                headerdata['User-Agent']=user_agent
            respone=session.get(url,headers=headerdata,timeout=5)
            # print respone.status_code
            # print respone.text
            print respone.status_code
            if respone.status_code==200:
                checkips.append(i)
        except ZeroDivisionError:
            pass
        except Exception,e:
            print Exception,e
        print '   ',len(dailiiplist),dailiiplist.index(i),len(checkips)
    f=open(filename,'w+')
    json.dump(checkips,f)
    f.close()



if __name__=="__main__":
    dailiiplist=mainspiter()
    # f=open(config['iplist_filename'],'r')
    # dailiiplist=json.load(f)
    # f.close()
    # check_ip(dailiiplist)