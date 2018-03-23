# -*- coding: utf-8 -*-
from flask_assets import Environment, Bundle

# Create the Flask-Assets instance
assets_env = Environment()

bundles = {
    'admin_js': Bundle(
        'js/jquery.min.js',
        'js/bootstrap.min.js',
        'js/jquery.cookie.js',
        'js/sweetalert2.all.js',
        'js/nprogress.js',
        'js/select2.js',
        'js/moxie.min.js',
        'js/plupload.full.min.js',
        'js/jquery.plupload.queue.js',
        'js/bootstrap-datetimepicker.js',
        'js/clipboard.js',
        'js/jquery.pjax.js',
        output='js/admin.min.js'
    ),
    'app_js': Bundle(
        'js/app.js',
        filters='jsmin',
        output='js/app.min.js'
    ),
    'admin_css': Bundle(
        'css/bootstrap.min.css',
        'css/todc-bootstrap.min.css',
        'css/font-awesome.css',
        'css/fineix.css',
        'css/nprogress.css',
        'css/sweetalert.css',
        'css/select2.css',
        'css/jquery.plupload.queue.css',
        'css/bootstrap-datetimepicker.css',
        filters='cssmin',
        output='css/admin.min.css'
    ),
    'app_css': Bundle(
        'css/app.css',
        filters='cssmin',
        output='css/app.min.css'
    ),
    'web_css': Bundle(
        'css/website.css',
        filters='cssmin',
        output='css/website.min.css'
    ),
    'themes_css': Bundle(
        'css/adminlte.css',
        'css/all-skins.css',
        filters='cssmin',
        output='css/dark-green.min.css'
    )
}
