# coding: utf-8
from . import menu
from ..wrapper import authorize
from flask import flash, request, url_for, render_template, g, redirect

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


@menu.route('/mail', methods=['GET', 'POST'])
@authorize
def mail_view():
    # 邮件管理
    if request.method == 'GET':
        sql = 'SELECT * FROM register_mail'
        entries = []
        if g.db.cursor.execute(sql):
            for row in g.db.cursor.fetchall():
                entries.append(dict(username=row[1], password=row[2], date=row[3], key=hash(str(row[0])), id=row[0]))
        return render_template('mail.html', entries=entries)

    if not request.form['username'] == '' and not request.form['password'] == '':
        sql = 'SELECT * FROM register_mail WHERE mail_username=\'' + request.form['username'] + '\''
        entries = []
        if g.db.cursor.execute(sql):
            for row in g.db.cursor.fetchall():
                entries.append(dict(username=row[1], password=row[2]))
            flash(u'该邮箱添加! 帐号:' + entries[0].get('username') + u',密码:' + entries[0].get('password'))
            return redirect(url_for("mail_view"))

        sql = 'INSERT INTO register_mail (mail_username, mail_password, mail_date) VALUES (%s, %s, now())'
        if g.db.cursor.execute(sql, (request.form['username'], request.form['password'])):
            flash(u'添加成功！')
            g.db.commit()
            return redirect(url_for("mail_view"))

    flash(u'请输入邮箱帐号或密码!')
    return redirect(url_for("menu.mail_view"))


@menu.route('/mail_delete', methods=['GET'])
def mail_delete_view():
    # 简单验证, 验证通过更据 id 直接删除
    if str(hash(str(request.args.get('id')))) == str(request.args.get('key')):
        sql = 'delete from register_mail  where id=%s;' % int(request.args.get('id'))
        if g.db.cursor.execute(sql):
            flash(u'删除成功!')
            g.db.commit()
            return redirect(url_for('menu.register_web_info_view'))
    g.db.commit()
    flash(u'删除失败！请刷新页面再试！')
    return redirect(url_for('menu.register_web_info_view'))
