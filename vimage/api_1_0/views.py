# -*- coding: utf-8 -*-
"""
    views.py

    :copyright: (c) 2018 by purpen.
"""
from flask import request, abort, g, url_for, jsonify

from . import api
from vimage.helpers.utils import *
from vimage.helpers.image_make import *
from vimage.models import ImageSet
from vimage.models.sensitive import *
from vimage import db


@api.route('/', methods=['GET'])
def hello_world():
    """test"""

    return 'Hello World!'
