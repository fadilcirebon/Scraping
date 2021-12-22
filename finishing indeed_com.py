# berikut adalah proses scraping contoh indeed.com
# berikut adalah lanjutan dari main.py, kita masuk ke finishing indeed.com dengan query yang lebih luas (all pages)

import os
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

url = 'https://www.indeed.com/jobs?'
site = 'https://www.indeed.com'
params = {
    'q':'python developer',
    'l' : 'new york'
}
headers = {'user-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

res = requests.get(url, params=params, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')

def get_total_pages(query, location): #mengganti parameter query dan location dari statis menjadi dinamis
    params = {
        'q': query,
        'l': location
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

def get_all_items(query,location,start,page): #mengambil semua data
    params = {
        'q': query,
        'l': location,
        'start': start   #penambahan parameter start untuk menambah query pagination
    }

    res = requests.get(url, params=params, headers=headers)

    with open('temp/res.html', 'w+') as outfile:
        outfile.write(res.text)
        outfile.close()
    soup = BeautifulSoup(res.text, 'html.parser')

    #definisi scraping
    contents = soup.find_all('table','jobCard_mainContent big6_visualChanges')


    jobs_list = []
    for item in contents:
        title = item.find('h2','jobTitle').text
        company = item.find('span','companyName')
        company_name = company.text #bagian ini penting karena jika tidak dilakukan parser.text di sini link tidak keluar.

        try:
            company_link = site + company.find('a')['href']
        except:
            company_link = 'Link is not available'


        #selanjutnya setelah semua terdefinisi, kita melakukan sorting data dan membuat dictionary (merapihkan)


        data_dict = {
             'title' : title,
              'company_name' : company_name,
              'company_link' : company_link
         }
        jobs_list.append(data_dict)

   #writing json file
    try:
        os.mkdir('json_result') #membuat file direktory dengan library os sebagai directory baru
    except FileExistsError:
        pass

    with open(f'json_result/{query}_in_{location}_page_{page}.json', 'w+') as json_data:
        json.dump(jobs_list, json_data)       #perhatikan fungsi json.dump tersebut, ada perbedaan dengan json.dumps
    print('Json Created')  #data akan tersimpan di folder json, baris ini sudah diexekusi sehingga di kasih #
    return jobs_list


    #writing csv files
    df = pd.DataFrame(dataframe)
    df.to_csv(f'data_result' / {filename}.csv, index=false)
    df.to_excel(f'data_result' / {filename}.xlsx, index=false)

def create_document (dataframe, filename): # membuat directory baru
    try:
        os.mkdir('data_result')
    except FileExistsError:
        pass


    print(f'File_{filename}.csv and {filename}.xlsx, successfully created')


def run():
    query = input('Enter your Job Query :')
    location = input('Enter your Location: ')

    total= get_total_pages(query,location)
    counter = 0
    final_result = []
    for page in range(total):
        page =+ 1
        counter =+ 10
        final_result += get_all_items(query, location, counter, page)

        #formatting data

    try:
        os.mkdir('reports')
    except FileExistsError:
        pass

    with open('reports/{}.json'.format(query), 'w+') as final_data:
        json.dump(final_result, final_data)

    print('Data Json has created')

    #create document
    create_document(final_result,query)



if __name__ == '__main__':
    run()