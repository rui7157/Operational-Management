# -*- coding: utf-8


# -*- coding: utf-8

from . import adm
from cdms.view.wrapper import authorize
from flask import flash, request, url_for, render_template, g, redirect, session, abort


@adm.route("/add_member",methods = ["GET","POST"])
@authorize
def add_member():


    return render_template("admin/add_member.html")