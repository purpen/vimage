# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_cors import CORS

api = Blueprint('api', __name__)

# 存在跨域的问题
CORS(api)

from . import views, maker, tools, templet
