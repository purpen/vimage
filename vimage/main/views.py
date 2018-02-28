# -*- coding: utf-8 -*-
from datetime import timedelta
from flask import jsonify, current_app, request, redirect, url_for
from flask_sqlalchemy import get_debug_queries
from . import main
from .. import db


@main.route('/helloworld')
def helloworld():
    """测试示例"""
    return 'Hello World!'
