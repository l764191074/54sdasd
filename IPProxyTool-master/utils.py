#-*- coding: utf-8 -*-

import logging
import os
import re
import subprocess
import traceback
import time
import datetime


# 自定义的日志输出
def log(msg, level = logging.DEBUG):
    logging.log(level, msg)
    print('%s [%s], msg:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), level, msg))

    # if level == logging.WARNING or level == logging.ERROR:
    #     for line in traceback.format_stack():
    #         print(line.strip())

        # for line in traceback.format_stack():
        #     logging.log(level, line.strip())


# 服务器使用，清理端口占用
def kill_ports(ports):
    for port in ports:
        log('kill %s start' % port)
        popen = subprocess.Popen('lsof -i:%s' % port, shell = True, stdout = subprocess.PIPE)
        (data, err) = popen.communicate()
        log('data:\n%s  \nerr:\n%s' % (data, err))

        pattern = re.compile(r'\b\d+\b', re.S)
        pids = re.findall(pattern, data)

        log('pids:%s' % str(pids))

        for pid in pids:
            if pid != '' and pid != None:
                try:
                    log('pid:%s' % pid)
                    popen = subprocess.Popen('kill -9 %s' % pid, shell = True, stdout = subprocess.PIPE)
                    (data, err) = popen.communicate()
                    log('data:\n%s  \nerr:\n%s' % (data, err))
                except Exception, e:
                    log('kill_ports exception:%s' % e)

        log('kill %s finish' % port)

    time.sleep(1)


# 获取创建存储代理 ip 表的命令
def get_create_table_command(table_name):
    command = (
        "CREATE TABLE IF NOT EXISTS {} ("
        "`id` INT(8) NOT NULL AUTO_INCREMENT,"
        "`ip` CHAR(25) NOT NULL UNIQUE,"
        "`port` INT(4) NOT NULL,"
        "`country` TEXT DEFAULT NULL,"
        "`anonymity` INT(2) DEFAULT NULL,"
        "`https` CHAR(4) DEFAULT NULL ,"
        "`speed` FLOAT DEFAULT NULL,"
        "`source` CHAR(20) DEFAULT NULL,"
        "`save_time` TIMESTAMP NOT NULL,"
        "`vali_count` INT(5) DEFAULT 0,"
        "PRIMARY KEY(id)"
        ") ENGINE=InnoDB".format(table_name))

    return command


# 获取插入代理 ip 表的命令
def get_insert_data_command(table_name):
    if table_name == 'free_ipproxy':
        command = ("INSERT IGNORE INTO {} "
                   "(id, ip, port, country, anonymity, https, speed, source, save_time, vali_count)"
                   "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s)".format(table_name))
    else:
        command = ("INSERT IGNORE INTO {} "
                   "(id, ip, port, country, anonymity, https, speed, source, save_time, vali_count)"
                   "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(table_name))

    return command


# 获取删除指定 id 的命令
def get_delete_data_command(table_name, id):
    command = ("DELETE FROM {0} WHERE id={1}".format(table_name, id))

    return command


# 获取更新指定 id 的命令
def get_update_data_command(table_name, id, speed, vali_count = 0):
    command = (
        "UPDATE {table_name} SET speed={speed}, vali_count={vali_count} WHERE id={id}".
            format(table_name = table_name, speed = speed, id = id, vali_count = vali_count))

    return command


# 获取表的长度
def get_table_length(sql, table_name):
    try:
        command = ('SELECT COUNT(*) from {}'.format(table_name))
        sql.execute(command)
        (count,) = sql.cursor.fetchone()
        log('get_table_length results:%s' % str(count))
        return count
    except:
        return 0


def get_table_ids(sql, table_name):
    ids = []
    try:
        command = ('SELECT id from {}'.format(table_name))
        result = sql.query(command)
        ids = [item[0] for item in result]
    except:
        pass
    return ids


# 通过指定 id 得到代理信息
def get_proxy_info(sql, table_name, id):
    command = ("SELECT * FROM {0} WHERE id=\'{1}\'".format(table_name, id))
    result = sql.query_one(command)
    if result != None:
        if len(result) == 9:
            data = {
                'id': result[0],
                'ip': result[1],
                'port': result[2],
                'country': result[3],
                'anonymity': result[4],
                'https': result[5],
                'speed': result[6],
                'source': result[7],
                'save_time': result[8],
                'vali_count': 0,
            }
        else:
            data = {
                'id': result[0],
                'ip': result[1],
                'port': result[2],
                'country': result[3],
                'anonymity': result[4],
                'https': result[5],
                'speed': result[6],
                'source': result[7],
                'save_time': result[8],
                'vali_count': result[9],
            }
        return data
    return None


# 插入代理
def sql_insert_proxy(sql, table_name, proxy):
    command = get_insert_data_command(table_name)


    msg = (0, proxy.ip, proxy.port, proxy.country, proxy.anonymity, proxy.https, proxy.speed, proxy.source,
           proxy.vali_count)
    sql.insert_data(command, msg)


def get_vali_count(sql, table_name, id):
    command = "SELECT vali_count FROM {0} WHERE id='{1}'".format(table_name, id)
    res = sql.query_one(command)
    if res == None:
        return 0
    else:
        return res[0]


def make_dir(dir):
    log('make dir:%s' % dir)
    if not os.path.exists(dir):
        os.makedirs(dir)

