# -*- coding: utf-8 -*-
import os
class MainConfig(object):
    SECRET_KEY = "c61f1f9e762e16831f676528b89b31d"
    SQL_HOST='192.168.2.222'
    USER='root'
    DB='cdms'
    CHARSET='utf8'



class TestDev():
    pass


class CidaoDev(object):
    SECRET_KEY = "c61f1f9e762e16831f676528b89b31d"
    SQL_HOST='127.0.0.1'
    USER='root'
    DB='cdms'
    CHARSET='utf8'
    UPLOAD_PATH=os.getenv('UPLOAD_PATH')





config = {
    'MainConfig': MainConfig,
    'TestDec':TestDev,
    'CidaoDev':CidaoDev
}