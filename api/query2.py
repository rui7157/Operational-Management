#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created by bayonet on 16-3-3.

"""
传入参数urls（网址）,keys（关键词）数列
返回数列  eg:["dbdydk.com:\n杭州复旦儿童医院 22 杭州复旦儿童医院治疗多动症怎么样 30"]

"""

import urllib2
from lxml import etree


def get_HTML_code(key, page=False):
    """  获取网站源代码
    key : 用户查询关键字
    page : 为 True 时 拼接 url 地址 """
    if not page:
        url = 'http://www.baidu.com/s?ie=utf-8&wd=' + key
    else:
        url = 'http://www.baidu.com' + key
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'}
    req = urllib2.Request(url=url, headers=headers)
    html = urllib2.urlopen(req).read()
    return etree.HTML(html)


def baidu_page(html, page):
    """ 查询百度前10页地址 """
    return html.xpath('//div[@id="page"]/a/@href')[:page - 1:]


def get_baidu_all_url(html):
    """ 获取百度非推广位url """
    urls = []
    for div in html.xpath('//div[@class="f13"]'):
        urls.append(div.xpath('a/text()')[0].split('/')[0])
    return urls


def serach(baidu_urls, my_urls, key):
    """ url 比对。 判断是否有排名
        baidu_urls : 百度查询结果非推广位全部Url
        my_urls : 用户需要对比的url
        key : 用户查询的关键字
    """
    page = 0
    result = []
    for urls in baidu_urls:
        page += 1
        position = 0
        for url in urls:
            position += 1
            if url in my_urls:
                result.append(dict(page=page, position=position, url=url, key=key))
    return result


def baidu_query_api(urls, key, page=5):
    """
    查询百度关键字排名
    page ： 查询页数
    """

    baidu_urls = []
    html  = get_HTML_code(key)
    baidu_page_address = baidu_page(html, page)
    baidu_urls += [get_baidu_all_url(html)]
    for page_address in baidu_page_address:
        html = get_HTML_code(page_address, page=True)
        baidu_urls += [get_baidu_all_url(html)]
    return serach(baidu_urls, urls, key)
