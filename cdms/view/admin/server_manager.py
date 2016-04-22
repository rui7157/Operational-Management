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
    sql="""SELECT `application`,`server_name`,`server_account`,`server_password`,`server_ip`,`server_lan_ip`,`root_auth`,`login_path`,`ftp_auth`,`ip_ext`,`price`,DATE_FORMAT(`start_time`,'%Y-%m-%d'),DATE_FORMAT(`end_time`,'%Y-%m-%d') FROM server ORDER BY `end_time`;""" #,sql_host,sql_user,sql_password
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
        sql="""SELECT `id`,`application`,`server_name`,`server_account`,`server_password`,`server_ip`,`server_lan_ip`,`root_auth`,`login_path`,`ftp_auth`,`ip_ext`,`price`,DATE_FORMAT(`start_time`,'%Y-%m-%d'),DATE_FORMAT(`end_time`,'%Y-%m-%d') FROM server ORDER BY `end_time`;""" #,sql_host,sql_user,sql_password
        g.db.cursor.execute(sql)
        data=g.db.cursor.fetchall()
        return render_template("admin/modify_server.html",data=data)

@adm.route("/delete_server",methods=["POST"])
def delete_server():
    sid=request.form.get("sid")
    sql="""DELETE FROM server WHERE id={sid};""".format(sid=sid)
    print sql
    g.db.cursor.execute(sql)
    g.db.commit()
    try:
        g.db.cursor.execute(sql)
        g.db.commit()
        return "success"
    except Exception:
        return "fail"




@adm.route("/add_application",methods=["GET","POST"])
def add_application():
    if request.method=="GET":
        sid=request.args.get("sid",None)
        if sid==None:
            abort(404)
        sql="""SELECT `id`,`ip`,`name`,`domain`,`other`FROM site WHERE server_id={sid}""".format(sid=sid)
        g.db.cursor.execute(sql)
        data=g.db.cursor.fetchall()
        # data=data[1:] #排除第一个id数据
        sql="""SELECT `id`,`application`,`server_name`,`server_account`,`server_password`,`server_ip`,`server_lan_ip`,`root_auth`,`login_path`,`ftp_auth`,`ip_ext`,`price`,DATE_FORMAT(`start_time`,'%Y-%m-%d'),DATE_FORMAT(`end_time`,'%Y-%m-%d') FROM server WHERE id={sid}""".format(sid=sid)
        g.db.cursor.execute(sql)
        server_data=g.db.cursor.fetchall()[0]
        return render_template("admin/add_site.html",data=data,server_data=server_data)

    if request.method=="POST":
        sid=request.form.get("sid")
        ip=request.form.get("ip")
        name=request.form.get("name")
        domain=request.form.get("domain")
        other=request.form.get("other")
        sql="""INSERT INTO site (`ip`,`name`,`domain`,`other`,`server_id`) VALUE ('{ip}','{name}','{domain}','{other}',{sid});""".format(sid=sid,ip=ip,name=name,domain=domain,other=other)
        try:
            g.db.cursor.execute(sql)
            g.db.commit()
            flash(u"添加成功！")
        except Exception:
            flash(u"添加失败！")
        return redirect(url_for('adm.add_application')+'?&sid='+sid)

@adm.route("/delete_site",methods=["POST"])
def delete_site():
    wid=request.form.get("wid")
    sql="""DELETE FROM site WHERE id={wid}; """.format(wid=wid)
    try:
        g.db.cursor.execute(sql)
        g.db.commit()
        return "success"
    except Exception:
        return "fail"
