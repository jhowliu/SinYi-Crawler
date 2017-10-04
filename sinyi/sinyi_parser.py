# -*- coding: utf-8 -*-
import os
import re
import random
import requests

from glob import glob
from bs4 import BeautifulSoup

from lib.utils import find_by_css

from lib.super_parser import SuperParser
from lib.super_parser import punctuation_cleaner

class SuperParserSinYi(SuperParser):

    def init(self):
        self.casefrom = 'SinYi'
        self.result = []
        self.rent_or_sale = u'出售'

    def start(self):
        file_list = glob('/home/lingtelli/house/parser/parser/data/html/*') # create by crawler
        #random.shuffle(file_list)
        for file_ in file_list[:5]:
            with open(file_) as f:
                self.html = f.read()

            self.url  = 'http://buy.sinyi.com.tw/house/' + os.path.basename(file_)
            self.soup = BeautifulSoup(self.html, 'html.parser')
            self.id_ = '-'.join(['sinyi', self.get_case_number(), self.date])
            obj = self.fill_data_into_schema()
            self.result.append(obj)

    def get_host_name(self):
        match = find_by_css(self.soup, '.name-sinyi')

        name = match[0].text if match else ""
        name = punctuation_cleaner.sub('', name)

        return name

    def get_host_phonenumber(self):
        match = find_by_css(self.soup, '.phone')

        phone = match[0].text if match else ""
        phone = punctuation_cleaner.sub('', phone)

        return phone

    def get_host_role(self):
        return u"代理人"

    def get_host_mail(self):
        mail_pattern = re.compile(r'([\w.]+@[\w]+\.[a-zA-Z]{2,4}\.?[a-zA-Z]{0,4})')
        return ""

    def get_host_company(self):
        return self.get_host_name()

    def get_community(self):
        return ""

    def get_price(self):
        unit = u"萬"

        match = find_by_css(self.soup, '.price')
        price = punctuation_cleaner.sub('', match[0].text) if match else 0.0
        price = float(price)

        return price, unit

    def get_price_per_pings(self):
        unit = u"萬/坪"
        match = find_by_css(self.soup, '#obj-info ul li')

        price = match[2].text if match and len(match)>2 else ""
        price = punctuation_cleaner.sub('', price)
        find = re.search(u'每坪單價：([\d.]+)', price)

        price = find.group(1) if find else 0.0

        return price, unit

    def get_separating_address(self, address):
        match = find_by_css(self.soup, '#content-main .tag_list')

        city = match[1].span.text if match else ""

        district = match[2].span.text if match else ""
        district = district.replace(city, '')

        road = address.replace(city, '').replace(district, '')

        return city, district, road

    def get_case_name(self):
        match = find_by_css(self.soup, '#content-main h2')

        case_name = match[0].text if match else ""
        case_name = punctuation_cleaner.sub('', case_name)

        return case_name

    # 物件編號
    def get_case_number(self):
        case_name = self.get_case_name()
        find = re.search('([a-zA-Z0-9]+)$', case_name)

        return find.group(1) if find else ""

    # 地址
    def get_address(self):
        match = find_by_css(self.soup, '#content-main h1')

        address = match[0].text if match else ""
        address = punctuation_cleaner.sub('', address)

        return address

    # 車位
    def get_parking_space(self):
        match = find_by_css(self.soup, '.house_info tr')

        parking = match[7].text if match and len(match)>7 else ""
        parking = punctuation_cleaner.sub('', parking)
        find = re.search(u'車位(\w+)', parking)

        return find.group(1) if find else ""

    # 建坪
    def get_building_pings(self):
        match = find_by_css(self.soup, '#obj-info ul li')

        building = punctuation_cleaner.sub('', match[1].text) if match else ""
        find = re.search(u'建物登記：([0-9.]+)坪', building)

        return find.group(1) if find else "0"

    # 地坪
    def get_floor_pings(self):
        match = find_by_css(self.soup, '#obj-info ul li')

        floor = match[5].text if match and len(match)>5 else ""
        find = re.search(u'土地登記：([0-9.])+坪', floor.replace(u'\xa0', ''))

        return find.group(1) if find else "0"

    # 主建物坪數
    def get_main_building_pings(self):
        match = find_by_css(self.soup, '#obj-info ul li')

        main = match[5].text if match and len(match)>5 else ""
        find = re.search('主建物：([0-9.]+)坪', main.replace(u'\xa0', ''))

        return find.group(1) if find else "0"

    # 附屬建物坪數
    def get_attached_building_pings(self):
        return u"0"

    # 公設
    def get_public_utilities_pings(self):
        match = find_by_css(self.soup, '.house_info tr')

        public = match[5].text if match and len(match)>5 else ""
        find = re.search(u'公共設施([0-9.]+)坪', \
                punctuation_cleaner.sub('', public))

        return find.group(1) if find else "0"

    # 公設比
    def get_public_utilities_ratio(self):
        ratio = 0.0

        public = float(self.get_public_utilities_pings().replace(u'坪',''))
        building = float(self.get_building_pings().replace(u'坪', ''))

        if building != 0:
            ratio = public / building * 100

        return "%.2f%%" % ratio

    def get_house_age(self):
        match = find_by_css(self.soup, '#obj-info ul li')

        age = match[5].text if match and len(match)>5 else ""
        find = re.search(u'屋齡：([0-9.]+年)', age.replace(u'\xa0', ''))

        return find.group(1) if find else ""

    def get_house_usage(self):
        return self.get_house_type()

    def get_house_type(self):
        match = find_by_css(self.soup, '.house_info tr')

        type_ = match[9].text if match and len(match)>9 else ""
        type_ = punctuation_cleaner.sub('',type_)
        find = re.search(u'類型(\w+)', type_)

        return find.group(1) if find else ""

    def get_decorating_level(self):
        return ""

    def get_lease_state(self):
        return ""

    def get_house_direction(self):
        match = find_by_css(self.soup, '.house_info tr')

        dir_ = match[8].text if match and len(match)>8 else ""
        dir_ = punctuation_cleaner.sub('', dir_)
        find = re.search(u'朝向大樓：(\w+)', dir_)

        return find.group(1) if find else ""

    def get_house_layout(self):
        match = find_by_css(self.soup, '#obj-info ul li')

        layout = match[4].text if match else ""
        layout = punctuation_cleaner.sub('', layout)

        return layout

    # there might have a better solution
    def get_separating_layout(self):
        house_layout = self.get_house_layout()

        m = re.search(ur'(\d+)房', house_layout)
        num_of_room = int(m.group(1)) if m else 0

        m = re.search(ur'(\d+)廳', house_layout)
        num_of_living = int(m.group(1)) if m else 0

        m = re.search(ur'(\d+)衛', house_layout)
        num_of_bath = int(m.group(1)) if m else 0

        m = re.search(ur'陽台', self.html)
        num_of_balcony = 1 if m else 0

        return num_of_room, num_of_living, num_of_bath, num_of_balcony

    def get_latitude_longtitude(self):
        ll_regex = re.compile('ll=(\d+.\d+?),(\d+.\d+?)&')

        m = ll_regex.search(self.html)

        try:
            lat = float(m.group(1))
            lng = float(m.group(2))
        except Exception as e:
            print("cannot find the latitude and longtitude")
            lat = lng = 0.0

        return lat, lng
