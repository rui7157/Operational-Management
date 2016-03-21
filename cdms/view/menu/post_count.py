# -*- coding: utf-8 -*-
from . import menu,authorize
from flask import request, render_template, g, redirect,url_for,session,flash

from ..wrapper import post_count_data

@menu.route('/post_count', methods=['POST', 'GET'])
def post_count():
    if request.method == 'GET':
        entries = post_count_data(session['exa_user'], session['group'])
    return render_template('post_count.html', entries=entries)


@menu.route("/post_count_select", methods=["POST"])
def post_count_select():
    # 日期选择器实时查询
    if request.method == "POST":
        user_id = int(request.form["user_id"])
        date_y = request.form["date_y"]
        date_m = request.form["date_m"]
        date_d = request.form["date_d"]
        sql = 'SELECT users.username, post_info.post_title, post_info.post_address, post_info.post_date, post_info.id, post_info.examination' \
              ' FROM users ' \
              'INNER JOIN post_info ON post_info.user_name_id = users.id ' \
              'WHERE users.id = {id} AND YEAR(post_date)={y} AND MONTH(post_date)={m} AND DAY(post_date)={d};'
        sql = sql.format(id=user_id, y=int(date_y), m=int(date_m), d=int(date_d))
        count = g.db.cursor.execute(sql)
        return str(count)
    return redirect(url_for("menu.index_view"))


@menu.route("/post_count/post_manager")
def post_manager():
    return render_template("post_manager.html")



@menu.route("/exa_post", methods=["POST", "GET"])
def exa_post():
    # 帖子审核视图
    if request.method == "POST":
        post_id = request.form["post_id"]
        is_exa = request.form["is_exa"]
        try:
            if is_exa == "ok":
                sql = """
         UPDATE post_info SET examination = 1 WHERE id = {}"""
            elif is_exa == "fail":
                sql = """ UPDATE post_info SET examination = 2 WHERE id = {}"""
            else:
                sql = """ UPDATE post_info SET examination = 0 WHERE id = {}"""
            g.db.cursor.execute(sql.format(post_id))
            g.db.commit()
        except:
            return "fail"
        else:
            return "success"
    return redirect(url_for("menu.index"))


@menu.route('/deletepost', methods=['GET'])
@authorize
def delete_post():
    # 简单验证, 验证通过更据 id 直接删除
    if str(hash(str(request.args.get('id')))) == str(request.args.get('key')):
        sql = 'delete from post_info where id=%s;' % int(request.args.get('id'))
        if g.db.cursor.execute(sql):
            flash(u'删除成功!')
            g.db.commit()
            return redirect(url_for('menu.article_records'))
    flash(u'删除失败！请刷新页面再试！')
    return redirect(url_for('menu.article_records'))