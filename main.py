# berikut adalah proses scraping contoh indeed.com

import os
import requests
from bs4 import BeautifulSoup


url = 'https://www.indeed.com/jobs?'
site = 'https://www.indeed.com'
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
        os.mkdir('temp') #membuat file direktory dengan library os
    except FileExistsError:
        pass

    with open('temp/res.html', 'w+') as outfile:
        outfile.write(res.text)
        outfile.close()

    total_pages = []

    #scraping steps: mengambil semua pagination
    soup = BeautifulSoup(res.text, 'html.parser')
    pagination = soup.find('ul','pagination-list')
    pages = pagination.find_all('li')
    for page in pages:
        total_pages.append(page.text)

    total = int(max(total_pages))
    return total

def get_all_items(): #mengambil semua data
    params = {
        'q': 'python developer',
        'l': 'new york'
    }
    #definisikan parsernya dulu sebagai berikut:
    res = requests.get(url, params=params, headers=headers)

    with open('temp/res.html', 'w+') as outfile:
        outfile.write(res.text)
        outfile.close()
    soup = BeautifulSoup(res.text, 'html.parser')

    #definisi scraping
    contents = soup.find_all('table','jobCard_mainContent big6_visualChanges')

    #selanjutnya mengambil item sebagai berikut:
    # *title
    # * company name
    # * company link
    # * company address

    for item in contents:
        title = item.find('h2','jobTitle').text
        company = item.find('span','companyName')
        company_name = company.text #bagian ini penting karena jika tidak dilakukan parser.text di sini link tidak keluar.

        try:
            company_link = site + company.find('a')['href']
        except:
            company_link = 'Link is not available'
        print(company_link)

        #selanjutnya setelah semua terdefinisi, kita melakukan sorting data dan membuat dictionary (merapihkan)

if __name__ == '__main__':
    get_all_items()
