# -*- coding: utf-8 -*-
from flask import request, url_for, abort, g

from . import api
from vimage.models import Templet
from vimage.helpers.utils import *


@api.route('/templets')
def get_templets():
    """获取模板列表"""
    _type = request.args.get('type')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    builder = Templet.query

    if _type:
        builder = builder.filter_by(type=_type)

    pagination = builder.order_by(Templet.created_at.asc()).paginate(page, per_page=per_page, error_out=False)
    templets = pagination.items
    prev_url = None
    if pagination.has_prev:
        prev_url = url_for('api.get_templets', page=page - 1, _external=True)
    next_url = None
    if pagination.has_next:
        next_url = url_for('api.get_templets', page=page + 1, _external=True)

    return full_response(R200_OK, {
        'templets': [templet.to_json() for templet in templets],
        'prev': prev_url,
        'next': next_url,
        'count': pagination.total
    })
