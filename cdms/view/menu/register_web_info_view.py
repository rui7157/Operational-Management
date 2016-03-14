# coding: utf-8
from . import menu
from ..wrapper import authorize
from flask import flash, request, url_for, render_template, g, redirect, session
from threading import Lock

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
lock = Lock()


@menu.route('/register_web_info', methods=['POST', 'GET'])
@authorize
def register_web_info_view():
    # 注册网站信息
    if request.method == 'GET':
        sql = """ SELECT users.username, users.password, periphery_entend.register_website,
                 periphery_entend.register_website_username, periphery_entend.register_website_password,
                 register_mail.mail_username, register_mail.mail_password, periphery_entend_data.data_date,
                 periphery_entend_data.id, periphery_entend_data.periphery_entend_id
                 FROM periphery_entend_data
                 INNER JOIN users ON periphery_entend_data.user_id = users.id
                 INNER JOIN periphery_entend ON periphery_entend_data.periphery_entend_id = periphery_entend.id
                 INNER JOIN register_mail ON periphery_entend_data.register_mail_id = register_mail.id
                 WHERE users.id = %s;"""
        entries = []
        if g.db.cursor.execute(sql, (session['user_name_id'],)):
            for row in g.db.cursor.fetchall():
                entries.append(dict(username=row[0], password=row[1], register_website=row[2],
                                    register_website_username=row[3], register_website_password=row[4],
                                    mail_username=row[5], mail_password=row[6], data_date=row[7], id=row[8],
                                    key=hash(str(row[8])), periphery_entend_id=row[9]
                                    ))

        return render_template('register_web_info.html', entries=entries)

    web_site = request.form['web_site']
    username = request.form['username']
    password = request.form['password']
    mail = request.form['mail']
    # 查询邮箱是否 存在 存在则取id

    sql = 'SELECT id FROM register_mail WHERE mail_username = %s'

    if not g.db.cursor.execute(sql, (mail,)):
        flash(u'该邮箱不存在，请先添加该邮箱!')
        return redirect(url_for("register_web_info_view"))
    register_mail_id = g.db.cursor.fetchall()[0][0]
    sql = 'INSERT INTO periphery_entend(register_website, register_website_username, register_website_password)' \
          'VALUES (%s, %s, %s)'

    # 处理并发数据出错问题
    lock.acquire()
    if g.db.cursor.execute(sql, (web_site, username, password)):
        sql = 'SELECT max(id) FROM periphery_entend'
        if g.db.cursor.execute(sql):
            register_web_id = g.db.cursor.fetchall()[0][0]
            sql = 'INSERT INTO periphery_entend_data (user_id, periphery_entend_id, register_mail_id, data_date) ' \
                  'VALUES (%d, %d, %d, now())' % (session['user_name_id'], register_web_id, register_mail_id)
            if g.db.cursor.execute(sql):
                flash(u'添加成功！')
                g.db.commit()
    lock.release()

    return redirect(url_for("menu.register_web_info_view"))


@menu.route('/register_web_info_delete')
def register_web_info_delete_view():
    # 简单验证, 验证通过更据 id 直接删除
    if str(hash(str(request.args.get('id')))) == str(request.args.get('key')):
        sql = 'delete from periphery_entend_data where id=%s;' % int(request.args.get('id'))
        if g.db.cursor.execute(sql):
            sql = 'delete from periphery_entend where id=%s;' % int(request.args.get('periphery_entend_id'))
            if g.db.cursor.execute(sql):
                flash(u'删除成功!')
                g.db.commit()
                return redirect(url_for('menu.register_web_info_view'))
    g.db.commit()
    flash(u'删除失败！请刷新页面再试！')
    return redirect(url_for('menu.register_web_info_view'))


@menu.route("/register_web_info_set", methods=["POST"])
@authorize
def register_web_info_set():
    periphery_entend_id = request.form["periphery_entend_id"]
    # periphery_entend网址ID
    sql = """UPDATE periphery_entend SET periphery_entend.register_website ='{}',
                 periphery_entend.register_website_username='{}', periphery_entend.register_website_password='{}' WHERE  periphery_entend.id ={};"""
    if g.db.cursor.execute(sql.format(request.form["register_website"], request.form["register_website_username"],
                                      request.form["register_website_password"], int(periphery_entend_id))):
        g.db.commit()
        set_post_result = 1
    else:
        set_post_result = 0
    return redirect(url_for('menu.register_web_info_view', set_post_result=set_post_result))
