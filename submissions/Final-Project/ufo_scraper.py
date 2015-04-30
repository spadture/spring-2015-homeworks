#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import argparse
import logging
import requests
import pandas as pd
import numpy as np
import re
import csv
from BeautifulSoup import BeautifulSoup

base_url = "http://www.nuforc.org/webreports/"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36"

def get_entry(url):
	headers = {'User-Agent': user_agent}
	response = requests.get(base_url+url, headers=headers)
	html = response.text.encode('utf-8')
	id = url
	soup = BeautifulSoup(html)
	entries = soup.findAll('td')
	#split = re.split(' : |,|Reported : |, Posted : |, Locations : |,Shape : |,Duration : |',entries[0].text)
	try:
		stats = str(entries[0])
		split = re.split('>', stats)

		occurred = re.split(' : ',str(split[2]))
		reported = re.split('d: ',str(split[3]))
		posted = re.split('d: ',str(split[4]))
		location = re.split('n: ',str(split[5]))
		shape = re.split('e: ',str(split[6]))
		duration = re.split('n:',str(split[7]))
		
		occurred = occurred[1].replace('  (Entered as','')
		reported = reported[1].replace('<br /','')
		posted = posted[1].replace('<br /','')
		location = location[1].replace('<br /','')
		shape = shape[1].replace('<br /','')
		duration = duration[1].replace('</font','')
	except IndexError:
		occurred = ""
		reported = ""
		posted = ""
		location = ""
		shape = ""
		duration = ""
	
	try:
		description = str(entries[1].text)
	except IndexError:
		description = ""
	
	print occurred
	print reported
	print posted
	print location
	print shape
	print duration
	print description
	
	with open('ufo.csv', 'a') as csvfile:
		fieldnames = ['id','occurred', 'reported', 'posted', 'location', 'shape', 'duration','descriptions']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerow({'id':id,'occurred': occurred, 'reported': reported, 'posted': posted, 'location': location, 'shape': shape, 'duration': duration, 'descriptions':description})
   
	
def get_report(url):
	headers = {'User-Agent': user_agent}
	response = requests.get(base_url+url, headers=headers)
	html = response.text.encode('utf-8')

	soup = BeautifulSoup(html)
	link_table = list()
	for link in soup.findAll('a', href=True):
		if(link['href']!="http://www.nwlink.com/~ufocntr"):
			link_table.append(link['href'])
	
	return link_table	

def get_urls(html):
	soup = BeautifulSoup(html)
	link_table = list()
	for link in soup.findAll('a', href=True):
		if(link['href']!="http://www.nwlink.com/~ufocntr"):
			link_table.append(link['href'])
	
	return link_table
	

def scrape_ufos(datadir='data/'):
    headers = {'User-Agent': user_agent}
    response = requests.get(base_url+'ndxevent.html', headers=headers)
    html = response.text.encode('utf-8')
    urls = get_urls(html)
    for url in urls[12:]:
    	reports = get_report(url)
    	for report in reports:
    		get_entry(report)
scrape_ufos()