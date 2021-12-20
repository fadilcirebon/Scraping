# berikut adalah proses scraping contoh indeed.com

import os
import requests
from bs4 import BeautifulSoup


url = 'https://www.indeed.com/jobs?'
params = {
    'q':'python developer',
    'l' : 'new york'
}
headers = {'user-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

res = requests.get(url, params=params, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')

def get_total_pages():
    params = {
        'q': 'python developer',
        'l': 'new york'
    }

    res = requests.get(url, params=params, headers=headers)

    try:
        os.mkdir('temp')
    except FileExistsError:
        pass

    with open('temp/res.html', 'w+') as outfile:
        outfile.write(res.text)
        outfile.close()

    #scraping steps:
    soup = BeautifulSoup(res.text, 'html.parser')
    print(soup.prettify())

if __name__ == '__main__':
    get_total_pages()
