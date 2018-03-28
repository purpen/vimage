# -*- coding: utf-8 -*-
from . import main


@main.route('/')
def index():
    """欢迎页"""
    return 'Hello, Moebeast!'
