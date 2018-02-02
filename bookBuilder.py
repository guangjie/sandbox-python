import bs4
import json
import os
import requests

DEV_MODE = False

def main():
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)

    if config["bookBuilder"] != '':
        common = config["bookBuilder"]["common"]
        env_dev = config["bookBuilder"]["dev"]
        env_prod = config["bookBuilder"]["prod"]


    URL = 'https://www.safaribooksonline.com/accounts/login'

    client = requests.session()
    client.get(URL)
    csrftoken = client.cookies["csrfsafari"]

    login_data = dict(email=common["username"], password1=common["password"], csrfmiddlewaretoken=csrftoken)

    client.post("https://www.safaribooksonline.com/accounts/login/", data=login_data, headers=dict(Referer=URL))
    next_page = 'https://www.safaribooksonline.com/library/view/art-of-computer/9780133488869/ch07.html'

    # while next_page != '':
    with open('art-of-computer-ch000.mhtml') as fin:
        text_string = fin.read()

    local_soup = bs4.BeautifulSoup(text_string, 'lxml')


    # r = client.get(next_page)
    # soup = bs4.BeautifulSoup(r.text, 'lxml')
    # link = soup.find(id='container').find(class_='t-sbo-next').find('a')
    with open('test.mhtml', 'w') as fout:
        fout.write(text_string)

        # if link:
        #     next_page = 'https://www.safaribooksonline.com' + link.attrs['href']
        # else:
        #     next_page = ''
        # print(next_page)

main()
