# -*- coding: utf-8


# -*- coding: utf-8

from . import adm
from cdms.view.wrapper import authorize
from flask import flash, request, url_for, render_template, g, redirect, session, abort


@adm.route("/add_member", methods=["GET", "POST"])
@authorize
def add_member():
    # 添加成员
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        group = request.form["group"]
        if username != "" and password != "" and group != "":
            sql = """INSERT INTO users (`username`,`password`,`user_quarter_id`,`exa_user`,`group`) VALUE ('{username}','{password}',1,0,{group})"""
            try:
                g.db.cursor.execute(sql.format(username=username, password=password, group=int(group)))
                g.db.commit()
                flash("插入用户：“{username}”，成功！".format(username=username))
            except Exception:
                flash("操作失败！")
        else:
            flash("输入不能为空！")
        return redirect(url_for("adm.add_member"))
    return render_template("admin/add_member.html")
