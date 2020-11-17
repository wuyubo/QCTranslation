#!/usr/bin/env python
# -*- coding:utf-8 -*-
#############################
# @author: djming
# @email:dengjinming@cvte.com
#############################

import pymongo
import xlwt,xlrd

pyclient = None #pymongo客户端


def initclient(dbhost='localhost', dbport=27017):
    '''
    初始化客户端,必须在插入数据前进行
    这种方法只能连接默认数据库，如果需要进行登录认证，请还需再调用auth()
    '''
    global pyclient
    
    '''
    if not uname == '' and not pswd == '' and not db == '':
        conn_temp = "mongodb://%s:%s@%s/%s?authSource=%s"
        conn = conn_temp % (uname, pswd, dbhost, db, db)
        print conn
        pyclient = pymongo.MongoClient(conn)
    else:
    '''
    pyclient = pymongo.MongoClient(host=dbhost, port=dbport)

def auth(dbname, uname, pswd):
    '''
    登录认证以访问指定的加密db
    '''
    db = pyclient[dbname]
    db.authenticate(uname,pswd)


def insertdata(dbname, colname, data):
    '''
    插入数据，需要指定数据库名及表名
    in:
        dbname : 数据库名
        colname : 表名
        data : 字典格式的数据
    out:
        插入结果数据
    '''
    global pyclient
    db = pyclient[dbname]
    col = db[colname]
    return col.insert_one(data)

def find_one(dbname, colname, data):
    '''
    查询数据
    in:
        dbname : 数据库名
        colname : 表名
        data : 查询条件，字典
    out:
        查询到的第一个数据
    '''
    global pyclient
    db = pyclient[dbname]
    col = db[colname]
    return col.find_one(data)


def querydata(dbname, colname, data):
    '''
    查询数据
    in:
        dbname : 数据库名
        colname : 表名
        data : 查询条件，字典
    out:
        cursor，可当做表格获取数据
    '''
    global pyclient
    db = pyclient[dbname]
    col = db[colname]
    return col.find(data).sort('importVer', pymongo.DESCENDING)

if __name__ == '__main__':
    initclient('10.10.14.37',27017)
    #auth("property", "propertyAdmin", "property$12")
    auth("tsys", "tsysadmin", "smarttv2019")

    '''
    # 导出翻译库中重复数据的sample code

    # 记录所有的值
    all_values = {}

    terminal = 'CNPD'

    # 查询条件
    query_data = {
            'source':terminal
    }
    data = querydata('tsys', 'faepv', query_data)

    total = 0
    for d in data:
        en = d['en']
        zh = d['zh']
        lan = d['language']
        value = d['value']
        repeat = False
        if en not in all_values : all_values[en] = {}
        if zh not in all_values[en] : all_values[en][zh] = {}
        if lan not in all_values[en][zh] : all_values[en][zh][lan] = []
        for v in all_values[en][zh][lan]:
            if value == v['value']:
                repeat = True
                continue
        if not repeat:
            all_values[en][zh][lan].append(d)
            total = total + 1
            print("find %d data" % total, end='\r')
    print("find %d data" % total)

    wb = xlwt.Workbook(encoding='utf8')
    index = 0
    sheet = wb.add_sheet(str(index))

    sheet.write(0,0, '#English')
    sheet.write(0,1, '#Chinese')
    sheet.write(0,2, 'Language')
    sheet.write(0,3, 'Value')
    sheet.write(0,4, 'Id')

    current_row = 1
    current = 0

    for en, zhs in all_values.items():
        for zh, lans in zhs.items():
            for lan,values in lans.items():
                current = current + 1
                print('dedump data %d %d' % (current, total), end='\r')
                if len(values) < 2: continue
                for v in values:
                    sheet.write(current_row, 0, en)
                    sheet.write(current_row, 1, zh)
                    sheet.write(current_row, 2, lan)
                    sheet.write(current_row, 3, v['value'])
                    sheet.write(current_row, 4, v['key'])
                    current_row = current_row + 1
                # 写完一组重复后空出一行
                current_row = current_row + 1
                if current_row > 65500:
                    index = index + 1
                    sheet = wb.add_sheet(str(index))
                    sheet.write(0,0, '#English')
                    sheet.write(0,1, '#Chinese')
                    sheet.write(0,2, 'Language')
                    sheet.write(0,3, 'Value')
                    sheet.write(0,4, 'Id')
                    current_row = 1

    print('Completed')
    wb.save(terminal+'.xls') 
    print("Save to %s.xls" % terminal)
    '''

    '''
    # 插入language 的sample code
    total = len(lans)
    progress = 0
    for lan in lans:
        progress = progress + 1
        print progress,'/',total
        data = {
                'language':lan[0],
                'code':lan[1],
                'alias':lan[2:]
        }
        insertdata('tsys', "language", data)
    '''
    '''
    # 插入翻译价格的sample code
    while (True):
        language = raw_input("language:")
        price = int(raw_input("price:"))
        language = "#" + language
        data = {
                "language":language,
                "price":price
        }
        insertdata('property', 'price', data)
    '''
    '''
    # test sample code
    for lan in lans:
        if lan[0] == '_id' : continue
        data = {
                "language": lan[0],
                "code": lan[1]
        }
        print "insert", data
        insertdata('test', 'languages', data)
    '''
