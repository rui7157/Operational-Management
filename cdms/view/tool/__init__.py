from flask import Blueprint

tool = Blueprint("tool",__name__)
from . import tools,baidu_query