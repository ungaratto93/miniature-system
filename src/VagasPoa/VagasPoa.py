import os, requests, datetime, glob, json, re
from datetime import datetime
from bs4 import BeautifulSoup as soup
import re
import time

class VagasPoa(object):
	""" Script para coletar emails do siste VagasPoa https://vagaspoa.com.br/ """

	def __init__(self, arg=0):
		super(VagasPoa, self).__init__()
		self.arg = arg
		self.string_w = ''

	def saveLog(self, url, page, status_code):
		try:
			print(url)
			with open('log.txt', 'a', encoding='utf-8') as logfile:
				logfile.write("LOG: GET " + str(url) + " | " + page + " | " + str(status_code) + " | " +  str(datetime.now().strftime("%d/%m/%y %H:%M:%S \n")))
		except (RuntimeError, NameError, TypeError) as e:
			print(e)

	def saveEmail(self, string):
		try:
			if (str(string[0]) != str(self.string_w)):
				with open('maillist.txt', 'a', encoding='utf-8') as file:
					file.write(str(string[0]) + "," + "\n")
				self.string_w = string[0]

		except (RuntimeError, NameError, TypeError) as e:
			print(e)

	def getEmail(self, url):
		try:
			response = requests.get(url)
			soup_data = soup(response.text, 'html.parser')

			for p in soup_data.find_all('p'):
				line = p.get_text()
				match = re.findall(r'[\w\.-]+@[\w\.-]+', line)
				if len(match) > 0:
					self.saveEmail(match)
		except AttributeError as e:
			print("ResultSet object has no attribute 'get_text'")

	def getPage(self):
		try:
			number = 842 #paginas ate 2510
			status_code = ''

			url = 'https://vagaspoa.com.br/'
			while number <= 2510:
				next_url = ''
				next_page = "page/" + str(number) + "/"
				next_url = str(url) + str(next_page)
				time.sleep(15)
				response = requests.get(next_url)
				status_code = str(response.status_code)
				self.saveLog(next_url, str(number), status_code)
				self.getEmail(next_url)
				number = number + 1
			print("Fim")
		except (ConnectionError, ConnectionResetError) as e:
 			print('Connection aborted.')
 			print('Foi forçado o cancelamento de uma conexão existente pelo host remoto')
