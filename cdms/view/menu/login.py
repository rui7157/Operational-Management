# -*- coding:utf-8 -*-
from . import menu
from flask import flash, request, url_for, render_template, g, redirect, session


@menu.route('/login', methods=['POST', 'GET'])
def login():
    # 登陆
    if request.method == 'GET':
        return render_template('login.html')

    if 'username' in session.keys():
        # 退出删除 session
        session.pop('quarters_periphery_entend')
        session.pop('user_name_id')
        session.pop('group')
        session.pop('exa_user')
        session.pop('username')
        return redirect(url_for('menu.login'))

    if g.db.cursor.execute("SELECT password,id FROM users WHERE username=%s", ((request.form['username']),)):
        # 查询数据库 用户名 返回1 判断密码
        if request.form['password'] == g.db.cursor.fetchall()[0][0]:
            # 创建用户cookie
            session['username'] = request.form['username']
            # 设置用户权限
            sql = "SELECT users.username, users.password, quarters.quarter, " \
                  "quarters.quarters_periphery_entend, users.id, users.group, users.exa_user " \
                  "FROM users INNER JOIN quarters ON users.user_quarter_id = quarters.id " \
                  "WHERE users.username=%s;"
            g.db.cursor.execute(sql, (request.form['username'],))
            sql_data = g.db.cursor.fetchall()
            session['quarters_periphery_entend'] = sql_data[0][3]
            session['user_name_id'] = sql_data[0][4]
            session['group'] = sql_data[0][5]
            session['exa_user'] = sql_data[0][6]
            return redirect(url_for('menu.index'))
    flash(u'你输入的帐号或密码不正确!')
    return render_template('login.html')


@menu.route("/logout")
def logout():
    if 'username' in session.keys():
        # 退出删除 session
        session.pop('quarters_periphery_entend')
        session.pop('user_name_id')
        session.pop('group')
        session.pop('exa_user')
        session.pop('username')
        return redirect(url_for('menu.login'))
