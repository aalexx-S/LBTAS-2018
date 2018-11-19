import argparse
import sys
import os
import requests
import sqlite3
import pandas
import partial
from contextlib import closing
from bs4 import BeautifulSoup

import getAllPush

def main(argv):
    # parse argument
    argP = argparse.ArgumentParser(description="Input a web ptt url and the program will mark all the ip of replies on a map, containing in a html file.")
    argP.add_argument('INPUT', help="The target web ptt url.")
    argP.add_argument('-db', '--database', help="IP2Location data base name.")
    output_subP = argP.add_mutually_exclusive_group()
    output_subP.add_argument('-o', '--output', help="The output file name. Otherwise stdout.")
    output_subP.add_argument('-silent', action='store_true', help="No any output. Use this option when called by other program and just want to get the return value.")
    arg = argP.parse_args(argv)

    original_stdout = sys.stdout # for restore stdout
    if arg.output:
        sys.stdout = open(arg.output, 'w')
    elif arg.silent:
        sys.stdout = open(os.devnull, 'w')
    url = arg.INPUT

    # get the page
    # bypass ask 18
    page = requests.get(url, cookies={'over18':'1'})
    soup = BeautifulSoup(page.text.encode('utf-8'), features = 'html.parser')

    ## read IP2Location database if present
    db_con = None
    if arg.database:
        db_con = sqlite3.connect(arg.database + '.db')
        with closing(db_con.cursor()) as cursor:
            # load CSV if not exist
            try:
                cursor.execute("SELECT * FROM ip2location_db")
            except sqlite3.OperationalError: # table not exist, load CSV
                print("Creating database from CSV file", file = sys.stderr)
                cursor.execute('''CREATE TABLE `ip2location_db`(
                        `ip_from` UNSIGNED INT(10),
                        `ip_to` UNSIGNED INT(10),
                        `country_code` CHAR(2),
                        `country_name` VARCHAR(64),
                        `region_name` VARCHAR(128),
                        `city_name` VARCHAR(128),
                        `latitude` DOUBLE,
                        `longitude` DOUBLE
                        );''')
                csv_r = pandas.read_csv(arg.database)
                csv_r.to_sql('ip2location_db', db_con, if_exists = 'replace')
                db_con.commit()

    # get all push
    all_push = getAllPush.get_all_push(soup)

    print(all_push)
    
    # restore stdout    
    sys.stdout = original_stdout

if __name__ == '__main__':
    main(sys.argv[1:])

