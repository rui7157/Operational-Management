# coding: utf-8
from . import tool
from flask import request, url_for, redirect,render_template
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


@tool.route("/tools")
def tools():
    return render_template("tools.html")