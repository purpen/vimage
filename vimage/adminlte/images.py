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

    return '图片列表'


@adminlte.route('/images/create', methods=['GET', 'POST'])
def add_images():
    """添加图片元素"""

    form = ImagesForm()

    # if request.method == 'POST':
    #     if form.validate_on_submit():
    #         image = ImageSet(
    #             name=form.name.data,
    #             description=form.description.data,
    #             tags=form.tags.data,
    #             type=form.type.data
    #         )
    #
    #         db.session.add(image)
    #         db.session.commit()
    #
    #         flash('添加图片成功', 'success')
    #     else:
    #         current_app.logger.warn('Add images error: %s' % form.errors)
    #         return redirect(url_for('adminlte.add_sensitive_word'))
    #
    #     return redirect(url_for('adminlte.add_images'))

    mode = 'create'
    return render_template('adminlte/images/create_and_edit.html',
                           mode=mode,
                           form=form,
                           **load_common_data())


@adminlte.route('/images/edit', methods=['POST'])
def edit_images():
    """编辑图片信息"""

    return '编辑图片信息'


@adminlte.route('/images/delete', methods=['GET'])
def delete_images():
    """删除图片元素"""

    return '删除图片元素'
