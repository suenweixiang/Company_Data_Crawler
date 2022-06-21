import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

ua = UserAgent()
headers = {'accept-language': 'en-US,en;q=0.9',
           'User-Agent': str(ua.chrome)}

zh = pd.read_csv('~/Desktop/brand_zh.csv')

for brand in zh.values[100:200]:
    if pd.isna(brand[1]) is False:
        name = brand[1]
        r = requests.get(
            f'https://www.twincn.com/Lq.aspx?q={name}', headers=headers)
        print('reg_brand:', name, f'< Response :{r.status_code} >')
        soup = BeautifulSoup(r.text, 'lxml')
        tb = soup.select('.table')[0]
        if len(tb.find_all('tr')) > 1:
            for i in tb.find_all('tr'):
                if i.find_all('td') != []:
                    id = i.find_all('td')[0].text
                    print('name:', name, "id:", id)
                    res = requests.get(
                        f'https://www.twincn.com/item.aspx?no={id}', headers=headers)
                    print('reg_brand:', name, 'tax_id:', id,
                          f'< Response :{res.status_code} >')
                    res_soup = BeautifulSoup(res.text, 'lxml')
                    phone = ''
                    company = ''
                    address = ''
                    content = []
                    company_list = []
                    try:
                        for s in res_soup.select('.table')[0].find_all('tr'):
                            if s.find('td').text == '公司名稱':
                                company = s.find_all('td')[1].text
                            if s.find('td').text == '公司所在地':
                                address = re.findall(
                                    '\S+', s.find_all('td')[1].text)[0]
                            if s.find('td').text == '電話':
                                phone = '-'.join(re.findall('\d+',
                                                            s.find_all('td')[1].text))
                            if s.find('td').text == '所營事業資料':
                                con = re.findall(
                                    '\S+', s.find_all('td')[1].text)
                                for i in con:
                                    if ''.join(re.findall(r'[\u4e00-\u9fa5]', i)) != '':
                                        content.append(
                                            ''.join(re.findall(r'[\u4e00-\u9fa5]', i)))
                        print(brand[0], brand[1], id, company,
                              phone, address, content)
                        company_list.append(
                            {
                                'brand': brand[0], 'brand_light': brand[1], 'company': company, 'id': id, 'tel': phone, 'address': address, 'content': content
                            })
                        pd.DataFrame(company_list).to_csv(
                            '~/Desktop/brand_list.csv', index=False, mode='a', header=False)
                        time.sleep(1)
                    except:
                        company_list.append(
                            {
                                'brand': brand[0], 'brand_light': brand[1], 'company': company, 'id': id, 'tel': phone, 'address': address, 'content': content
                            })
                        pd.DataFrame(company_list).to_csv(
                            '~/Desktop/brand_list.csv', index=False, mode='a', header=False)
                        time.sleep(1)

        else:
            company_list = []
            print(name)
            company_list.append(
                {
                    'brand': brand[0], 'brand_light': brand[1], 'company': '', 'id': '', 'tel': '', 'address': '', 'content': ''
                }
            )
            pd.DataFrame(company_list).to_csv(
                '~/Desktop/brand_list.csv', index=False, mode='a', header=False)
            time.sleep(1)
    else:
        company_list = []
        print(name)
        company_list.append(
            {
                'brand': brand[0], 'brand_light': brand[1], 'company': '', 'id': '', 'tel': '', 'address': '', 'content': ''
            }
        )
        pd.DataFrame(company_list).to_csv(
            '~/Desktop/brand_list.csv', index=False, mode='a', header=False)
        time.sleep(1)