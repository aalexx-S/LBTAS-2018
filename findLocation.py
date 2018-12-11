import argparse
import sys
import os
import sqlite3
from contextlib import closing
from types import SimpleNamespace
from collections import defaultdict
from bs4 import BeautifulSoup
import requests
import pandas

import getAllPush
import getLocationFromPush
import corToCity
from geolocationAPI import GeolocationAPIHandler

def main(argv):
    # parse argument
    argP = argparse.ArgumentParser(description="Input a web ptt url and the program will find all the replyer's location.")
    argP.add_argument('INPUT', help="The target web ptt url.")
    argP.add_argument('-k', '--keyfile', help='The file contains service name and the required informations')
    argP.add_argument('-db', '--database', help="IP2Location data base name.")
    argP.add_argument('-shp', '--shapefile', help="Taiwan administation area shapefile.")
    argP.add_argument('-qt', '--querytimes', help="Number of times of queries for each ip addresses. The result will be the average of all queries. Default to 1.")
    output_subP = argP.add_mutually_exclusive_group()
    output_subP.add_argument('-o', '--output', help="The output file name. Otherwise stdout.")
    output_subP.add_argument('-silent', action='store_true', help="No any output. Use this option when called by other program and just want to get the return value.")
    arg = argP.parse_args(argv)

    # config
    config = SimpleNamespace()
    config.stdout = sys.stdout
    config.stderr = sys.stderr
    if arg.output:
        config.stdout = open(arg.output, 'w')
    elif arg.silent:
        config.stdout = open(os.devnull, 'w')
        config.stderr = open(os.devnull, 'w')
    url = arg.INPUT
    config.keyfile = 'key.txt'
    if arg.keyfile:
        config.keyfile = arg.KEY_FILE
    config.threads = 4
    # cut .shp off shape file name
    config.shapefile = './shp/COUNTY_MOI_1070516'
    if arg.shapefile:
        config.shapefile = arg.shapefile[:arg.shapefile.rfind('.shp')]
    # separate filename and path
    config.shppath, config.shpname = os.path.split(config.shapefile)
    if config.shppath == '':
        config.shppath = '.'
    config.qt = 1
    if arg.querytimes:
        if arg.querytimes <= 0:
            print('[Error] Query times <= 0.', file=config.stderr)
            exit(1)
        config.qt = arg.querytimes

    ## read IP2Location database if present
    config.db_name = 'ipFindLocation.db'
    config.db_csv_table_name = ""
    db_conn = sqlite3.connect(config.db_name)
    if arg.database:
        config.db_csv_table_name = arg.database
        with closing(db_conn.cursor()) as cursor:
            # load CSV if not exist
            try:
                cursor.execute("SELECT * FROM `{0}`".format(config.db_csv_table_name))
            except sqlite3.OperationalError: # table not exist, load CSV
                print("[Log] Creating database from CSV file.", file=config.stderr)
                header = ['ip_from', 'ip_to', 'country_code', 'country_name', 'region_name', 'city_name', 'latitude', 'longitude']
                csv_r = pandas.read_csv(arg.database, names=header)
                csv_r.to_sql(config.db_csv_table_name, db_conn, if_exists='replace')
                db_conn.commit()

    # init geolocation handler
    GeolocationAPIHandler.config = config
    config.geoHandler = GeolocationAPIHandler(config.keyfile)

    # get the page
    print("[Log] Getting web page.", file=config.stderr)
    page = requests.get(url, cookies={'over18':'1'}) # bypass ask 18
    soup = BeautifulSoup(page.text.encode('utf-8'), features='html.parser')

    # get all push
    print("[Log] Parsing web page.", file=config.stderr)
    getAllPush.config = config
    poster = getAllPush.get_poster(soup)
    all_push, no_ip_counter = getAllPush.get_all_push(soup)
    print("[Log] {0} out of {1} pushes don't have ip information".format(no_ip_counter, no_ip_counter + len(all_push)), file=config.stderr)

    ## transfer to location
    # set environment
    config.quried_table_name = "quried_ip"
    getLocationFromPush.config = config
    # query
    print("[Log] Query poster.", file=config.stderr)
    result_poster = getLocationFromPush.get_location_from_push([poster])[0] # return in list
    print("[Log] Query pushes.", file=config.stderr)
    result_push = getLocationFromPush.get_location_from_push(all_push)

    # filter ips not in Taiwan
    foreign_push = []
    taiwan_push = []
    for push in result_push:
        if push['country_name'] != 'Taiwan':
            foreign_push.append(push)
        else:
            taiwan_push.append(push)


    ## map ip to cities
    print("[Log] Reading city shape from shapefile.", file=config.stderr)
    corToCity.config = config
    if result_poster['country_name'] == 'Taiwan': # if poster in Taiwan, find the city name
        taiwan_push.insert(0, result_poster)
    result_poster, *taiwan_push = corToCity.cor_to_city(taiwan_push) # cor_to_shape keeps input order

    # output data
    print("title = {0}".format(result_poster['title']))
    if result_poster['country_name'] != 'Taiwan':
        print("poster: {0}".format(result_poster['country_name']), file=config.stdout)
    else:
        print("poster: {0}".format(result_poster['city']), file=config.stdout)

    q = defaultdict(lambda: 0)
    for i in taiwan_push:
        q["{0}".format(i['city'])] += 1
    for a, b in q.items():
        print("{0}: {1}".format(a, b), file=config.stderr)

    w = defaultdict(lambda: [0, set()])
    w1 = {}
    w2 = {}
    for i in foreign_push:
        w["{0}".format(i['country_name'])][0] += 1
        w["{0}".format(i['country_name'])][1].add(i['id'])
    for a, b in w.items():
        print("{0}: {1} {2}".format(a, b[0], b[1]), file=config.stdout)
        w1[a] = b[0]
        w2[a] = b[1]

    # return data
    re = {'ip_record_ratio': 1 - (no_ip_counter/len(all_push)), 'poster': result_poster, 'foreign_push': foreign_push, 'taiwan_push': taiwan_push, 'taiwan_push_acc': q, 'foreign_push_acc': w1, 'foreign_push_id': w2}
    return re

if __name__ == '__main__':
    main(sys.argv[1:])
