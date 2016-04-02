# -*- coding: utf-8
from flask import Blueprint

adm = Blueprint("adm",__name__)

from . import admin,user_manager,member_manager,server_manager