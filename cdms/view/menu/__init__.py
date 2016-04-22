from flask import Blueprint
from ..wrapper import  authorize
menu = Blueprint("menu", __name__, static_folder='../../static', template_folder='../../templates')

from . import index, article_records, login, mail, post_count, register_web_info_view,page
