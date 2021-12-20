# berikut adalah proses scraping contoh indeed.com

import os
import requests
from bs4 import BeautifulSoup
import json

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

    jobs_list = [] #membuat variabel untuk append di bawah nanti
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

        #hasilnya akan keluar sudah tersusun seperti list dictionary di atas


        #jika mau append dalam satu baris data, bisa menggunakan fungsi append, contoh kita buat dulu variable 'joblist' lalu tuliskan perintah appendnya


        jobs_list.append(data_dict)


    #print(jobs_list) #jika perintah print di luar indentasi loop, maka akan diprint dalam satu list
    #print(len(jobs_list)) # untuk mengetahui jumlah data dalam satu list tersebut
    #print('jumlah datanya adalah sebanyak',len(jobs_list),'buah') bisa juga dengan perintah ini, supaya ada penambahan text
    #print(f'jumlah data: {len(jobs_list)}') perintah ini juga bisa digunakan, hasilnya nanti "jumlah data : 15"

    #lanjut mengolah hasil data menjadi sebuah json file, import library json dulu di awal coding (import json)
    #writing json file

    try:
        os.mkdir('json_result') #membuat file direktory dengan library os sebagai directory baru
    except FileExistsError:
        pass

    with open('json_result/job_list.json', 'w+') as json_data:
        json.dump(jobs_list, json_data)       #perhatikan fungsi json.dump tersebut, ada perbedaan dengan json.dumps

    print('Json Created')  #data akan tersimpan di folder json


if __name__ == '__main__':
    get_all_items()
