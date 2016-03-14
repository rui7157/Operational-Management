# coding: utf-8
from . import other
from flask import render_template

try:
    import MySQLdb
except Exception:
    import pymysql as MySQLdb


# -----------------错误页面--------------
@other.app_errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@other.app_errorhandler(405)
def request_method_not_allowed(e):
    return render_template('error/405.html'), 405


@other.app_errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500
