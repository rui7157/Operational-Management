# -*- coding: utf-8

from . import adm
from cdms.view.wrapper import authorize
from flask import flash, request, url_for, render_template, g, redirect, session,abort


@adm.route("/")
@authorize
def admin():
    # if session.get('group') !=0:
    #     abort(403)


    return render_template("admin/admin.html")
