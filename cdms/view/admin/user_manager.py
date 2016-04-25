# -*- coding: utf-8

from . import adm
from cdms.view.wrapper import authorize
from flask import flash, request, url_for, render_template, g, redirect, session, abort


@adm.route("/modify_password", methods=["GET", "POST"])
@authorize
def modify_password():
    #修改密码
    if request.method == "POST":
        current_user_id = session.get('user_name_id')
        old_pwd = request.form['old_pwd']
        new_pwd = request.form['new_pwd']
        sql = """SELECT password FROM users WHERE id={id};"""
        g.db.cursor.execute(sql.format(id=current_user_id))
        if g.db.cursor.fetchall()[0][0] == old_pwd:
            try:
                sql = """UPDATE users SET password='{new_pwd}' WHERE id={id};"""
                g.db.cursor.execute(sql.format(new_pwd=new_pwd, id=current_user_id))
                g.db.commit()
                flash("修改成功")
                return redirect(url_for("adm.admin"))
            except Exception:
                flash("修改失败！")
                return redirect(url_for("adm.modify_password"))
        else:
            flash("密码输入错误！")
            return redirect(url_for("adm.modify_password"))
    return render_template("admin/modify_password.html")
