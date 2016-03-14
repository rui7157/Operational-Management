# -*- coding: utf-8 -*-

from flask import Blueprint

other = Blueprint("other", __name__)

from . import oth
