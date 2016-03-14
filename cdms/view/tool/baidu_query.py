# coding: utf-8
from . import tool
from flask import request, url_for, redirect,render_template
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


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
