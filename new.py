#coding:utf-8
import requests
import re
import urllib2
import pymysql.cursors
import math

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
#连接配置信息
config = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'root',
          'password':'',
          'db':'hospital',
          'charset':'utf8'
          }
# 创建连接
connection = pymysql.connect(**config)
 

requests=requests.session()
cookies={
    "JSESSIONID":"3ACB4FD7162CE25CE7C9C9AD15FD72A0",
    "systemId":"4",
    "userLoginId":"admin"
}

# webcontent=requests.get("http://183.62.113.2/customerWork/queryCustomerWork",cookies=cookies).content
for page in range(1,6):
    print 'main page %d ' %page
    mainPostData=dict(
    beginDateTime="",
    customerName="",
    endDateTime="",
    flag=2,
    hiddenBeginDateTime="",
    hiddenCustomerName="",
    hiddenEndDateTime="",
    pageNo=page,
    pageSize=200,
    role=1)
    try:
        webcontent=requests.get("http://183.62.113.2/customerWork/queryCustomerWork",cookies=cookies).content
        webcontent=requests.post("http://183.62.113.2/customerWork/queryCustomerWork",cookies=cookies,data=mainPostData).content
        
        # print webcontent
        data=re.findall(r"""<a onclick\="viewPage\('(\d{4}-\d{2}-\d{2})','(.*?)','(\d*?)','1'\)">""",webcontent)
        for udate,uname,number in data:
            registerCount=requests.get("http://183.62.113.2/customerWork/viewRegisterCountPage?operationDate={}&customerName={}&customerId={}&status=1".format(udate,urllib2.unquote(urllib2.unquote(uname)),number),cookies=cookies).content        
            registerCount=requests.post("http://183.62.113.2/customerWork/viewRegisterCountPage",data=dict(customerName=uname,operationDate=udate,pageNo=1,pageSize=200,status=1)).content
            pageNumber=int(re.findall(r'<i class="red">(\d+?)</i>',registerCount)[0])
            print u"一共%d条数据" %pageNumber
            pageNumber=int(math.ceil(pageNumber/200.0))
            #http://183.62.113.2/customerWork/viewRegisterCountPage
            print u"翻页数量register : %s " %pageNumber
            # print udate.decode("utf-8","ignore"),uname.decode("utf-8","ignore"),number.decode("utf-8","ignore")
            for p in range(1,pageNumber+1):
                print u"正在爬取：register  %d" %p
                pageArgs=dict(
                customerName=uname,
                operationDate=udate,
                pageNo=p,
                pageSize=200,
                status=1)

                registerCount =requests.post("http://183.62.113.2/customerWork/viewRegisterCountPage",data=pageArgs).content
                presonInfo=re.findall(r"""<tr>[\s\S]*?<td>(.*?)</td>[\s\S]*?<td>[\s\S]*?([男|女])[\s\S]*?</td>[\s\S]*?<td>(.*?)</td>[\s\S]*?<td>身份证</td>[\s\S]*?<td>(.*?)</td>[\s\S]*?<td>(\d{4}-\d{2}-\d{2})</td>[\s\S]*?<td></td>[\s\S]*?<td>(.*?)</td>[\s\S]*?</tr>""",registerCount)
                for info in presonInfo:
                    name,sex,phone,idcard,date,times=info
                    # print name.decode("utf-8","ignore"),sex.decode("utf-8","ignore").replace(" ",""),phone.decode("utf-8","ignore"),idcard.decode("utf-8","ignore"),date.decode("utf-8","ignore"),times.decode("utf-8","ignore")
                    # 执行sql语句

                    with connection.cursor() as cursor:
                        # 执行sql语句，插入记录
                        sql = 'INSERT INTO `registerperson_best` (`name`,`sex`,`phone`,`idcard`,`date`,`times`) VALUES (%s, %s, %s, %s, %s ,%s)'
                        cursor.execute(sql, (name.decode("utf-8","ignore"),sex.decode("utf-8","ignore").replace(" ",""),phone.decode("utf-8","ignore"),idcard.decode("utf-8","ignore"),date.decode("utf-8","ignore"),times.decode("utf-8","ignore")))
                    # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                    connection.commit()




            guahaoCount=requests.get("http://183.62.113.2/customerWork/viewRegisterationCountPage?operationDate={}&customerName={}&customerId={}&status=2".format(udate,urllib2.unquote(urllib2.unquote(uname)),number),cookies=cookies).content
            guahaoCount =requests.post("http://183.62.113.2/customerWork/viewRegisterationCountPage",data=dict(customerName=uname,operationDate=udate,pageNo=1,pageSize=200,status=2)).content 
            # print guahaoCount

            pageNumber2=int(re.findall(r'<i class="red">(\d+?)</i>',guahaoCount)[0])
            print u"一共%d条数据" %pageNumber2

            pageNumber2=int(math.ceil(pageNumber2/200.0))
            print u" 翻页数量: %s " %pageNumber2
            # print udate.decode("utf-8","ignore"),uname.decode("utf-8","ignore"),number.decode("utf-8","ignore")
            for p2 in range(1,pageNumber2+1):
                print u"正在爬取第 %d 页" %p2
                postArgs=dict(
                customerName=uname,
                operationDate=udate,
                pageNo=p2,
                pageSize=200,
                status=2)

                guahaoCount =requests.post("http://183.62.113.2/customerWork/viewRegisterationCountPage",data=postArgs).content       
                guahaoInfo=re.findall(r"""</td>[\s\S]*?<td>[\s\S]*?</td>[\s\S]*?<td>[\s\S]*?</td>[\s\S]*?<td>([\s\S]*?)</td>[\s\S]*?<td>([\s\S]*?)</td>[\s\S]*?<td>([\s\S]*?)</td>[\s\S]*?<td>([\s\S]*?)</td>[\s\S]*?<td>[\s\S]*?([男|女])[\s\S]*?</td>[\s\S]*?<td>(\d*?)</td>[\s\S]*?<td>身份证</td>[\s\S]*?<td>([\s\S]*?)</td>[\s\S]*?<td>([\s\S]*?)</td>[\s\S]*?<td></td>[\s\S]*?<td>[\s\S]*?<p>([\s\S]*?)</p>[\s\S]*?<p>([\s\S]*?)</p>[\s\S]*?</td>[\s\S]*?<td>([\s\S]*?)</td>[\s\S]*?<td>([\s\S]*?)</td>[\s\S]*?</tr>""",guahaoCount)
                for info in guahaoInfo:
                    doctor,doctype,doc,name,sex,phone,idcard,sdate,jzdate,jztime,status,yydatetime=info
                    # print doctor.decode("utf-8","ignore"),doctype.decode("utf-8","ignore"),doc.decode("utf-8","ignore"),name.decode("utf-8","ignore"),sex.decode("utf-8","ignore").replace(" ",""),phone.decode("utf-8","ignore"),idcard.decode("utf-8","ignore"),sdate.decode("utf-8","ignore"),jzdate.decode("utf-8","ignore"),jztime.decode("utf-8","ignore"),status.decode("utf-8","ignore"),yydatetime.decode("utf-8","ignore")

                    with connection.cursor() as cursor:
                        # 执行sql语句，插入记录
                        sql = 'INSERT INTO `guahaoinfo_best` (`doctor`,`doctype`,`doc`,`name`,`sex`,`phone`,`idcard`,`sdate`,`jzdate`,`jztime`,`status`,`yydatetime`) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s)'
                        cursor.execute(sql, (doctor.decode("utf-8","ignore"),doctype.decode("utf-8","ignore"),doc.decode("utf-8","ignore"),name.decode("utf-8","ignore"),sex.decode("utf-8","ignore").replace(" ",""),phone.decode("utf-8","ignore"),idcard.decode("utf-8","ignore"),sdate.decode("utf-8","ignore"),jzdate.decode("utf-8","ignore"),jztime.decode("utf-8","ignore"),status.decode("utf-8","ignore"),yydatetime.decode("utf-8","ignore")))
                    # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                    connection.commit()
    except Exception:
        print u"连接异常"

