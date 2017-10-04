# -*- coding: utf-8 -*-
from parser_591 import SuperParser591
from sinyi.sinyi_parser import SuperParserSinYi

import json

def test_get_latitude_longtitude(parser):
    lat, lng = parser.get_latitude_longtitude()
    print(lat, lng)

def test_get_case_name(parser):
    name = parser.get_case_name()
    print("標題: %s" % name)

def test_get_case_number(parser):
    name = parser.get_case_number()
    print("編號: %s" % name)

def test_get_address(parser):
    address = parser.get_address()
    print("地址: %s" % address)

def test_separating_address(parser, address):
    city, district, road = parser.get_separating_address(address)
    print("城市: %s\n區域: %s\n路名: %s" % (city, district, road))

def test_get_price(parser):
    price, unit = parser.get_price()
    print("價格: %.2f %s" % (price, unit))

def test_get_price_per_pings(parser):
    price, unit = parser.get_price_per_pings()
    print("每坪價格: %f %s" % (price, unit))

def test_get_buling_pings(parser):
    building_pings = parser.get_building_pings()
    print("建坪: %s" % building_pings)

def test_get_floor_pings(parser):
    floor_pings = parser.get_floor_pings()
    print("地坪: %s" % floor_pings)

def test_get_main_building_pings(parser):
    main_building = parser.get_main_building_pings()
    print("主建物坪數: %s" % main_building)

def test_get_attached_building_pings(parser):
    attached_building_pings = parser.get_attached_building_pings()
    print("附屬建物坪數: %s" % attached_building_pings)

def test_get_public_utilities_pings(parser):
    public_utilities_pings = parser.get_public_utilities_pings()
    print("公設坪數: %s" % public_utilities_pings)

def test_get_public_utilities_ratio(parser):
    public_utilities_ratio = parser.get_public_utilities_ratio()
    print("公設比: %s" % public_utilities_ratio)

def test_get_parking_space(parser):
    parking_space = parser.get_parking_space()
    print("車位: %s" % parking_space)

def test_get_house_age(parser):
    house_age = parser.get_house_age()
    print("屋齡: %s" % house_age)

def test_get_community(parser):
    community = parser.get_community()
    print("社區: %s" % community)

def test_house_layout(parser):
    house_layout = parser.get_house_layout()
    print("格局: %s" % house_layout)

def test_house_type(parser):
    house_type = parser.get_house_type()
    print("房屋類型: %s" % house_type)

def test_house_usage(parser):
    house_usage = parser.get_house_usage()
    print("房屋用途: %s" % house_usage)

def test_host_phonenumber(parser):
    phonenumber = parser.get_host_phonenumber()
    print("聯絡電話: %s" % phonenumber)

def test_host_name(parser):
    host_name = parser.get_host_name()
    print("聯絡人: %s" % host_name)

def test_host_role(parser):
    host_role = parser.get_host_role()
    print("聯絡人性質: %s" % host_role)

def test_host_mail(parser):
    mail = parser.get_host_mail()
    print("聯絡信箱: %s" % mail)

def test_host_company(parser):
    company = parser.get_host_company()
    print("聯絡人公司: %s" % company)

def test_house_direction(parser):
    direction = parser.get_house_direction()
    print("方位: %s" % direction)

def test_house_decorating_level(parser):
    decorating_level = parser.get_decorating_level()
    print("裝潢程度:" % decorating_level)

def test_lease_staet(parser):
    lease_state = parser.get_lease_state()
    print("租約:" % lease_state)

def test_separating_layout(parser):
    num_of_room, num_of_living, num_of_bath, num_of_balcony = parser.get_separating_layout()

    print(num_of_room, "房")
    print(num_of_living, "客廳")
    print(num_of_bath, "廁所")
    print(num_of_balcony, "陽台")


# For testing
if __name__ == '__main__':
    html = ""
    with open('data/html/00859H') as fp:
        page = fp.read()

    sinyi_html = page

    with open('data/sale_page.txt') as fp:
        lines = fp.readlines()

    for line in lines:
        html += line
    parser = SuperParser591(html, 'url', 'S')

    '''
    test_get_latitude_longtitude(parser)
    test_get_case_name(parser)
    test_get_case_number(parser)
    test_get_address(parser)
    test_separating_address(parser, parser.get_address())
    test_get_price(parser)
    test_get_price_per_pings(parser)
    test_get_buling_pings(parser)
    test_get_floor_pings(parser)
    test_get_house_age(parser)
    test_house_layout(parser)
    test_separating_layout(parser)
    test_house_decorating_level(parser)
    test_lease_staet(parser)
    test_get_community(parser)
    test_host_name(parser)
    test_host_role(parser)
    test_host_company(parser)
    test_host_phonenumber(parser)
    test_host_mail(parser)

    obj = parser.fill_data_into_schema()
    obj = json.dumps(obj, indent=4,ensure_ascii=False).encode('utf-8')
    print(obj)
    '''
    obj = parser.fill_data_into_schema()
    obj = json.dumps(obj, indent=4,ensure_ascii=False)
    print(obj)


    sinyi_parser = SuperParserSinYi(sinyi_html, 'url', 'S')
    test_get_case_number(sinyi_parser)
    test_get_case_name(sinyi_parser)
    test_host_name(sinyi_parser)
    test_host_role(sinyi_parser)
    test_host_company(sinyi_parser)
    test_host_phonenumber(sinyi_parser)
    test_get_price(sinyi_parser)
    test_get_price_per_pings(sinyi_parser)
    test_get_address(sinyi_parser)
    test_separating_address(sinyi_parser, sinyi_parser.get_address())
    test_get_buling_pings(sinyi_parser)
    test_get_floor_pings(sinyi_parser)
    test_get_house_age(sinyi_parser)
    test_house_layout(sinyi_parser)
    test_separating_layout(sinyi_parser)
    test_get_parking_space(sinyi_parser)
    test_get_public_utilities_pings(sinyi_parser)
    test_house_direction(sinyi_parser)
    test_house_type(sinyi_parser)
    test_house_usage(sinyi_parser)
    test_get_parking_space(sinyi_parser)
    test_get_public_utilities_ratio(sinyi_parser)

    obj = sinyi_parser.fill_data_into_schema()
    obj = json.dumps(obj, indent=4, ensure_ascii=False)
    print(obj)
