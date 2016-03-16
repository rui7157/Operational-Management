#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created by bayonet on 16-3-16.
from . import tool
from flask import render_template, session

try:
    import MySQLdb
except Exception:
    import pymysql as MySQLdb


@tool.route("/tool/error_query", methods=["GET"])
def error_query():
    conn = MySQLdb.connect(host='192.168.2.222', user='root', db='edit', charset='utf8')
    cursor = conn.cursor()
    error_query_sql = 'select * from webinfo WHERE name=\'%s\' AND YEAR(date)=YEAR(now()) AND MONTH(date)=MONTH(now()) AND DAY(date)=DAY(now());'
    error_info_list = []

    if cursor.execute(error_query_sql % (session.get('username'),)):
        for error_info in cursor.fetchall():
            error_info_list.append(dict(url=error_info[1], date=error_info[4]))
    conn.close()
    return render_template('tool/error_query.html', error_info_list=error_info_list)
