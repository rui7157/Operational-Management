# -*- coding: utf-8 -*-
from . import tool
from flask import request, url_for, redirect, render_template, make_response, session, flash
import xlwt
import StringIO


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
        if result:
            response_data = ""
            for dict_data in result:
                response_data = response_data + u"<tr><td>{key}</td><td>{url}</td><td>百度排名第{page}页第<span class='label label-danger'>{position}</span>个".format(
                        url=dict_data["url"], position=str(dict_data["position"]), page=str(dict_data["page"]),
                        key=dict_data["key"])
            return response_data
        else:
            return "null"


@tool.route("/tool/query/download_excel",methods=["POST"])
def download_excel():
    if request.method=="POST":
        web_table_data=request.form.values()
        urls,keys,result=[],[],[]
        for table_tr in web_table_data:
            key,url,res=table_tr.split("&")
            urls.append(url)
            keys.append(key)
            result.append(res)
        str_data = generate_xls(urls, keys, result)
        response = make_response(str_data)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers['Transfer-Encoding'] = 'chunked'
        response.headers['Content-Disposition'] = 'attachment; filename=bauduquery.xls'
        flash("返回下载情况")
        return response
    else:
        flash("没有数据")
        return redirect(url_for("tool.query_request"))


def generate_xls(urls, keys, result):
    xls_file = xlwt.Workbook()
    sheet = xls_file.add_sheet(u"百度排名", cell_overwrite_ok=True)
    font0 = xlwt.Font()
    font0.name = 'Times New Roman'
    font0.colour_index = 2
    font0.bold = True
    style0 = xlwt.XFStyle()
    style0.font = font0
    row = 0
    sheet.col(0).width = 256 * 20
    sheet.col(1).width = 256 * 30
    sheet.col(2).width = 256 * 20

    sheet.write(0, 0, u"网址", style0)
    sheet.write(0, 1, u"关键词", style0)
    sheet.write(0, 2, u"排名", style0)
    if urls != None and keys != None and result != None:
        for url, key, res in zip(urls, keys, result):
            row += 1
            sheet.write(row, 0, url.decode("utf-8"))
            sheet.write(row, 1, key.decode("utf-8"))
            sheet.write(row, 2, res.decode("utf-8"))
    ios = StringIO.StringIO()
    xls_file.save(ios)
    ios.seek(0)
    return ios.getvalue()
