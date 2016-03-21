# -*- coding: utf-8 -*-
from . import tool
from flask import request, url_for, redirect, render_template, make_response, jsonify


@tool.route("/tool/query", methods=["GET"])
def query():
    return render_template("tool/query.html")


@tool.route("/tool/query_request", methods=["POST"])
def query_request():
    def user_input_format(text):
        """ 用户输入格式化处理"""
        text = text.split("\n")  # 分割字符串
        text = list(set(text))  # 去重复
        text = [i for i in text if i != "" and i != None]  # 去除空值
        return text

    if request.method == "POST":
        web_results = []
        from api.query import web_api
        # 获取用户输入，并做去空行处理
        urls = request.form['url']
        keys = request.form['key']
        urls = user_input_format(urls)
        keys = user_input_format(keys)
        result = web_api(urls=urls, keys=keys)
        return "".join(result)
    return redirect(url_for("tool.query"))


@tool.route("/tool/query_request2", methods=["POST"])
def query_request2():
    from concurrent.futures import ThreadPoolExecutor, Executor
    if request.method == "POST":
        from api.query2 import baidu_query_api
        urls = request.form['url']
        urls = urls.split("\n")
        key = request.form['key']
        executor = ThreadPoolExecutor(5)
        result = executor.submit(baidu_query_api, urls=urls, key=key)
        result = result.result()
        print result
        if result:
            response_data = ""
            for dict_data in result:
                response_data = response_data + u"<tr><td>{key}</td><td>{url}</td><td>百度排名第{page}页第<span class='label label-danger'>{position}</span>个".format(
                    url=dict_data["url"], position=str(dict_data["position"]), page=str(dict_data["page"]),
                    key=dict_data["key"])
            return response_data
        else:
            return "null"


@tool.route("/tool/query/download_excel")
def download_excel():
    str_data = "test"
    response = make_response(str_data)
    response.headers['Content-Type'] = 'application/vnd.ms-excel'
    response.headers['Content-Disposition'] = 'attachment; filename=data.xls'
    return response
