# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, current_app, abort

from . import adminlte
from vimage import db
from vimage.models import Sensitive
from vimage.forms import SensitiveWordsForm


def load_common_data():
    """
    私有方法，装载共用数据
    """
    return {
        'top_menu': 'sensitive_words',
        'sub_menu': 'sensitive_words'
    }


@adminlte.route('/sensitive_words')
@adminlte.route('/sensitive_words/<int:page>')
def get_sensitive_words(page=1):
    """获取所有的敏感词列表"""

    return '敏感词列表'


@adminlte.route('/sensitive_words/create', methods=['GET', 'POST'])
def create_sensitive_word():
    """添加敏感词"""

    form = SensitiveWordsForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            sensitive_word = Sensitive(
                word=form.word.data,
                type=form.type.data
            )

            db.session.add(sensitive_word)
            db.session.commit()

            flash('添加敏感词成功', 'success')
        else:
            current_app.logger.warn('Add Sensitive word error: %s' % form.errors)
            return redirect(url_for('adminlte.create_sensitive_word'))

        return redirect(url_for('adminlte.get_sensitive_words'))

    mode = 'create'
    return render_template('adminlte/sensitive_words/create_and_edit.html',
                           mode=mode,
                           form=form,
                           **load_common_data())


@adminlte.route('/sensitive_words/edit', methods=['POST'])
def edit_sensitive_word():
    """编辑敏感词"""

    return '编辑敏感词'


@adminlte.route('/sensitive_words/delete', methods=['GET'])
def delete_sensitive_word():
    """删除敏感词"""

    return '删除敏感词'
