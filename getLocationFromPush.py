import copy
import sqlite3
from contextlib import closing
from collections import defaultdict
from multiprocessing.dummy import Pool as ThreadPool

config = None

def get_location_from_push(all_push):
    db_conn = sqlite3.connect(config.db_name)
    db_conn.row_factory = sqlite3.Row
    # create quried ip table in db if not exist
    with closing(db_conn.cursor()) as cursor:
        cursor.execute('''CREATE TABLE IF NOT EXISTS `{0}`(
                `ip` VARCHAR(16),
                `ip_int` UNSIGNED INT(10),
                `country_name` VARCHAR(64),
                `latitude` DOUBLE,
                `longitude` DOUBLE
                );'''.format(config.quried_table_name))
        db_conn.commit()

    # make all the requests ip list
    query_ip_list = []
    ip_to_pushes_map = defaultdict(list) # an ip can make multiple pushes
    for push in all_push:
        query_ip_list.append(push['ip'])
        ip_to_pushes_map[push['ip']].append(push)
    query_ip_list = list(set(query_ip_list))

    # multi-thread look up
    pool = ThreadPool(config.threads)
    re = pool.imap(_get_location, query_ip_list)
    i = 1 # progress bar
    result = []
    for r in re:
        # progress
        nod_p = i / len(query_ip_list)
        nop = int(40 * nod_p)
        print("[Log] Progress: [" + '-' * nop + ' ' * (40 - nop) + "] {0} out of {1} ip queried.".format(i, len(query_ip_list)), end="\r", file=config.stderr)
        i += 1
        # process return
        ip = r['ip']
        for push in ip_to_pushes_map[ip]:
            tmp = copy.deepcopy(push)
            tmp['country_name'] = r['country_name']
            tmp['longitude'] = r['longitude']
            tmp['latitude'] = r['latitude']
            result.append(tmp)
    print('', file=config.stderr) # to keep progress bar after finish
    db_conn.commit()
    db_conn.close()
    return result

# Thread entry point
def _get_location(ip):
    # if quried, return
    db_conn = sqlite3.connect(config.db_name)
    db_conn.row_factory = sqlite3.Row
    with closing(db_conn.cursor()) as cursor:
        # check if queried
        cursor.execute("SELECT * FROM `{0}` WHERE `ip_int` = {1}".format(config.quried_table_name, _ip_to_int10(ip)))
        res = cursor.fetchall()
        if len(res) > 1: # this really shouldn't happen
            print("[Warning] Multiple result with same ip in database for ip {0} ({1}). Use the first one".format(ip, _ip_to_int10(ip)), file=config.stderr)
        if len(res) >= 1: # already quried
            return res[0]

        # not quried, call API
        # if ip2location db present, query that first
        res = _ip2location_db_check(db_conn, ip)
        if res is None or res['country_code'] == 'TW': # not present, or need accurate result, call API
            res = config.geoHandler.request(ip)

        # Taiwan is Taiwan !!
        # IP2Location
        if res is not None and res['country_name'] == 'Taiwan, Province of China':
            res['country_name'] = 'Taiwan'

        # put in db
        if res is not None and res['longitude'] != float('inf') and res['latitude'] != float('inf'):
            cursor.execute("INSERT INTO `{0}` VALUES (?,?,?,?,?)".format(config.quried_table_name), (ip, _ip_to_int10(ip), res['country_name'], res['latitude'], res['longitude']))
        else:
            #print("[Warning] Invalide API request return. None or longitude or latitude error.", file = config.stderr)
            pass
    return res

def _ip2location_db_check(db_conn, ip):
    if config.db_csv_table_name == "": # ip2location csv database isn't available
        return None
    # query ip
    ip_int10 = _ip_to_int10(ip)
    with closing(db_conn.cursor()) as cursor:
        cursor.execute("SELECT * FROM `{0}` WHERE ip_from <= {int10} AND ip_to >= {int10};".format(config.db_csv_table_name, int10=ip_int10))
        res = cursor.fetchall()
        if len(res) > 1: # this really shouldn't happen
            print("[Warning] Multiple result with same ip segment in ip2location CSV database for ip {0} ({1}).".format(ip, _ip_to_int10(ip)), file=config.stderr)
        if len(res) >= 1:
            re = {}
            for i in res[0].keys():
                re[i] = res[0][i]
            re['ip'] = ip
            return re

    return None # not found

def _ip_to_int10(ip):
    token = ip.split('.')
    return int(token[0]) * 16777216 + int(token[1]) * 65536 + int(token[2]) * 256 + int(token[3])

def _int10_to_ip(ip):
    a = int(ip / 16777216)
    t = ip % 16777216
    b = int(t / 65536)
    t %= 65536
    c = int(t / 256)
    t %= 256
    return "{0}.{1}.{2}.{3}".format(a, b, c, t)
