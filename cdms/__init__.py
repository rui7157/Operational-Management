#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created by bayonet on 16-2-26.

import functools
import thread
from flask import Flask, flash, request, url_for, render_template, g, redirect, session
from flask.ext.mail import Mail
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

try:
    import MySQLdb
except Exception:
    import pymysql as MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')

lock = thread.allocate_lock()

from flask import Flask
from config import config


app = Flask(__name__)
mail=Mail()

def create_app(config_name):
    from view.tool import tool
    from view.menu import menu
    from view.other import other
    from view.admin import adm

    app.config.from_object(config[config_name])
    mail.init_app(app)
    app.secret_key = app.config["SECRET_KEY"]
    app.register_blueprint(menu)
    app.register_blueprint(tool)
    app.register_blueprint(other)
    app.register_blueprint(adm,url_prefix='/admin')
    return app



try:
    import MySQLdb
except Exception:
    import pymysql as MySQLdb


@app.before_request
def before_request():
    """ 在请求前 建立数据库连接 """
    g.db = MySQLdb.connect(host=app.config['SQL_HOST'], user=app.config['USER'], db=app.config['DB'],
                           charset=app.config['CHARSET'])
    g.db.cursor = g.db.cursor()


@app.teardown_request
def teardown_request(exception):
    """ 在请求后 关闭数据库连接 """
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
