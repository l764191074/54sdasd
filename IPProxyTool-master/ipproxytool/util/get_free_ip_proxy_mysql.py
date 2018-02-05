#! /usr/bin/env python2
# coding=utf-8
import pymysql.cursors


def get_proxy():
    # Connect to the database
    connection = pymysql.connect(host='192.3.244.150',
                                 port=3306,
                                 user='ip_proxy_user',
                                 password='lc4771822',
                                 db='ip_proxy',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)

    # 执行sql语句
    try:
        with connection.cursor() as cursor:
            # 执行sql语句，进行查询
            sql = 'SELECT * FROM httpbin  ORDER BY id'
            cursor.execute(sql,)
            # 获取查询结果
            # print(result)

            return cursor._rows
        # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        connection.commit()

    finally:
        connection.close()


def insert_local():
    ip_list = get_proxy()
    connection_local = pymysql.connect(host='192.168.0.17',
                                 port=3306,
                                 user='root',
                                 password='l4771822',
                                 db='test',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection_local.cursor() as cursor:
            # 执行sql语句，进行查询
            sql = 'delete from free_ipproxy'
            cursor.execute(sql, )
            connection_local.commit()
            for it in ip_list:
                sql = u"INSERT IGNORE INTO free_ipproxy (id, save_time, ip, country, port, anonymity, https, speed, source, vali_count)VALUES(0, '{save_time}', '{ip}', '{country}', '{port}', '{anonymity}', '{https}', '{speed}', '{source}', 0)".format(**it)
                cursor.execute(sql,)
                connection_local.commit()

    finally:
        connection_local.close()

if __name__ == '__main__':
    insert_local()