import copy
import sys
import sqlite3
import geolocationAPIHandler
from contextlib import closing

config = None

def get_location_from_push (all_push):
    global db_conn
    db_conn = sqlite3.connect(config.db_name)
    db_conn.row_factory = sqlite3.Row
    # create quried ip table in db if not exist
    with closing(db_conn.cursor()) as cursor:
        cursor.execute('''CREATE TABLE IF NOT EXISTS `{0}`(
                `ip` UNSIGNED INT(10),
                `country_name` VARCHAR(64),
                `region_name` VARCHAR(128),
                `city_name` VARCHAR(128),
                `latitude` DOUBLE,
                `longitude` DOUBLE
                );'''.format(config.quried_table_name))
        db_conn.commit()

    result = []
    i = 1
    for push in all_push:
        # progress
        nod_p = i / len(all_push)
        nop = int(40 * nod_p)
        print("[Log] [" + '-' * nop + ' ' * (40 - nop) + "] {2:.2f}%".format(i, len(all_push), nod_p * 100), end = "\r", file = config.stderr)
        i += 1
        # process ip
        tmp = copy.deepcopy(push)
        ip = tmp['ip']
        res = _get_location(ip)
        tmp['country_name'] = res['country_name']
        # Taiwan is Taiwan !!
        if tmp['country_name'] == 'Taiwan, Province of China':
            tmp['country_name'] = 'Taiwan'
        tmp['region_name'] = res['region_name']
        tmp['city_name'] = res['city_name']
        tmp['longitude'] = res['longitude']
        tmp['latitude'] = res['latitude']
        result.append(tmp)
    print('') # to keep progress bar
    db_conn.commit()
    db_conn.close()
    return result

def _get_location(ip):
    # if quried, return
    with closing(db_conn.cursor()) as cursor:
        cursor.execute("SELECT * FROM `{0}` WHERE ip = {1}".format(config.quried_table_name, _ip_to_int10(ip)))
        res = cursor.fetchall()
        if len(res) > 1: # this really shouldn't happen
            print("[Warning] Multiple result with same ip in database for ip {0} ({1}). Use the first one".format(ip, _ip_to_int10(ip)), file = config.stderr)
        if len(res) >= 1: # already quried
            return res[0]
        # not quried, call API
        # if ip2location db present, query that first
        res = _ip2location_db_check(ip)
        if res == None: # not present, call API
            res = geolocationAPIHandler.geolocation_API_handler(ip)
        elif res['country_code'] == 'TW': # call api for more accurate result
            api_r = geolocationAPIHandler.geolocation_API_handler(ip)
            #TODO
        # put in db
        if res['longitude'] != float('inf') and res['latitude'] != float('inf'):
            cursor.execute("INSERT INTO {0} VALUES (?,?,?,?,?,?)".format(config.quried_table_name), (_ip_to_int10(ip), res['country_name'], res['region_name'], res['city_name'], res['longitude'], res['latitude']))
        else:
            print("[Warning] Invalide longitude or latitude.", file = config.stderr)
        return res

def _ip2location_db_check (ip):
    if config.db_csv_table_name == "": # ip2location csv database isn't available
        return None

    # query ip
    ip_int10 = _ip_to_int10(ip)
    with closing(db_conn.cursor()) as cursor:
        cursor.execute("SELECT * FROM `{0}` WHERE ip_from <= {1} AND ip_to >= {2};".format(config.db_csv_table_name, ip_int10, ip_int10))
        res = cursor.fetchall()
        if len(res) > 1: # this really shouldn't happen
            print("[Warning] Multiple result with same ip segment in ip2location CSV database for ip {0} ({1}).".format(ip, _ip_to_int10(ip)), file = config.stderr)
        if len(res) >= 1:
            return res[0]

    return None # not found

def _ip_to_int10(ip):
    token = ip.split('.')
    return int(token[0]) * 16777216 + int(token[1]) * 65536 + int(token[2]) * 256 + int(token[3])
