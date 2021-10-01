import csv
from requests_html import HTMLSession


class ChainCheck:
    def __init__(self, urls_file, result='result.csv'):
        self.session = HTMLSession()
        self.urls_file = urls_file
        self.result = result

    def check_url(self, url):
        request = self.session.get(url)

        redirect_chain = list()
        for item in request.history:
            if 300 <= item.status_code < 400:
                redirect_chain.append(item.url)

        result = {'final_url': request.url, 'status': request.status_code, 'redirect_chain': redirect_chain}
        return result

    def worker(self):
        with open(self.urls_file, 'r', encoding='utf-8') as urls:
            result = dict()
            for line in urls:
                url = line.strip()
                result[url] = self.check_url(url)
        return result

    def writer(self):
        with open(self.result, 'w', encoding='utf-8', newline='') as f:
            header = ['REQUEST_URL', 'FINAL_URL', 'STATUS_CODE', 'LEN_CHAIN', 'CHAIN']
            my_csv = csv.writer(f, delimiter=';')
            my_csv.writerow(header)
            dict_to_write = self.worker()
            for key in dict_to_write.keys():
                row = [key, dict_to_write[key]['final_url'], dict_to_write[key]['status'],
                       len(dict_to_write[key]['redirect_chain']), dict_to_write[key]['redirect_chain']]
                my_csv.writerow(row)


if __name__ == "__main__":
    file = 'urls.txt'
    check_chain = ChainCheck(file)
    # chain = check_chain.worker()
    check_chain.writer()
    print('Done!')






