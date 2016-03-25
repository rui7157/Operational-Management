# -*- coding: utf-8

from . import adm
from cdms.view.wrapper import authorize
from flask import flash, request, url_for, render_template, g, redirect, session,abort
import pygal

@adm.route("/")
@authorize
def admin():

    """
    line_chart = pygal.Bar()
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
    line_chart.render()
    """
    # print session
    # group_leader={"杨磊":1,"涂丹":2,"谭俊":3,"张行":4,"杨帆":5}
    # if session.get("username") in group_leader.keys():
    #     sql="""SELECT username FROM users WHERE `group`={group};"""
    #     g.db.cursor.execute(sql.format(group_leader.get(session.get("username"))))
    #     print g.db.fetchall()[0]
    # line_chart=pygal.Bar()
    # line_chart=u"发帖统计"
    # line_chart.x_labels=map(str,range(10))
    return render_template("admin/admin.html")
