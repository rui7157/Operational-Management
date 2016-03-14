# -*- coding: utf-8

from flask import Blueprint
from ..wrapper import authorize

other = Blueprint("other",__name__)




from . import oth
