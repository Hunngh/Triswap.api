#!/usr/bin/env python
# -*- coding:utf-8 -*-

# file:__init__.py.py
# author:软件2202 曹凛然
# datetime:2024/12/29 14:51
# software: PyCharm

from app.database.database import Base, engine

def init_db():
    Base.metadata.create_all(bind=engine)
