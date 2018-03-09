# -*- coding: utf-8 -*-

from flask import Blueprint

main = Blueprint('mainImage', __name__)

from . import views
