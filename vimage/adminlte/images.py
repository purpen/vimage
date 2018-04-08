# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, current_app, abort

from . import adminlte
from vimage import db
from vimage.models import ImageSet
from vimage.forms import ImagesForm


def load_common_data():
    """
    私有方法，装载共用数据
    """
    return {
        'top_menu': 'images',
        'sub_menu': 'images'
    }


@adminlte.route('/images')
@adminlte.route('/images/<int:page>')
def get_images(page=1):
    """获取所有的图片列表"""

    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', 0, type=int)

    builder = ImageSet.query

    if status:
        builder = builder.filter_by(status=status)

    paginated_images = builder.order_by(ImageSet.created_at.desc()).paginate(page, per_page)

    return render_template('adminlte/images/show_list.html',
                           paginated_images=paginated_images,
                           **load_common_data())


@adminlte.route('/images/create', methods=['GET', 'POST'])
def create_image():
    """添加图片元素"""

    form = ImagesForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            image = ImageSet(
                name=form.name.data,
                description=form.description.data,
                cover_id=form.cover_id.data,
                tags=form.tags.data,
                type=form.type.data
            )

            db.session.add(image)
            db.session.commit()

            flash('添加图片成功!', 'success')
        else:
            current_app.logger.warn('Add images error: %s' % form.errors)
            return redirect(url_for('adminlte.create_image'))

        return redirect(url_for('adminlte.get_images'))

    mode = 'create'
    return render_template('adminlte/images/create_and_edit.html',
                           mode=mode,
                           form=form,
                           **load_common_data())


@adminlte.route('/images/<string:rid>/edit', methods=['GET', 'POST'])
def edit_image(rid):
    """编辑图片信息"""

    image = ImageSet.query.filter_by(sn=rid).first_or_404()
    form = ImagesForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(image)

            db.session.commit()

            flash('编辑模板成功', 'success')
        else:
            current_app.logger.warn('Edit image error: %s' % form.errors)
            return redirect(url_for('adminlte.edit_image', rid=rid))

        return redirect(url_for('adminlte.get_images'))

    mode = 'edit'
    form.name.data = image.name
    form.cover_id.data = image.cover_id
    form.type.data = image.type
    form.description.data = image.description
    form.tags.data = image.tags
    form.status.data = image.status
    return render_template('adminlte/images/create_and_edit.html',
                           mode=mode,
                           form=form,
                           image=image,
                           **load_common_data())


@adminlte.route('/images/delete', methods=['POST'])
def delete_image():
    """删除图片元素"""

    selected_ids = request.form.getlist('selected[]')
    if not selected_ids or selected_ids is None:
        flash('Delete image is null!', 'danger')
        abort(404)

    try:
        for rid in selected_ids:
            image = ImageSet.query.filter_by(sn=rid).first()
            if image:
                db.session.delete(image)

        db.session.commit()

        flash('图像已删除！', 'success')
    except Exception as err:
        db.session.rollback()
        flash('Delete country is error: %s!!!' % str(err), 'danger')

    return redirect(url_for('.get_images'))
