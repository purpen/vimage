# -*- coding: utf-8 -*-

import os
import gevent.monkey
import multiprocessing

gevent.monkey.patch_all()

# 监听本机的8080端口
bind = '127.0.0.1:8080'

preload_app = True

# 启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1

# 每个进程的开启线程
threads = multiprocessing.cpu_count() * 2

backlog = 2048

# worker_connections - The maximum number of simultaneous clients
# This setting only affects the Eventlet and Gevent worker types.
worker_connections = 1001

# max_requests - The maximum number of requests a worker will process
# before restarting
# Any value greater than zero will limit the number of requests a work
# will process before automatically restarting. This is a simple method
# to help limit the damage of memory leaks.
max_requests = 2048

# keep_alive - The number of seconds to wait for requests on a
# Keep-Alive connection
# Generally set in the 1-5 seconds range.
keepalive = 2

# 工作模式为gevent
workers_class = 'gunicorn.workers.ggevent.GeventWorker'

debug = False

# 如果不使用supervisord之类的进程管理工具可以是进程成为守护进程，否则会出问题
# INFO exited: gunicorn (exit status 0; not expected)
daemon = False

# 进程名称
proc_name = 'gunicorn.pid'
# 进程pid记录文件
pidfile = '/var/run/vimage/gunicorn.pid'


loglevel = 'debug'

logfile = '/var/log/vimage/aim.log'
accesslog = '/var/log/vimage/aim-access.log'
access_log_format = '%(h)s %(t)s %(U)s %(q)s'
errorlog = '/var/log/vimage/aim-error.log'


x_forwarded_for_header = 'X-FORWARDED-FOR'
