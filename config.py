# -*- coding: utf-8



class MainConfig(object):
    SECRET_KEY = "c61f1f9e762e16831f676528b89b31d"
    HOST='192.168.2.222'
    USER='root'
    DB='cdms'
    CHARSET='utf8'

class TestDev(object):
    SECRET_KEY = "c61f1f9e762e16831f676528b89b31d"
    HOST='127.0.0.1'
    USER='root'
    DB='cdms'
    CHARSET='utf8'



config = {
    'MainConfig': MainConfig,
    'TestDec':TestDev
}