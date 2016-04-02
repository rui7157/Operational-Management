# -*- coding: utf-8

from . import adm
from cdms.view.wrapper import authorize
from flask import flash, request, url_for, render_template, g, redirect, session, abort
from ..wrapper import generate_sql





@adm.route("/add_server.php",methods=["GET","POST"])
def add_server():
    #添加服务器


    if request.method == "POST":
        sql=generate_sql(request.form,"add")
        try:
            print sql
            g.db.cursor.execute(sql)
            g.db.commit()
            flash("服务器添加成功！")
        except Exception:
            flash("添加失败！")
    return render_template("admin/add_server.html")


@adm.route("/query_server.exe")
def query_server():
    sql="""SELECT `server_name`,`server_account`,`server_password`,`server_ip`,`server_lan_ip`,`root_auth`,`login_path`,`ftp_auth`,`ip_ext`,`price`,DATE_FORMAT(`start_time`,'%Y-%m-%d'),DATE_FORMAT(`end_time`,'%Y-%m-%d') FROM server ORDER BY `end_time`;""" #,sql_host,sql_user,sql_password
    g.db.cursor.execute(sql)
    data=g.db.cursor.fetchall()
    return render_template("admin/query_server.html",data=data)

@adm.route("/modify_server",methods=["GET","POST"])
def modify_server():
    if request.method=="POST":
        sql = generate_sql(request.form,"modify",request.form.get("sid"))
        try:
            g.db.cursor.execute(sql)
            g.db.commit()
            return "success"
        except Exception:
            return "fail"

    if request.method=="GET":
        sql="""SELECT `id`,`server_name`,`server_account`,`server_password`,`server_ip`,`server_lan_ip`,`root_auth`,`login_path`,`ftp_auth`,`ip_ext`,`price`,DATE_FORMAT(`start_time`,'%Y-%m-%d'),DATE_FORMAT(`end_time`,'%Y-%m-%d') FROM server ORDER BY `end_time`;""" #,sql_host,sql_user,sql_password
        g.db.cursor.execute(sql)
        data=g.db.cursor.fetchall()
        return render_template("admin/modify_server.html",data=data)

@adm.route("/delete_server",methods=["POST"])
def delete_server():
    sid=request.form.get("sid")
    sql="""DELETE FROM server WHERE id={sid};""".format(sid=sid)
    try:
        print sql
        g.db.cursor.execute(sql)
        g.db.commit()
        return "success"
    except IOError:
        return "fail"