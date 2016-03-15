# -*- coding: utf-8

from . import menu
from ..wrapper import authorize
from flask import  flash, request, url_for, render_template, g, redirect, session



@menu.route("/admin")
@authorize
def admin():
    

    return render_template("user.html")