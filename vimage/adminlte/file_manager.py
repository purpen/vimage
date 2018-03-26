# -*- coding: utf-8 -*-
import re
import time
import hashlib
from urllib import parse
from os.path import splitext
from PIL import Image
from flask import current_app, render_template, url_for, request, jsonify
from wtforms import ValidationError
from pymysql.err import IntegrityError

from vimage import db, uploader
from . import adminlte
from vimage.models import Asset, Directory
from vimage.helpers import QiniuStorage
from vimage.helpers.utils import *


@adminlte.route('/file_manager/folder', methods=['POST'])
def folder():
    parent_id = 0
    top = 0
    success = True

    if request.method == 'POST':
        sub_folder = request.form.get('folder')
        parent_directory = request.form.get('parent_directory', '')

        sub_folder = parse.unquote(sub_folder)
        # 截取头尾空格
        sub_folder = sub_folder.strip()
        # 验证目录
        if sub_folder is None or sub_folder == '':
            return custom_response(False, "Directory name isn't empty!")

        # 替换中间空格符
        sub_folder = re.sub(r'\s+', '_', sub_folder)

        pattern = re.compile(r'[!#@\$\/%\?&]')
        if len(pattern.findall(sub_folder)):
            return custom_response(False, "Directory name can't contain special characters [!#@$/?&]!")

        if Directory.query.filter_by(name=sub_folder).first():
            return custom_response(False, "Directory name is already exist!")

        if parent_directory != '':
            directories = parent_directory.split('/')
            # pop last item
            last_directory_name = directories.pop()
            last_directory = Directory.query.filter_by(name=last_directory_name).first()

            parent_id = last_directory.id
            top = 1

        try:
            directory = Directory(
                name=sub_folder,
                parent_id=parent_id,
                top=top
            )

            db.session.add(directory)

            db.session.commit()

        except ValidationError:
            success = False

    return status_response(success)


@adminlte.route('/file_manager/show_asset')
@adminlte.route('/file_manager/show_asset/<int:page>')
def show_asset(page=1):
    per_page = 20
    parent_directory = ''
    all_directory = []
    paginated_assets = []

    current_directory = request.args.get('directory', '')
    up_target = request.args.get('up_target', 'mic')
    # top level
    if current_directory == '' or current_directory is None:
        all_directory = Directory.query.filter_by(top=0).all()
        paginated_assets = Asset.query.filter_by(directory_id=0).paginate(page, per_page)
    else:
        directories = current_directory.split('/')
        # pop last item
        last_directory_name = directories.pop()

        last_directory = Directory.query.filter_by(name=last_directory_name).first()

        current_app.logger.debug('Directory name: [%s]' % last_directory_name)

        if last_directory:
            all_directory = Directory.query.filter_by(parent_id=last_directory.id).all()
            paginated_assets = last_directory.assets.paginate(page, per_page)

            # 验证是否存在父级
            if last_directory.parent_id:
                # directories.pop()
                parent_directory = '/'.join(directories)

    # 生成上传token
    cfg = current_app.config
    up_token = QiniuStorage.up_token(cfg['QINIU_ACCESS_KEY'], cfg['QINIU_ACCESS_SECRET'], cfg['QINIU_BUCKET_NAME'],
                                     cfg['DOMAIN_URL'])
    if current_app.config['MODE'] == 'prod':
        up_endpoint = cfg['QINIU_UPLOAD']
    else:
        up_endpoint = url_for('adminlte.flupload')

    return render_template('file_manager.html',
                           up_target=up_target,
                           up_endpoint=up_endpoint,
                           up_token=up_token,
                           current_directory=current_directory,
                           parent_directory=parent_directory,
                           all_directory=all_directory,
                           paginated_assets=paginated_assets)


@adminlte.route('/file_manager/get_asset/<int:rid>')
def get_asset(rid):
    asset = Asset.query.get_or_404(rid)
    return jsonify(asset.to_json())


@adminlte.route('/file_manager/view_asset/<int:rid>')
def view_asset(rid):
    asset = Asset.query.get_or_404(rid)
    return jsonify(asset.to_json())


@adminlte.route('/file_manager/flupload', methods=['POST'])
def flupload():
    """开发环境文件上传，生产环境使用七牛直传"""
    saved_asset_ids = []
    sub_folder = str(time.strftime('%y%m%d'))
    root_folder = 'asset'

    directory = _pop_last_directory()
    if directory:
        current_directory = Directory.query.filter_by(name=directory).first()
        directory_id = current_directory.id
    else:
        # 获取默认目录
        current_directory = Directory.query.filter_by(is_default=True).first()
        directory_id = current_directory.id if current_directory else 0

    for f in request.files.getlist('file'):
        upload_name = f.filename
        mime_type = f.mimetype

        # Gen new file name
        file_ext = splitext(f.filename)[1].lower()
        name_prefix = 'fx' + str(time.time())
        name_prefix = hashlib.md5(name_prefix.encode('utf-8')).hexdigest()[:15]
        filename = '%s/%s/%s%s' % (root_folder, sub_folder, name_prefix, file_ext)

        # Upload to local
        filename = uploader.save(f, folder=sub_folder, name=name_prefix + '.')

        current_app.logger.warn('path: %s' % uploader.path(filename))

        # Get info of upload image
        img = Image.open(uploader.path(filename))
        img.load()
        width = img.size[0]
        height = img.size[1]

        # Update to DB
        new_asset = Asset(
            filepath=filename,
            filename=upload_name,
            directory_id=directory_id,
            width=width,
            height=height,
            mime=mime_type
        )
        db.session.add(new_asset)
        db.session.commit()

        saved_asset_ids.append(new_asset.id)

    return jsonify({
        'status': 200,
        'ids': saved_asset_ids
    })


@adminlte.route('/file_manager/pldelete', methods=['POST'])
def pldelete():
    """删除附件"""
    path_list = request.form.getlist('path[]')

    current_app.logger.debug('delete path list %s' % path_list)

    try:
        for filepath in path_list:
            if re.match(r'([a-zA-Z0-9]+\/)?[0-9]{6}\/\w{15}\.\w{3,4}$', filepath):
                asset = Asset.query.filter_by(filepath=filepath).first()
                db.session.delete(asset)
            else:
                last_directory = _pop_last_directory(filepath)
                directory = Directory.query.filter_by(name=last_directory).first()
                if directory:
                    db.session.delete(directory)

    except IntegrityError as err:
        db.session.rollback()
        current_app.logger.warn('Pldelete asset error: %s' % err)
        return custom_response('此图正在被使用中,不能被删！', 200, False)

    return status_response(R200_OK)


def _pop_last_directory(directory_path=None):
    directory_path = request.form.get('directory') if directory_path is None else directory_path
    """get the last directory"""
    last_directory = None
    if directory_path:
        directories = directory_path.split('/')
        # pop last item
        last_directory = directories.pop()
    return last_directory
