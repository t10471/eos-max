import requests
import csv
import shutil
from retry import retry


URL = 'https://eos.greymass.com'
CSV = 'output.csv'


def main():
    url = f'{URL}/v1/chain/get_block'
    shutil.rmtree(CSV, ignore_errors=True)
    with open(CSV, 'w', newline='') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['timestamp', 'transactions'])
        for i in range(1, 19498657):
        # for i in range(1, 10):
            res = request(url, i)
            r = res.json()
            writer.writerow([r['timestamp'], len(r['transactions'])])


@retry(tries=3, delay=2)
def request(url, i):
    return requests.post(url, json={'block_num_or_id': i})


if __name__ == '__main__':
    main()
