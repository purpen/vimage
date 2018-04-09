# -*- coding: utf-8 -*-
"""
    __init__.py
    ~~~~~~~~~~~~~~
    :copyright: (c) 2018 by purpen.
"""
import os
from flask import Flask
# 导入扩展
from .extensions import (
    db,
    csrf,
    cache,
    cdn,
    fsk_celery,
    bootstrap,
    login_manager
)
# 导入上传
from flask_uploads import UploadSet, configure_uploads, patch_request_class
from .assets import assets_env, bundles
# 导入配置参数
from config import config

basedir = os.path.abspath(os.path.dirname(__file__))

# 创建set
uploader = UploadSet(
    'photos',
    extensions=('xls', 'xlsx', 'jpg', 'jpe', 'jpeg', 'png', 'gif', 'csv')
)
# 属性可以设为None、'basic' 或'strong'
login_manager.session_protection = 'strong'
# 设置登录页面的端点
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 加载私有环境变量
    if os.path.exists('%s/private_config.py' % basedir):
        app.config.from_pyfile('%s/private_config.py' % basedir)

    config[config_name].init_app(app)
    
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    assets_env.init_app(app)
    assets_env.register(bundles)
    # cdn
    cdn.init_app(app)
    # 缓存
    cache.init_app(app)

    # Init the Flask-Celery-Helper via app object
    # Register the celery object into app object
    fsk_celery.init_app(app)

    # 初始化上传
    configure_uploads(app, uploader)
    # 文件大小限制，默认为16MB
    patch_request_class(app)

    # logging setting
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(app.config['ERROR_LOG'])
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.DEBUG)
        app.logger.info('Mix startup')

    # attach routes

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .adminlte import adminlte as adminlte_blueprint
    app.register_blueprint(adminlte_blueprint, url_prefix='/adminlte')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
    # 禁用csrf
    csrf.exempt(api_1_0_blueprint)

    return app
