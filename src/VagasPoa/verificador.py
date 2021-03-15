import os
import re
import time
import pprint

mailing = []
file=open('limpador.txt','r', encoding='utf-8')
mailing = file.read().split(',')
file.close()

def converter(match):
	return str(match).\
		replace('[', '').\
		replace(']','').\
		replace("'", '')

def reader():
	pre_domain = []
	index = 0
	while index < len(mailing)-1:
		match = re.findall(r'^.+@(.+)\.[\w]+$', mailing[index])
		string = converter(match)
		pre_domain += [string]
		index = index + 1
	return pre_domain

def info():
	print("\n")
	print("Quantity " + str(len(mailing)))

pre_domains = reader()

info()

domains = {}
begin = 0

while begin < len(pre_domains)-1:
	count_duplicate = 0
	end = len(pre_domains)-1
	while end >= 0:

		if pre_domains[end] == pre_domains[begin]:
			domain_address = pre_domains[begin]
			domains[domain_address] = 0

			count_duplicate = count_duplicate + 1

			if domain_address != '':
				if domain_address in domains:
					domains[domain_address] = count_duplicate

		end = end - 1
	begin = begin + 1


pprint.pprint(domains)
#sorted_domains = sorted(domains.items(), key=lambda item: item[1])
#pprint.pprint(sorted_domains)