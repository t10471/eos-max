import os
import requests
import csv
from retry import retry

GET = 'get'
POST = 'post'

URLS = [{'method': POST, 'url': 'https://eos.greymass.com/v1/chain/get_block'},
        {'method': POST, 'url': 'http://bp.cryptolions.io:8888//v1/chain/get_block'},
        {'method': GET, 'url': 'https://eosweb.net/api/v1/get_block/{}'},
        ]

CSV = 'output.csv'
START = 1
END = 19498657

def main():
    start = START
    if os.path.exists(CSV):
        start = read_csv()
    with open(CSV, 'a', newline='') as f:
        writer = csv.writer(f, lineterminator='\n')
        if not os.path.exists(CSV):
            writer.writerow(['timestamp', 'transactions'])
        i = start
        print(f'start block number {i}')
        while i <= END:
            for u in URLS:
                res = request(u, i)
                r = res.json()
                print('{} {} {}'.format(i, r['timestamp'], len(r['transactions'])))
                writer.writerow([r['timestamp'], len(r['transactions'])])
                i += 1
                f.flush()


def read_csv():
    i = START - 1
    with open(CSV, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            i += 1
    return i

@retry(tries=3, delay=2)
def request(u, i):
    if u['method'] == GET:
        return requests.get(u['url'].format(i))
    else:
        return requests.post(u['url'], json={'block_num_or_id': i})

if __name__ == '__main__':
    main()
