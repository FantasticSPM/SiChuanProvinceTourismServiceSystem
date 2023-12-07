import pymysql

"""
运行项目时发生错误：mysqlclient 1.4.3 or newer is required; you have %s." % Database.__version__
解决方法之一：
    将python安装路径下“\Lib\site-packages\django\db\\backends\mysql”的base.py文件中：
            if version < (1, 4, 3):
                raise ImproperlyConfigured(
                    "mysqlclient 1.4.3 or newer is required; you have %s." % Database.__version__
                )
    注释掉。
解决方法二：在django项目文件中init.py文件加入下面的代码。
"""
pymysql.version_info = (1, 4, 6, 'final', 0)
