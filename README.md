# vimage
智能生成图片服务提供商

## 系统要求：
- Python 3.6+、Flask 1.0+、virtualenv3.5
- Mysql 5.0+、Redis
- Nginx/1.8.0
- gevent (1.1.2)
- gunicorn (19.6.0)
- celery

使用**virtualenv**安装创建独立的Python环境

项目运行于 `Python3` 环境下：

    virtualenv py3env --python=python3

启动虚拟环境：

    source py3env/bin/activate

退出虚拟环境：

    deactivate
    
## 测试环境启动

    python3 manage.py server
    
## 添加数据表

    python3 manage.py db migrate -m 'xxxx'
    
    python3 manage.py db upgrade
    
## 常用扩展说明

flower - 针对Celery的基于网页的实时管理工具, 启动命令：

    celery flower -A celery_runner --loglevel=info
    
    # 启动work
    celery worker -A celery_runner -f /var/log/celery.log -D
    # 启动beat
    celery beat -A celery_runner -f /var/log/celery.log --detach