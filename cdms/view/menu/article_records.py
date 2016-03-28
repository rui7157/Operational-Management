# -*- coding:utf-8 -*-
from . import menu
from ..wrapper import authorize
from flask import flash, request, url_for, render_template, g, redirect, session
import xlrd
import os
from werkzeug.utils import secure_filename


@menu.route('/article_records', methods=['POST', 'GET'])
@authorize
def article_records():
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
    else:
        flash(u'标题或发帖地址为空!')

    return redirect(url_for('menu.article_records'))


@menu.route('/article_records_file', methods=['POST'])
@authorize
def article_records_file():

    def write_sql(str_data):
        success=0
        fail_data = ""
        for index,i in enumerate(str_data):

            try:
                title = i[0].replace("?", "")
                url = i[1]
                success+=1
            except IndexError:
                fail_data = fail_data+str(index+1)+":"+"".join(i)+" | "
                continue
            g.db.cursor.execute('INSERT INTO  post_info (user_name_id, post_title, post_address, post_date) ' \
                            'VALUES(%s, "%s", "%s",  now());' % (session['user_name_id'], title, url))
            g.db.commit()
        return fail_data,success

    f = request.files["filename"]
    filename = secure_filename(f.filename)
    fileformat = filename.split(".")[-1:][0]
    if fileformat == "txt":
        str_data = f.readlines()
        str_data = [i.decode('gbk').split() for i in str_data]
        fail_data,success=write_sql(str_data)
    elif fileformat in ["xls", "xlsx", "XLS", "XLSX"]:
        filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)),"..","..","static","upload",filename)
        f.save(filepath)
        f=xlrd.open_workbook(filepath)
        os.remove(filepath)
        sheet_data=f.sheet_by_index(0)
        row_count = sheet_data.nrows
        excel_data = []
        for row_num in xrange(row_count):
            excel_data.append([sheet_data.cell(row_num, 0).value, sheet_data.cell(row_num, 1).value])
        fail_data,success=write_sql(excel_data)
    else:
        flash("不支持您所上传的文件类型！")
    if fail_data:
        flash("成功{success}条，失败的条目：{fail}".format(success=success,fail=str(fail_data)))
    else:
        flash("成功上传所有条目{}条！".format(success))
    return redirect(url_for("menu.article_records"))  #
