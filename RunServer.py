#!/usr/bin/python
# -*- coding: utf-8 -*-
# Created by bayonet on 16-3-9.

from app import app


app.debug = True

if __name__ == '__main__':
    app.run("127.0.0.1")