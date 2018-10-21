#!/usr/bin/env python3

import sys
import requests

def write_file(filename, response):
    with open(filename, 'wb') as outfile:
        outfile.write(response.content)

def clear_print(last_found, log):
    if not last_found:
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')
    print(log)

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def print_usage():
    print('Usage:')
    print('  python amex-scrape.py')
    print('    - default: request 300 sequential card images')
    print('  python amex-scrape.py [count]')
    print('    - count: number of sequential card images to request')

def main():
    headers = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    session = requests.session()
    last_found = True
    count_found = 0
    domain = 'aexp-static.com'
    if len(sys.argv) == 2:
        if is_number(sys.argv[1]):
            count_max = int(sys.argv[1])
        else:
            print_usage()
            return
    else:
        count_max = 300
    print(f'Searching for {count_max} cards on {domain}...')
    for i in range(0, count_max + 1):
        id = str(i).zfill(3)
        url = f'https://www.{domain}/online/myca/shared/summary/cardasset/images/NUS000000{id}_480x304_STRAIGHT_96.gif'
        filename = f'US{id}.gif'
        progress = f'({str(int(round(100 * i / count_max)))}% done)'
        response = session.get(url, headers=headers)
        if response.ok:
            clear_print(last_found, f'Found card. Writing file {filename}. {progress}')
            write_file(filename, response)
            last_found = True
            count_found += 1
        else:
            clear_print(last_found, f'No card for {filename} found. {progress}')
            last_found = False
    print(f'Found {count_found} total card images.')

main()
