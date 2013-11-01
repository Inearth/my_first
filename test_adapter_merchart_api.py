#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import unittest
import requests
import datetime as dt
import xml.etree.ElementTree as ET_xml
import config_parser
import json



goods = ['chair', 'book', 'sofa', 'car', 'tablet', 'mouse', 'display', 'notepad']

services = ['dpd', 'boxberry', 'b2c', 'sdek', 'ems']

states_of_postpackages = ['accepted', 'delivered', 'undelivered', 'awaiting', 'left_terminal',
                         'dispatching', 'arrived_to_city', 'arrived_to_office', 'refund']

delivery_states_of_orders = ['created', 'delivered', 'cancelled', 'in_delivery', 'accepted', 'assembled',
                        'passed_in_delivery', 'undelivered', 'fuck']


class TestAdapterMerchantApi(unittest.TestCase):

    @staticmethod
    def create_request(params):
        params = {'file': params}
        data = requests.post(config_parser.config.get('mediator', 'url'), files=params)
        output = True if data.content is '' and data.status_code == 200 else data.content
        return output

    @staticmethod
    def data_item(items, count_items):
        for i in range(count_items):
            item = ET_xml.SubElement(items, "item")
            item.set("quantity", str(random.randint(100, 500)))
            item.text = random.choice(goods)

    def data_packages(self, postpackages, count_postpackage, count_items):
        for i in range(count_postpackage):
            postpackage = ET_xml.SubElement(postpackages, "postpackage")
            postpackage.set("id", str(random.randint(100, 500)))
            items = ET_xml.SubElement(postpackage, "items")
            self.data_item(items, count_items)
            service = ET_xml.SubElement(postpackage, "service")
            service.text = random.choice(services)
            state_package = ET_xml.SubElement(postpackage, "state")
            state_package.text = random.choice(states_of_postpackages)
            time_package = ET_xml.SubElement(postpackage, "time")
            time_package.text = dt.datetime.now().strftime("%Y-%m-%d %H:%M")

    def data_order(self, orders, count_orders, count_postpackage, count_items):
        for j, i in enumerate(range(count_orders)):
            order = ET_xml.SubElement(orders, "order")
            order.set("id", str(j+1000))
            postpackages = ET_xml.SubElement(order, "postpackages")
            self.data_packages(postpackages, count_postpackage, count_items)
            state_ord = ET_xml.SubElement(order, "state")
            state_ord.text = random.choice(delivery_states_of_orders)
            time_ord = ET_xml.SubElement(order, "time")
            time_ord.text = dt.datetime.now().strftime("%Y-%m-%d %H:%M")

    def new_generate_xml(self, count_orders=1, count_postpackage=1, count_items=1):
        root = ET_xml.Element("xml")
        root.set("version", "1.0")
        root.set("encoding", "utf-8")
        orders = ET_xml.SubElement(root, "orders")
        self.data_order(orders, count_orders, count_postpackage, count_items)
        return ET_xml.tostring(root)

    def test_1mediator(self, count_elements=None):
        count_elements = [1, 1, 1]
        data_xml = self.new_generate_xml(count_elements[0], count_elements[1], count_elements[2])
        print data_xml
        self.assertIsNotNone(data_xml)
        response = self.create_request(data_xml)
        print 'Отправили файл ? : ', response


    def test_2get_new_sending(self):
        request = requests.get(config_parser.config.get('merchant_api', 'url'))
        data = json.loads(request.text)
        print data
        print data['status']

    def test_change_of_order(self):
        pass