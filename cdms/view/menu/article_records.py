# -*- coding:utf-8 -*-
from . import menu
from ..wrapper import authorize
from flask import flash, request, url_for, render_template, g, redirect, session
# import xlrd
# import os
# from werkzeug.utils import secure_filename
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

    # def get_data(filepath):
    #     """获取excel数据源"""         # 改成自己的路径
    #     is_valid = False            # 验证文件
    #     try:
    #         filepath = [file, filepath][filepath != '']
    #         print filepath
    #         # 判断给出的路径是不是xls格式
    #         if os.path.isfile(filepath):
    #             filename = os.path.basename(filepath)
    #             if filename.split('.')[1] == 'xls':
    #                 is_valid = True
    #         data = None
    #         if is_valid:
    #             data = xlrd.open_workbook(filepath)
    #     except Exception, e:
    #         flash("上传遇到错误！")
    #         return None
    #     return data
    def check_data(url,*title):
        if url.isalpha():
            return False
        return True

    f = request.files["filename"]
    str_data = f.readlines()
    str_data = [i.decode('gbk')[1::].split() for i in str_data]
    fail_data=[]
    for i in str_data:
        try:
            title = i[0]
            url = i[1]
        except IndexError:
            break
        if check_data(url):
            g.db.cursor.execute('INSERT INTO  post_info (user_name_id, post_title, post_address, post_date) ' \
          'VALUES(%s, "%s", "%s",  now());' %(session['user_name_id'], title, url))
        else:
            fail_data.append(i[0]+":"+i[1]+"\n")
    g.db.commit()
    if fail_data:
        flash("插入失败：{}".format("".join(fail_data)))
    return redirect(url_for("menu.article_records"))  #



    #     dict_data[i.split("\t")[0]] = i.split()[1]
    # print dict_data
    # data = xlrd.xldate(f)
    # print data
    # fname = secure_filename(f.filename)
    # # fpath = os.path.join(url_for("static",filename = "temp"),fname)
    # fpath = url_for("static",filename = "temp")+"/"+fname
    # print fpath
    # f.save(fpath)
    # data = get_data(fpath)
    # if data:
    #     table = data.sheet_by_index(0)
    #     nrows = table.nrows        #获取行数
    #     for i in range(0,nrows):
    #         print table.cell(i,0).value  #第一列
    #         print table.cell(i,1).value #第二列

        # table.cell(i,col_index[0]).value


