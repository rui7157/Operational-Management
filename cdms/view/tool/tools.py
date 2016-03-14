# -*- coding: utf-8 -*-
from . import tool
from flask import render_template


@tool.route("/tools")
def tools():
    return render_template("tools.html")