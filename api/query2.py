#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created by bayonet on 16-3-3.

"""
传入参数urls（网址）,keys（关键词）数列
返回数列  eg:["dbdydk.com:\n杭州复旦儿童医院 22 杭州复旦儿童医院治疗多动症怎么样 30"]

"""

import requests
from lxml import etree


def get_HTML_code(key, page=False):
    """ 获取网站源代码 """
    if not page:
        return etree.HTML(requests.get('http://www.baidu.com/s?ie=utf-8&wd=' + key).content)
    return etree.HTML(requests.get('http://www.baidu.com' + key).content)


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
    """ url 比对。 判断是否有排名 """
    page = 0
    result = []
    for urls in baidu_urls:
        page += 1
        for url in urls:
            try:
                position = my_urls.index(url) + 1
                result.append(dict(page=page, position=position, url=my_urls[my_urls.index(url)], key=key))
            except ValueError:
                pass
    return result


def baidu_query_api(page=5):
    """
    查询百度关键字排名
    page ： 查询页数
    """
    baidu_urls = []
    key = 'B站'
    html = get_HTML_code(key)
    baidu_page_address = baidu_page(html, page)
    baidu_urls += [get_baidu_all_url(html)]
    for page_address in baidu_page_address:
        html = get_HTML_code(page_address, page=True)
        baidu_urls += [get_baidu_all_url(html)]
    # print urls
    print serach(baidu_urls, ['www.bilibili.tv', 'www.bilibili.com'], key)


if __name__ == '__main__':
    baidu_query_api()
