#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from lxml import html
import requests
import csv

page_source = open("QS Graduate Employability Rankings 2019 _ Top Universities.html", "r", encoding="utf-8").read()
tree = html.fromstring(page_source)
import codecs
result_file = codecs.open("result.csv", "w", "utf-8")
result_file.write(u'\ufeff')

def insert_row(result_row):
    result_file.write('"' + '","'.join(result_row) + '"' + "\n")
    result_file.flush()
header = ["Rank", "Name", "Location", "About", "Link"]
insert_row(result_row=header)

rows = tree.xpath('//table[@id="qs-rankings"]/tbody/tr')
for i, row in enumerate(rows):
    try:
        rank = row.xpath('.//span[contains(@class,"rank")]/text()')[0].strip()
    except:
        rank = ""
    try:
        name = row.xpath('td[@class=" uni"]//a[@class="title"]/text()')[0].strip()
    except:
        name = ""
    try:
        location = row.xpath('td[@class=" country"]/div/text()')[0].strip()
    except:
        location = ""
    try:
        link = row.xpath('td[@class=" uni"]//a[@class="title"]/@href')[0]
    except:
        link = ""

    try:
        r = requests.get(link)
        tree = html.fromstring(r.text)
        about = "\n".join([elm.strip() for elm in tree.xpath('//div[contains(@class,"field-profile")]//text()') if elm.strip()]).strip()
    except:
        about = ""

    result_row = [rank, name, location, about, link]
    insert_row(result_row)
    print("[Details] {}".format(result_row))
