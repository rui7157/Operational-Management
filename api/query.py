#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created by bayonet on 16-3-3.

"""
传入参数urls（网址）,keys（关键词）数列
返回数列  eg:["dbdydk.com:\n杭州复旦儿童医院 22 杭州复旦儿童医院治疗多动症怎么样 30"]

"""




import requests, json, re, sys
import urllib2, socket
from lxml import etree
from multiprocessing import Queue, Process
socket.timeout(30)
from threading import Thread

reload(sys)
sys.setdefaultencoding('utf-8')


def get_HTML_code(key):
    """ 获取网站源代码 """
    return requests.get('http://www.baidu.com/s?wd=' + key + '&rn=50').content


def baidu_paiming(hosts, keys, result):
    """
        更据百度site查询 来获取所有关键字
        二次查询 对比 网站url 是否为查询要查询排名的url
    """
    keyfile=dict()
    for key in keys:
        a = 0
        c = 0

        html = etree.HTML(get_HTML_code(key))
        for x in html.xpath('//div[@class="f13"]'):
            for i in x.xpath('a[@class="c-showurl"]/text()'):
                # c排名第几位
                c += 1
                url = str(i).split('/')[0]
                for h in hosts:
                    if re.search('cn|com|org|net|info', url):
                        if re.search(url, h.replace('\n', '')):
                            # url:网络url  h:自己提供 url
                            if url != 'www.' and url != '.ca':
                                # a: 关键字和url匹配成功的次数
                                a += 1
                                if keyfile.has_key(url):
                                    # if key == '复旦儿童医院':
                                    # print keyfile[url]
                                    keyfile[url]=keyfile[url]+key+" "+str(c)+"\n"
                                else:
                                    keyfile[url]=key+" "+str(c)+"\n"
    if not isinstance(result,list):
        result.put(keyfile)
    else:
        for k,v in keyfile.items():
            result.append(k+":\n"+v)
        return result


def web_api(urls, keys):
    results = []
    if len(keys) > 16:
        #关键字小于16不使用多进程
        result = Queue()
        key_num = len(keys) / 4
        key_num_yu = len(keys) % 4
        # p1 = Process(target=baidu_paiming, args=(urls, keys[0 * key_num:1 * key_num], result))
        # p2 = Process(target=baidu_paiming, args=(urls, keys[1 * key_num:2 * key_num], result))
        # p3 = Process(target=baidu_paiming, args=(urls, keys[2 * key_num:3 * key_num], result))
        # p4 = Process(target=baidu_paiming, args=(urls, keys[3 * key_num:4 * key_num+key_num_yu], result))
        p1 =Thread(target=baidu_paiming, args=(urls, keys[0 * key_num:1 * key_num], result))
        p2 = Thread(target=baidu_paiming, args=(urls, keys[1 * key_num:2 * key_num], result))
        p3 = Thread(target=baidu_paiming, args=(urls, keys[2 * key_num:3 * key_num], result))
        p4 = Thread(target=baidu_paiming, args=(urls, keys[3 * key_num:4 * key_num+key_num_yu], result))



        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        re = list()
        result_dict=dict()

        while not result.empty():
            tmp = result.get()
            re.append(tmp)
        new_dict=dict()
        for r in range(4):
            for k,v in re[r].items():
                if new_dict.has_key(k):
                    new_dict[k]=new_dict[k]+v
                else:
                    new_dict[k]=v

        for url,result_end in new_dict.items():
            results.append(url+":\n"+result_end)
    else:
        results=baidu_paiming(keys=keys, hosts=urls, result=results)
    return results


if __name__ == '__main__':
    urls = open('host.txt', 'rU').readlines()
    keys = open("key.txt", "rU").readlines()
    web_api(urls=urls, keys=keys)
