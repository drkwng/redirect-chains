import csv
from concurrent.futures import ThreadPoolExecutor
from requests_html import HTMLSession


class ChainCheck:
    def __init__(self, _urls, result_file='result.csv'):
        self.session = HTMLSession()
        self.urls = urls
        self.result_file = result_file

    def check_url(self, url):
        request = self.session.get(url)
        redirect_chain = list()
        for item in request.history:
            if 300 <= item.status_code < 400:
                redirect_chain.append(item.url)

        result = {'request_url': url, 'final_url': request.url,
                  'status': request.status_code, 'redirect_chain': redirect_chain}
        return result

    def worker(self):
        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for item in executor.map(self.check_url, self.urls):
                results.append(item)
        return results

    def main(self):
        with open(self.result_file, 'w', encoding='utf-8', newline='') as res:
            header = ['REQUEST_URL', 'FINAL_URL', 'STATUS_CODE', 'LEN_CHAIN', 'CHAIN']
            my_csv = csv.writer(res, delimiter=';')
            my_csv.writerow(header)
            res_data = self.worker()
            for elem in res_data:
                row = [elem['request_url'], elem['final_url'], elem['status'],
                       len(elem['redirect_chain']), elem['redirect_chain']]
                my_csv.writerow(row)


if __name__ == "__main__":
    try:
        file = input('Please enter the urls list filename and press Enter: \n')
        urls = []
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                urls.append(line.strip())
        print('Program started. Please wait...')
        check_chain = ChainCheck(urls)
        check_chain.main()
        print('Done! Check the result.csv file')

    except Exception as e:
        print(e, type(e))






