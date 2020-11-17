#! /usr/bin/python
# -*- coding:utf-8 -*-

import sys
import xlrd
import xlwt
from tool import mongoutils

COLS = ["CVTE", "newoldtran", "cnpd", "faepv", "hisense", "TCL", "caixun"]
MAX_LEVEL = len(COLS) - 1
DB_NAME="tsys"
mongoutils.initclient("10.10.14.37")
mongoutils.auth(DB_NAME, "tsysr","cvte2019")



def find_from_db(querybody, db=0):
    if db > MAX_LEVEL:
        return ""
    col = COLS[db]
    trans = mongoutils.querydata(DB_NAME, col, querybody)
    for tran in trans:
        value =  tran['value']
        value = value.strip() if isinstance(value, str) else value
        return value
    return ""
    #return find_from_db(querybody, level+1)


def query(en, zh, language, db=0):
	value = find_from_db({'en':en,'zh':zh,'language':language}, db)
	return value if value != "" else find_from_db({'en':en,'language':language}, db)




