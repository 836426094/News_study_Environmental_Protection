#coding=utf-8


import multiprocessing
import time

import random
import os
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import *
import time
from selenium import webdriver

def getd():
    driver=webdriver.Firefox()
    return driver

def proxy_get(url,iplist,driver):
    try:
        if driver:
            pass
        else:
            driver=getd()
        start=time.time()
        proxytem=webdriver.Proxy()
        proxytem.proxy_type=ProxyType.MANUAL
        # proxytem.http_proxy='139.196.140.9:80'  #只要代理ip可用 就可以代理访问
        networdip=random.choice(iplist)#'203.19.34.146:8080'#
        print networdip
        proxytem.http_proxy= networdip
        #proxiip.proxy
        proxytem.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
        driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
        driver.get(url)
        driver.implicitly_wait(10)
        html=driver.page_source
        # l=[]
        # l.append(html)
        end=time.time()
        print u'耗时',end-start
        if u'安居客' in html:
            return driver,True
        else:
            return driver,False
        # driver.quit()
        # print networdip,'---Success!'
    except Exception,e:
        print u'ip',Exception,e
        # try:
        #     driver.quit()
        #     pass
        # except:
        #     pass
        return driver,False
    # return driver

def get_proxyip():
    # f=open('C:\\spiters\\Shua_liang\\dailiip.txt','r')
    # iplistyuanshi=f.readlines()
    # f.close()
    # iplist=[]
    # for i in iplistyuanshi:
    #     ip=i.strip().split('@')[0]
    #     # print iplistyuanshi.index(i), ':', ip
    #     if 'HTTP' in ip:
    #         continue
    #     if len(ip)>21:
    #         # print iplistyuanshi.index(i), ':', ip, i
    #         continue
    #     iplist.append(ip)
    # ['202.197.127.139:1209', '124.88.67.54:80', '115.231.105.109:8081', '116.52.7.139:8080', '221.237.154.57:9797', '175.151.117.171:80', '116.62.45.185:3128', '27.191.234.69:9999', '113.65.20.176:9999', '221.235.21.168:8998', '61.177.75.214:3128', '119.137.32.190:8088', '124.89.35.206:9999', '180.97.80.235:3128', '61.152.81.193:9100', '113.108.141.98:9797', '113.105.80.61:8080', '221.8.25.243:9999', '119.130.115.226:808', '182.39.153.2:8118', '211.87.235.35:9999', '49.74.87.192:8123', '61.162.223.41:9797', '183.131.151.208:80', '123.138.89.130:9999', '58.251.132.181:8888', '116.216.128.2:8118', '60.13.143.99:8080', '180.97.81.234:3128', '125.93.148.174:9000', '202.202.90.20:8080', '110.73.9.226:9999', '113.66.147.25:9999', '60.211.213.34:8080', '124.127.255.27:8080', '222.161.56.166:9000', '118.144.48.91:3128', '183.63.14.107:808', '183.16.5.130:8123', '118.119.168.172:9999', '123.55.194.43:9999', '125.217.199.148:8197', '218.56.132.157:8080', '121.8.170.53:9797', '60.191.134.162:9999', '124.128.221.27:8080', '221.193.235.94:9999', '218.56.132.156:8080', '221.193.235.90:9999', '219.145.244.250:3128', '218.56.132.158:8080', '122.72.32.75:80', '58.217.195.141:80', '1.82.216.135:80', '119.55.89.142:9999', '222.186.161.215:3128', '124.88.67.30:80', '125.88.39.73:80', '121.32.251.43:80', '211.98.156.104:8080', '118.144.154.253:3128', '123.139.56.234:9999', '182.44.148.179:9000', '218.75.116.58:9999', '119.188.162.218:8080', '183.45.172.82:9797', '42.157.7.43:9999', '203.91.121.74:3128', '124.207.132.242:3128', '221.237.154.58:9797', '210.75.21.251:1920', '120.24.83.57:8118', '111.123.43.155:3128', '183.19.43.222:3128', '180.97.80.170:3128', '221.229.252.98:8080', '124.207.82.166:8008', '180.169.59.221:8080', '180.169.59.222:8080', '162.105.80.111:3128', '218.66.253.144:8800', '123.233.120.26:8080', '27.46.97.4:9797', '113.200.29.10:9999', '101.230.214.25:8080', '115.154.144.21:1080', '101.251.199.66:3128', '110.6.222.103:8118', '121.13.165.15:9797', '180.97.81.133:3128', '114.215.192.135:8118', '110.73.182.12:9000', '222.29.45.161:808', '113.222.80.187:3128', '61.185.137.126:3128', '112.243.24.222:9999', '58.67.159.50:80', '60.160.128.10:9797', '36.110.90.179:8123', '27.205.93.33:9999', '112.91.218.21:9000', '58.252.73.14:9090', '119.29.177.147:3128', '123.138.216.91:9999', '101.81.143.162:9000', '59.61.89.230:8800', '59.61.89.233:8800', '123.7.38.31:9999', '218.31.56.238:9999', '113.66.147.42:9999', '61.163.236.177:9999', '61.158.187.157:8080', '222.186.45.115:62222', '220.113.26.18:8080', '61.153.232.218:8080', '115.238.228.9:8080', '220.164.18.225:8081', '180.97.80.19:3128', '125.93.148.25:9000', '118.116.251.107:8118', '59.41.214.218:3128', '218.87.109.30:80', '118.178.124.33:3128', '125.40.24.202:9999', '120.27.110.37:3128', '1.27.58.14:8118', '221.204.11.8:8080', '113.109.27.102:8118', '111.177.124.140:9797', '180.97.80.20:3128', '42.122.40.80:8123', '101.200.43.104:8080', '121.13.164.227:9797', '59.47.125.10:9797', '115.236.8.235:3128', '58.52.201.119:8080', '113.110.208.245:9999', '60.174.237.43:9999', '124.193.85.88:8080', '113.65.20.117:9999', '121.17.126.68:8081', '58.213.19.233:10081', '110.73.5.25:9999', '125.93.149.85:9000', '112.90.18.121:80', '182.92.207.196:3128', '125.37.210.63:9999', '180.97.81.215:3128', '218.6.145.11:9797', '180.97.80.82:3128', '180.97.80.78:3128', '125.93.148.195:9000', '125.93.149.88:9000', '113.108.253.195:9797', '58.249.55.222:9797', '218.28.176.246:8080', '110.206.127.136:9797', '125.93.149.149:9000', '202.170.139.100:1920', '14.28.139.220:8088', '222.82.222.242:9999', '124.88.67.39:80', '113.65.161.113:9797', '125.45.87.12:9999', '222.217.19.248:8080', '113.18.193.9:80', '36.110.14.98:8888', '116.242.227.201:3128', '119.131.118.43:9797', '112.109.137.95:8118', '112.95.81.130:9999', '119.128.112.110:9797', '183.61.163.59:8080', '42.196.254.182:8080', '60.160.34.4:3128', '218.6.79.198:3128', '113.18.193.24:8080', '113.18.193.17:8080', '113.18.193.21:8000', '42.51.4.25:80', '219.132.232.77:9797', '120.35.30.178:80', '218.77.83.89:3128', '119.141.101.5:9797', '125.81.104.124:8123', '183.56.177.130:808', '119.52.11.14:9999', '113.18.193.19:8080', '113.18.193.25:8000', '124.88.67.22:80', '221.237.155.64:9797', '101.254.232.74:9999', '60.191.164.83:3128', '113.66.141.251:9797', '113.79.74.176:9797', '222.186.45.117:55336', '218.86.60.18:808', '119.165.74.210:9999', '219.150.242.54:9999', '59.51.27.213:3128', '218.75.149.207:3128', '1.27.182.29:8118', '122.227.167.230:8080', '115.236.166.125:8080', '119.145.203.58:80', '223.15.32.8:9797', '1.85.216.142:8118', '222.35.86.1:8080', '119.131.64.104:8118', '60.191.159.86:3128', '122.224.183.170:9999', '124.239.177.85:8080', '115.154.15.59:8123', '220.249.185.178:9999', '122.195.244.134:8080', '118.144.213.85:3128', '118.144.213.89:3128', '123.13.204.109:9999', '125.93.148.104:9000', '218.94.123.143:8080', '218.76.84.206:3128', '61.136.79.240:9000', '59.36.234.80:8118', '163.125.195.123:8118', '27.46.97.3:9797', '27.46.50.13:9797', '180.97.237.199:8080', '60.206.229.152:3128', '113.18.193.26:80', '180.97.80.84:3128', '115.28.235.0:3128', '113.226.77.233:8118', '120.26.242.41:8123', '218.56.132.154:8080', '113.119.121.66:9999', '171.36.62.173:9797', '125.93.149.214:9000', '202.97.156.247:80', '120.132.71.212:80', '113.79.74.219:9797', '110.182.78.65:9797', '14.119.209.118:9797', '220.249.101.159:80', '125.93.149.170:9000', '119.129.96.58:9797', '202.105.111.232:9000', '113.18.193.16:8080', '122.226.62.90:3128', '125.40.26.99:9797', '124.79.217.88:8118', '110.182.102.175:9797', '222.22.73.50:8998', '183.54.205.130:9797', '113.18.193.20:8080', '113.18.193.12:8080', '124.88.67.34:80', '123.52.130.3:9999', '58.38.59.246:9000', '221.204.101.103:9797', '123.163.79.80:9000', '60.207.239.245:3128', '183.53.65.203:808', '61.129.129.72:8080', '122.72.18.160:80', '221.204.98.107:9797', '125.93.148.156:9000', '183.31.179.240:9797', '113.98.96.37:3128', '125.93.148.143:9000', '113.99.130.191:9000', '119.254.92.53:80', '222.186.45.59:62386', '211.87.227.204:3128', '113.222.81.111:3128', '60.207.239.247:3128', '60.207.189.250:3128', '14.211.132.246:9797', '113.18.193.14:8080', '120.84.230.75:9000', '116.16.100.211:9000', '111.194.98.134:9797', '121.204.165.115:8118', '183.29.252.86:9000', '125.40.26.63:9797', '222.217.19.242:8080', '171.217.113.169:9797', '60.191.174.227:3128', '218.56.132.155:8080', '162.105.71.173:8118', '123.13.205.185:8080', '1.85.219.166:8118', '124.202.131.164:8080', '221.214.110.130:8080', '113.65.20.50:9999', '223.13.65.250:9797', '58.252.6.165:9000', '222.85.2.12:8080', '119.52.63.78:9999', '121.69.26.14:8080', '182.92.103.13:8118', '218.241.234.48:8080', '182.44.143.8:9000', '221.204.102.148:9797', '113.77.179.150:9999', '210.73.220.83:8088', '123.138.89.131:9999', '210.73.220.79:8088', '210.73.220.78:8088', '210.73.220.91:8088', '221.238.72.196:8998', '210.73.220.84:8088', '119.100.214.192:8998', '121.41.6.85:3128', '113.18.193.27:8000', '183.31.141.113:9797', '60.176.203.2:9999', '113.66.147.169:9999', '183.63.110.202:3128', '58.255.44.32:9000', '113.109.25.186:808', '113.65.10.134:9797', '114.249.18.240:9999', '221.204.102.186:9797', '59.78.45.37:1080', '222.89.10.28:9000', '1.207.62.194:3128', '119.131.67.188:8118', '218.75.144.25:9000', '113.91.66.81:8118', '27.46.49.40:9797', '58.251.235.77:9999', '27.54.197.36:8888', '60.221.249.115:8080', '180.157.242.80:8118', '49.209.80.36:80', '58.252.73.6:9090', '58.210.143.98:1080', '113.74.115.3:9797', '116.17.162.33:9797', '119.29.103.13:8888', '27.46.50.191:8118', '113.108.192.74:80', '110.182.99.169:9797', '123.5.57.136:9999', '110.182.236.182:9797', '14.105.94.136:8118', '202.118.8.13:3128', '113.109.18.178:9797']
    # iplist =['124.88.67.54:80', '124.88.67.54:80','202.197.127.139:1209', '119.137.32.190:8088', '183.63.14.107:808', '123.55.194.43:9999', '218.56.132.157:8080', '121.8.170.53:9797',
    #          '218.56.132.156:8080', '58.217.195.141:80', '124.88.67.30:80', '121.32.251.43:80', '123.139.56.234:9999', '220.164.18.225:8081', '58.52.201.119:8080', '58.213.19.233:10081',
    #          '112.90.18.121:80', '183.56.177.130:808', '120.132.71.212:80', '124.88.67.34:80', '218.56.132.155:8080', '49.209.80.36:80']

    filename=os.getcwd()+'\\checkiplist.json'
    f=open(filename,'r')
    iplist=json.load(f)
    f.close()
    return iplist

iplist=get_proxyip()



allurl=[]
for i in range(30):
    allurl.append('https://checkcoverage.apple.com/cn/zh/')

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=4)
    url='http://changge.anjuke.com/community/?from=esf_list_navigation'
    result = []
    start=time.time()
    # for i in xrange(40):
    #     # msg = "hello %d" %(i)
    #     # result.append(pool.apply_async(get, (url,iplist2,getd() )))
    #     pool.apply_async(get, (url,iplist2,getd() ))
    # pool.close()
    # pool.join()
    driver = getd()
    for i in range(100):
        print i,
        driver,status=proxy_get(url,iplist,driver)
        print driver,start

        if status!=False:
            print driver.page_source
            break

        # print driver.page_source

        # break
    end=time.time()



    print end-start
    # for res in result:
    #     print res.get()
    # print "Sub-process(es) done."