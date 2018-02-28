# -*- coding: utf-8 -*-
# 装载静态文件
from flask_bootstrap import Bootstrap
# 数据库连接
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_cdn import CDN
# 管理用户认证系统中的认证状态
from flask_login import LoginManager
# 缓存
from flask_caching import Cache
# 后台定时任务
from flask_celery import Celery


db = SQLAlchemy()
csrf = CSRFProtect()
cache = Cache()
# Create the Flask-Celery-Helper's instance
fsk_celery = Celery()
bootstrap = Bootstrap()
# Flask-Login初始化
login_manager = LoginManager()
# cdn
cdn = CDN()
