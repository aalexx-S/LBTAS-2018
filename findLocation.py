import argparse
import sys
import os
import requests
import sqlite3
import pandas
from contextlib import closing
from bs4 import BeautifulSoup
from types import SimpleNamespace

import getAllPush
import getLocationFromPush

def main(argv):
    # parse argument
    argP = argparse.ArgumentParser(description="Input a web ptt url and the program will mark all the ip of replies on a map, containing in a html file.")
    argP.add_argument('INPUT', help="The target web ptt url.")
    argP.add_argument('-db', '--database', help="IP2Location data base name.")
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
                print("[Log] Creating database from CSV file.", file = config.stderr)
                header = ['ip_from', 'ip_to', 'country_code', 'country_name', 'region_name', 'city_name', 'latitude', 'longitude']
                csv_r = pandas.read_csv(arg.database, names = header)
                csv_r.to_sql(config.db_csv_table_name, db_conn, if_exists = 'replace')
                db_conn.commit()

    # get the page
    print("[Log] Getting web page.", file = config.stderr)
    page = requests.get(url, cookies={'over18':'1'}) # bypass ask 18
    soup = BeautifulSoup(page.text.encode('utf-8'), features = 'html.parser')

    # get all push
    print("[Log] Parsing web page.", file = config.stderr)
    poster = getAllPush.get_poster(soup)
    all_push = getAllPush.get_all_push(soup)

    # transfer to location
    # set environment
    config.quried_table_name = "quried_ip"
    getLocationFromPush.config = config
    # query
    result_poster = getLocationFromPush.get_location_from_push([poster])
    result_push = getLocationFromPush.get_location_from_push(all_push)

    # call map api

if __name__ == '__main__':
    main(sys.argv[1:])

