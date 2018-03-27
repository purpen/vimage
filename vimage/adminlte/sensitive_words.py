# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, current_app, abort

from . import adminlte
from vimage import db
from vimage.models import Sensitive


@adminlte.route('/sensitive_words')
@adminlte.route('/sensitive_words/<int:page>')
def get_sensitive_words(page=1):
    """获取所有的敏感词列表"""

    return '敏感词列表'


@adminlte.route('/sensitive_words/add', methods=['POST'])
def add_sensitive_word():
    """添加敏感词"""

    return '添加敏感词'


@adminlte.route('/sensitive_words/edit', methods=['POST'])
def edit_sensitive_word():
    """编辑敏感词"""

    return '编辑敏感词'


@adminlte.route('/sensitive_words/delete', methods=['GET'])
def delete_sensitive_word():
    """删除敏感词"""

    return '删除敏感词'
