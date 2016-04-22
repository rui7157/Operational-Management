# coding: utf-8
from . import menu
from ..wrapper import authorize
from flask import render_template,redirect,url_for



@menu.route("/", methods=['GET', 'POST'])
@authorize
def index():
    # 主页
    return render_template('index.html')
