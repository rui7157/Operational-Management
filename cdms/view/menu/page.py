# -*- coding: utf-8

from . import menu
from . import authorize
from flask import request, render_template, g, session

try:
    import MySQLdb
except Exception:
    import pymysql as MySQLdb


@menu.route('/page')
@authorize
def page():
    """
    第一次取出一共有多少mysql数据
    更据Mysql取出来的数据 来分页
    """
    user_post_id = request.args.get("user_post_id", None)
    current = int(request.args.get('page', 1))
    date_y, date_m, date_d = request.args.get("y", None), request.args.get("m", None), request.args.get("d", None)

    # -- 第一次查询 取所有数据  --
    sql = 'SELECT users.username, post_info.post_title, post_info.post_address, post_info.post_date, post_info.id' \
          ' FROM users ' \
          'INNER JOIN post_info ON post_info.user_name_id = users.id ' \
          'WHERE users.id = %s'
    if date_y and date_m and date_d:
        id = int(user_post_id)
        sql = """
                  SELECT users.username, post_info.post_title, post_info.post_address, post_info.post_date, post_info.id
                  FROM users INNER JOIN post_info ON post_info.user_name_id = users.id WHERE users.id = {0}
                  AND YEAR(post_date)={1} AND MONTH(post_date)={2} AND DAY(post_date)={3}; """
        sql = sql.format(id, int(date_y), int(date_m), int(date_d))
    elif user_post_id:
        id = int(user_post_id)
        sql = sql % (id)
    else:
        id = int(session['user_name_id'])
        sql = sql % (id)
    n = g.db.cursor.execute(sql)
    number = n / 10
    if n % 10 > 0:
        number += 1
    # -- 分页查询  --
    if date_y and date_m and date_d:
        sql = 'SELECT users.username, post_info.post_title, post_info.post_address, post_info.post_date, post_info.id, post_info.examination' \
              ' FROM users ' \
              'INNER JOIN post_info ON post_info.user_name_id = users.id ' \
              'WHERE users.id = {id} AND YEAR(post_date)={y} AND MONTH(post_date)={m} AND DAY(post_date)={d} ORDER BY id DESC LIMIT %d,%d;'
        sql = sql.format(id=id, y=int(date_y), m=int(date_m), d=int(date_d))

    else:
        sql = 'SELECT users.username, post_info.post_title, post_info.post_address, post_info.post_date, post_info.id, post_info.examination ' \
              ' FROM users ' \
              'INNER JOIN post_info ON post_info.user_name_id = users.id ' \
              'WHERE users.id = {id} ORDER BY id DESC LIMIT %d,%d ;'
        sql = sql.format(id=id)
    if number == 1:
        g.db.cursor.execute(sql % (0, 10))
    else:
        try:
            # 分页 2 * 10 - 10 取出数据
            g.db.cursor.execute(sql % (current * 10 - 10, 10))
        except MySQLdb.MySQLError:
            pass
    try:
        number = range(1, number + 1)
        max_list = number[len(number) - 1]
    except IndexError:
        number = []
        max_list = 1

    entries = []
    for row in g.db.cursor.fetchall():
        entries.append(dict(name=row[0], title=row[1], url=row[2], date=row[3], id=row[4], is_exa_post=row[5]))

    is_exa_user = 0  # 是否审核用户
    if session.get("user_name_id"):
        current_user_id = session.get('user_name_id')
        sql = """SELECT exa_user FROM users WHERE id={};"""
        if g.db.cursor.execute(sql.format(current_user_id)):
            is_exa_user = g.db.cursor.fetchall()[0][0]

    return render_template('page.html', entries=entries, upper_page=current - 1,
                           next_page=current + 1, current_page=current, number=number, max_list=max_list,
                           is_exa_user=is_exa_user, date_y=date_y, date_m=date_m, date_d=date_d,
                           user_post_id=user_post_id)
