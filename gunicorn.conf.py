# coding: utf-8

"""gunicorn配置参数"""

import gevent.monkey
import multiprocessing

gevent.monkey.patch_all()
_cpu = multiprocessing.cpu_count()
proc_name = 'django3template'  # 进程名

bind = ""  # 绑定的ip与端口
backlog = 2048  # 监听队列数量，64-2048
worker_class = 'gevent'  # 使用gevent模式，还可以使用sync 模式，默认的是sync模式
workers = _cpu * 2 + 1  # 进程数
threads = _cpu * 4  # 指定每个进程开启的线程数
worker_connections = 2000
loglevel = 'info'  # 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'

accesslog = f"/var/log/gunicorn_{proc_name}_access.log"  # 访问日志文件
errorlog = f"/var/log/gunicorn_{proc_name}_error.log"  # 错误日志文件

daemon = True
