# -*- coding: utf-8 -*-

import functools
import thread
from flask import flash, url_for, g, redirect, session
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

try:
    import MySQLdb
except Exception:
    import pymysql as MySQLdb

lock = thread.allocate_lock()


def authorize(fn):
    """ 验证登录 """

    @functools.wraps(fn)
    def wrapper(*args, **kwds):
        if 'username' in session.keys():
            # 验证cookie 是否存在 存在函数退出
            return fn()
        flash(u'请先登录!')
        return redirect(url_for('menu.login'))

    return wrapper


def post_count_data(exa_user, group):
    """ 获取当前组成员 文章数 """

    def user_info(row):
        sql = 'SELECT post_info.post_address, post_info.post_title, post_info.post_date, ' \
              'users.username FROM post_info INNER JOIN users ON post_info.user_name_id = users.id ' \
              'WHERE users.id = %s ' \
              'AND year(post_date)=year(now()) AND month(post_date)=month(now()) and day(post_date)=day(now())'
        return g.db.cursor.execute(sql, (row[0],))

    if exa_user == 2:
        sql_group = 'SELECT id, username FROM users'
    else:
        sql_group = 'SELECT id, username FROM users  WHERE users.group = %s'
    entries = []

    if session['exa_user'] == 2:
        # exa_user --> 2 为超管权限。 获取所有人 文章数
        g.db.cursor.execute(sql_group)
    else:
        g.db.cursor.execute(sql_group, (group,))
    for row in g.db.cursor.fetchall():
        # 获取用户当天帖子数
        count = user_info(row)
        entries.append(dict(id=row[0], username=row[1], count=count))
    return entries


def generate_sql(data,method,*sid):
    keys,values="",""
    if method=="add":
        for k,v in data.items():
            if v:
                if keys:
                    keys+=",`"+k+"`"
                else:
                    keys+="`"+k+"`"
                if values:
                    if k in ["price"]:
                        values+=","+v
                    else:
                        values+=",'"+v+"'"
                else:
                        values+="'"+v+"'"
        return "INSERT INTO server ({keys}) VALUE ({values});".format(keys=keys,values=values)

    elif method=="modify":
        # data.pop("sid")
        temp = filter(lambda v:True if not(v[1] in ["无",""] or  v[0] in ["sid"]) else False,[(k,v) for k,v in data.items()])
        print temp
        set_data=",".join(["`"+k+"`"+"="+v  if k in ["price"] else "`"+k+"`"+"="+"'"+v+"'" for k,v in temp])
        return "UPDATE server SET {set_data} WHERE id={sid};".format(set_data=set_data,sid=sid[0])
    else:
        raise ValueError,method