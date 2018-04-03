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

    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', 0, type=int)

    builder = Sensitive.query

    if status:
        builder = builder.filter_by(status=status)

    paginated_sensitive_words = builder.order_by(Sensitive.id).paginate(page, per_page)

    return render_template('adminlte/sensitive_words/show_list.html',
                           paginated_sensitive_words=paginated_sensitive_words,
                           **load_common_data())


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


@adminlte.route('/sensitive_words/<string:rid>/edit', methods=['GET', 'POST'])
def edit_sensitive_word(rid):
    """编辑敏感词"""

    sensitive_word = Sensitive.query.filter_by(id=rid).first_or_404()
    form = SensitiveWordsForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(sensitive_word)

            db.session.commit()

            flash('编辑敏感词成功', 'success')
        else:
            current_app.logger.warn('Edit sensitive word error: %s' % form.errors)
            return redirect(url_for('adminlte.edit_sensitive_word', rid=rid))

        return redirect(url_for('adminlte.get_sensitive_words'))

    mode = 'edit'
    form.type.data = sensitive_word.type
    form.word.data = sensitive_word.word
    return render_template('adminlte/sensitive_words/create_and_edit.html',
                           mode=mode,
                           form=form,
                           sensitive_word=sensitive_word,
                           **load_common_data())


@adminlte.route('/sensitive_words/delete', methods=['POST'])
def delete_sensitive_word():
    """删除敏感词"""

    selected_ids = request.form.getlist('selected[]')
    if not selected_ids or selected_ids is None:
        flash('Delete sensitive word is null!', 'danger')
        abort(404)

    try:
        for rid in selected_ids:
            sensitive_word = Sensitive.query.filter_by(id=rid).first()
            if sensitive_word:
                db.session.delete(sensitive_word)

        db.session.commit()

        flash('敏感词已删除！', 'success')
    except Exception as err:
        db.session.rollback()
        flash('Delete country is error: %s!!!' % str(err), 'danger')

    return redirect(url_for('.get_sensitive_words'))
