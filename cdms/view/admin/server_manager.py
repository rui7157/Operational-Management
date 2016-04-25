# -*- coding: utf-8

from . import adm
from cdms.view.wrapper import authorize
from flask import flash, request, url_for, render_template, g, redirect, session, abort
from ..wrapper import generate_sql
import xlrd
import os
from werkzeug.utils import secure_filename


@adm.route("/add_server.php", methods=["GET", "POST"])
def add_server():
    # 添加服务器


    if request.method == "POST":
        sql = generate_sql(request.form, "add")
        try:
            g.db.cursor.execute(sql)
            g.db.commit()
            flash("服务器添加成功！")
        except Exception:
            flash("添加失败！")
    return render_template("admin/add_server.html")


@adm.route("/query_server")
def query_server():
    # 查询服务器
    sql = """SELECT `id`,`application`,`server_name`,`server_account`,`server_password`,`server_ip`,`server_lan_ip`,`root_auth`,`login_path`,`ftp_auth`,`ip_ext`,`price`,DATE_FORMAT(`start_time`,'%Y-%m-%d'),DATE_FORMAT(`end_time`,'%Y-%m-%d') FROM server ORDER BY `end_time`;"""  # ,sql_host,sql_user,sql_password
    g.db.cursor.execute(sql)
    data = g.db.cursor.fetchall()
    return render_template("admin/query_server.html", data=data)


@adm.route("/modify_server", methods=["GET", "POST"])
def modify_server():
    # 修改服务器
    if request.method == "POST":
        sql = generate_sql(request.form, "modify", request.form.get("sid"))
        try:
            g.db.cursor.execute(sql)
            g.db.commit()
            return "success"
        except Exception:
            return "fail"

    if request.method == "GET":
        sql = """SELECT `id`,`application`,`server_name`,`server_account`,`server_password`,`server_ip`,`server_lan_ip`,`root_auth`,`login_path`,`ftp_auth`,`ip_ext`,`price`,DATE_FORMAT(`start_time`,'%Y-%m-%d'),DATE_FORMAT(`end_time`,'%Y-%m-%d') FROM server ORDER BY `end_time`;"""  # ,sql_host,sql_user,sql_password
        g.db.cursor.execute(sql)
        data = g.db.cursor.fetchall()
        return render_template("admin/modify_server.html", data=data)


@adm.route("/delete_server", methods=["POST"])
def delete_server():
    # 删除服务器
    sid = request.form.get("sid")
    sql = """DELETE FROM server WHERE id={sid};""".format(sid=sid)
    g.db.cursor.execute(sql)
    g.db.commit()
    try:
        g.db.cursor.execute(sql)
        g.db.commit()
        return "success"
    except Exception:
        return "fail"


@adm.route("/add_application", methods=["GET", "POST"])
def add_application():
    # 添加服务器
    if request.method == "GET":
        sid = request.args.get("sid", None)
        if sid == None:
            abort(404)
        sql = """SELECT `id`,`ip`,`name`,`domain`,`icp`FROM site WHERE server_id={sid}""".format(sid=sid)
        g.db.cursor.execute(sql)
        data = g.db.cursor.fetchall()
        # data=data[1:] #排除第一个id数据
        sql = """SELECT `id`,`application`,`server_name`,`server_account`,`server_password`,`server_ip`,`server_lan_ip`,`root_auth`,`login_path`,`ftp_auth`,`ip_ext`,`price`,DATE_FORMAT(`start_time`,'%Y-%m-%d'),DATE_FORMAT(`end_time`,'%Y-%m-%d') FROM server WHERE id={sid}""".format(
                sid=sid)
        g.db.cursor.execute(sql)
        server_data = g.db.cursor.fetchall()[0]
        return render_template("admin/add_site.html", data=data, server_data=server_data)

    if request.method == "POST":
        sid = request.form.get("sid")
        ip = request.form.get("ip")
        name = request.form.get("name")
        domain = request.form.get("domain")
        icp = request.form.get("icp")
        sql = """INSERT INTO site (`ip`,`name`,`domain`,`icp`,`server_id`) VALUE ('{ip}','{name}','{domain}','{icp}',{sid});""".format(
                sid=sid, ip=ip, name=name, domain=domain, icp=icp)
        try:
            g.db.cursor.execute(sql)
            g.db.commit()
            flash(u"添加成功！")
        except Exception:
            flash(u"添加失败！")
        return redirect(url_for('adm.add_application') + '?&sid=' + sid)


@adm.route("/article_records_excel", methods=["POST"])
def article_records_excel():
    # 接受EXCEL
    def write_sql(str_data):
        success = 0
        fail_data = ""
        for index, i in enumerate(str_data):
            try:
                title = i[0].replace("?", "")
                url = i[1]
                success += 1
            except IndexError:
                fail_data = fail_data + str(index + 1) + ":" + "".join(i) + " | "
                continue
            g.db.cursor.execute('INSERT INTO  post_info (user_name_id, post_title, post_address, post_date) ' \
                                'VALUES(%s, "%s", "%s",  now());' % (session['user_name_id'], title, url))
            g.db.commit()
        return fail_data, success

    f = request.files["filename"]
    filename = secure_filename(f.filename)
    fileformat = filename.split(".")[-1:][0]
    if fileformat == "txt":
        str_data = f.readlines()
        str_data = [i.decode('gbk').split() for i in str_data]
        fail_data, success = write_sql(str_data)
    elif fileformat in ["xls", "xlsx", "XLS", "XLSX"]:
        filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "static", "upload", filename)
        f.save(filepath)
        f = xlrd.open_workbook(filepath)
        os.remove(filepath)
        sheet_data = f.sheet_by_index(0)
        row_count = sheet_data.nrows
        excel_data = []
        for row_num in xrange(row_count):
            excel_data.append([sheet_data.cell(row_num, 0).value, sheet_data.cell(row_num, 1).value])
        fail_data, success = write_sql(excel_data)
    else:
        flash("不支持您所上传的文件类型！")
    if fail_data:
        flash("成功{success}条，失败的条目：{fail}".format(success=success, fail=str(fail_data)))
    else:
        flash("成功上传所有条目{}条！".format(success))
    return redirect(url_for("menu.article_records"))


@adm.route("/query_site")
def query_site():
    # 查询站点
    sid = request.args.get("sid", None)
    if sid == None:
        abort(404)

    sql = """SELECT `id`,`ip`,`name`,`domain`,`icp` FROM site WHERE server_id={sid}""".format(sid=sid)
    g.db.cursor.execute(sql)
    data = g.db.cursor.fetchall()

    sql = """SELECT `id`,`application`,`server_name`,`server_account`,`server_password`,`server_ip`,`server_lan_ip`,`root_auth`,`login_path`,`ftp_auth`,`ip_ext`,`price`,DATE_FORMAT(`start_time`,'%Y-%m-%d'),DATE_FORMAT(`end_time`,'%Y-%m-%d') FROM server WHERE id={sid}""".format(
            sid=sid)
    g.db.cursor.execute(sql)
    server_data = g.db.cursor.fetchall()[0]

    return render_template("admin/query_site.html", data=data, server_data=server_data)


@adm.route("/delete_site", methods=["POST"])
def delete_site():
    # 删除站点
    wid = request.form.get("wid")
    sql = """DELETE FROM site WHERE id={wid}; """.format(wid=wid)
    try:
        g.db.cursor.execute(sql)
        g.db.commit()
        return "success"
    except Exception:
        return "fail"

@adm.route("/search_site",methods=["POST"])
def search_site():
    #搜索站点

    text=request.form.get("text",None)
    if text:
        sql="""SELECT  `id`,`ip`,`name`,`domain`,`icp` FROM site WHERE concat_ws(`name`,`domain`,`icp`,`ip`) LIKE '%{text}%' """.format(text=text)
        g.db.cursor.execute(sql)
        data = g.db.cursor.fetchall()
    else:
        flash(u"请输入搜索内容！")
        return redirect(url_for('.query_server'))
    if not data:
        flash(u"搜索不到相关信息！")
        return redirect(url_for('.query_server'))

    return render_template("admin/query_site.html", data=data)