# -*- coding: utf-8 -*-
from flask import render_template

from . import adminlte


@adminlte.route('/')
def dashboard():
    """管理控制台"""

    return render_template('adminlte/dashboard.html')
