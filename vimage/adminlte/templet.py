# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, current_app, abort

from . import adminlte
from vimage import db
from vimage.models import Templet
from vimage.forms import TempletForm


def load_common_data():
    """
    私有方法，装载共用数据
    """
    return {
        'top_menu': 'templets',
        'sub_menu': 'templets'
    }


@adminlte.route('/templets')
@adminlte.route('/templets/<int:page>')
def get_templets(page=1):
    """获取所有模板列表"""
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', 0, type=int)

    builder = Templet.query

    if status:
        builder = builder.filter_by(status=status)

    paginated_templets = builder.order_by(Templet.created_at.desc()).paginate(page, per_page)

    return render_template('adminlte/templet/show_list.html',
                           paginated_templets=paginated_templets,
                           **load_common_data())


@adminlte.route('/templets/create', methods=['GET', 'POST'])
def create_templet():
    """添加新模板"""
    form = TempletForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            templet = Templet(
                name=form.name.data,
                cover_id=form.cover_id.data,
                type=form.type.data,
                requirements=form.requirements.data,
                status=form.status.data
            )
            db.session.add(templet)

            db.session.commit()

            flash('添加模板成功', 'success')
        else:
            current_app.logger.warn('Create templet error: %s' % form.errors)
            return redirect(url_for('adminlte.create_templet'))

        return redirect(url_for('adminlte.get_templets'))

    mode = 'create'
    return render_template('adminlte/templet/create_and_edit.html',
                           mode=mode,
                           form=form,
                           **load_common_data())


@adminlte.route('/templets/<string:rid>/edit', methods=['GET', 'POST'])
def edit_templet(rid):
    """编辑模板信息"""
    templet = Templet.query.filter_by(sn=rid).first_or_404()
    form = TempletForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(templet)

            db.session.commit()

            flash('编辑模板成功', 'success')
        else:
            current_app.logger.warn('Edit templet error: %s' % form.errors)
            return redirect(url_for('adminlte.edit_templet', rid=rid))

        return redirect(url_for('adminlte.get_templets'))

    mode = 'edit'
    form.name.data = templet.name
    form.cover_id.data = templet.cover_id
    form.type.data = templet.type
    form.requirements.data = templet.requirements
    form.status.data = templet.status
    return render_template('adminlte/templet/create_and_edit.html',
                           mode=mode,
                           form=form,
                           templet=templet,
                           **load_common_data())


@adminlte.route('/templets/delete', methods=['POST'])
def delete_templet():
    """删除模板"""
    selected_ids = request.form.getlist('selected[]')
    if not selected_ids or selected_ids is None:
        flash('Delete templet is null!', 'danger')
        abort(404)

    try:
        for rid in selected_ids:
            templet = Templet.query.filter_by(sn=rid).first()
            if templet:
                db.session.delete(templet)

        db.session.commit()

        flash('Delete templet is ok!', 'success')
    except Exception as err:
        db.session.rollback()
        flash('Delete country is error: %s!!!' % str(err), 'danger')

    return redirect(url_for('.get_templets'))
