import argparse
import sys
import os
import requests
from bs4 import BeautifulSoup

import getAllPush

def main(argv):
    # parse argument
    argP = argparse.ArgumentParser(description="Input a web ptt url and the program will mark all the ip of replies on a map, containing in a html file.")
    argP.add_argument('INPUT', help="The target web ptt url.")
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

    # get all push
    all_push = getAllPush.get_all_push(soup)

    print(all_push)

    sys.stdout = original_stdout

if __name__ == '__main__':
    main(sys.argv[1:])

