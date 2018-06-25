# -*- coding:utf-8 -*-

import os
import re
import urllib
import json
import socket
import urllib.request
import urllib.parse
import urllib.error

import sys
import time

timeout = 5
socket.setdefaulttimeout(timeout)


class Crawler:
    """
    get images by keywords from Baidu website
    """
    __time_sleep = 0.1
    __amount = 0
    __start_amount = 0
    __counter = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    url = 'http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word={}&cg=girl&pn={}&rn=60&itg=0&z=0&fr=&width=&height=&lm=-1&ic=0&s=0&st=-1&gsm=1e0000001e'

    def __init__(self, t=0.1):
        self.time_sleep = t

    def get_suffix(self, name):
        m = re.search(r'\.[^\.]*$', name)
        if m.group(0) and len(m.group(0)) <= 5:
            return m.group(0)
        else:
            return '.jpeg'


    def get_referrer(self, url):
        par = urllib.parse.urlparse(url)
        if par.scheme:
            return par.scheme + '://' + par.netloc
        else:
            return par.netloc

    def save_image(self, rsp_data, word):
        """
        save image to disk
        """
        if not os.path.exists(word):
            os.mkdir(word)

        self.__counter = len(os.listdir(word)) + 1
        for image_info in rsp_data['imgs']:

            try:
                time.sleep(self.time_sleep)
                suffix = self.get_suffix(image_info['objURL'])

                refer = self.get_referrer(image_info['objURL'])
                opener = urllib.request.build_opener()
                opener.addheaders = [
                    ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'),
                    ('Referer', refer)
                ]
                urllib.request.install_opener(opener)

                urllib.request.urlretrieve(image_info['objURL'], word + '/' + str(self.__counter) + str(suffix))
            except urllib.error.HTTPError as urllib_err:
                print(urllib_err)
                continue
            except Exception as err:
                time.sleep(1)
                print(err)
                print("unexcept error, ignore...")
                continue
            else:
                print(word + " + 1, total: " + str(self.__counter) + " " + word)
                self.__counter += 1
        return


    def get_images(self, word='三轮车'):
        search = urllib.parse.quote(word)
        
        pn = self.__start_amount
        while pn < self.__amount:
            target = self.url.format(search, pn)
            try:
                time.sleep(self.time_sleep)
                req = urllib.request.Request(url=target, headers=self.headers)
                n_page = urllib.request.urlopen(req)
                rsp = n_page.read().decode('unicode_escape')
            except UnicodeDecodeError as e:
                print(e)
                print('-----UnicodeDecodeErrorurl:', target)
            except urllib.error.URLError as e:
                print(e)
                print("-----urlErrorurl:", target)
            except socket.timeout as e:
                print(e)
                print("-----socket timout:", target)
            else:
                rsp_data = json.loads(rsp)
                self.save_image(rsp_data, word)

                print("next page")
                pn += 60
            finally:
                n_page.close()
        print("finish!")
        return

    def start(self, word, spider_page_num=1, start_page=1):
        """
        start fetch images
        """
        self.__start_amount = (start_page - 1) * 60
        self.__amount = spider_page_num * 60 + self.__start_amount
        self.get_images(word)


# entry for this script
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("invalid parameters! usage ==> python image_get.py [keywords] [total pages] [start index from 1]")
    else:
        keywords = sys.argv[1]
        total = sys.argv[2]
        start = sys.argv[3]

        crawler = Crawler(0.05)  
        crawler.start(keywords, int(total), int(start))