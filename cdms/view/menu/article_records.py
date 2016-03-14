#coding:u8
from . import menu
from ..wrapper import authorize
from flask import  flash, request, url_for, render_template, g, redirect, session
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@menu.route('/article_records', methods=['POST', 'GET'])
@authorize
def article_records_view():
    # 记录文章
    if request.method == 'GET':
        sql = 'SELECT users.username, post_info.post_title, post_info.post_address, post_info.post_date, post_info.id' \
              ' FROM users ' \
              'INNER JOIN post_info ON post_info.user_name_id = users.id where users.id = %d ' \
              'AND year(post_date)=year(now()) AND month(post_date)=month(now()) and day(post_date)=day(now())' \
              'ORDER BY id DESC LIMIT 10;' % int(session['user_name_id'])
        g.db.cursor.execute(sql)
        entries = []
        for row in g.db.cursor.fetchall():
            entries.append(dict(name=row[0], title=row[1], url=row[2], date=row[3],
                                key=hash(str(row[4])), id=row[4]))
        return render_template('article_records.html', entries=entries)

    # POST 数据处理
    url = request.form['url']
    # 获取域名

    sql = 'SELECT register_website FROM periphery_entend WHERE register_website = %s'
    if not request.form['url'] == '' or not request.form['title'] == '':
        sql = 'INSERT INTO  post_info (user_name_id, post_title, post_address, post_date) ' \
              'VALUES(%s, %s, %s,  now());'
        g.db.cursor.execute(sql, (session['user_name_id'], request.form['title'], request.form['url']))
        g.db.commit()
        flash(u'添加成功！')
    else:
        flash(u'标题或发帖地址为空!')

    return redirect(url_for('article_records_view'))
