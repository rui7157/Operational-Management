# -*- coding: utf-8 -*-
from . import other
from flask import render_template

try:
    import MySQLdb
except Exception:
    import pymysql as MySQLdb


# -----------------错误页面--------------
@other.app_errorhandler(403)
def internal_server_error(e):
    return render_template('error/403.html'), 403

@other.app_errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404

@other.app_errorhandler(405)
def request_method_not_allowed(e):
    return render_template('error/405.html'), 405


@other.app_errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500
@other.route("/test")
def drawSVG():
    import pygal
    line_chart = pygal.Line(legend_at_bottom=True,legend_box_size=18)
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None, 0, 16.6,  25,  31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,  66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
    svg = line_chart.render_response()
    return svg