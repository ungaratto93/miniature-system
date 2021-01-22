import os, requests, datetime, glob, json, re
from bs4 import BeautifulSoup as soup

class Magalu(object):
	"""docstring for Magalu"""
	def __init__(self):
		super(Magalu, self).__init__()
		self.__attr_statuscode = ''
		self.__attr_contentasbytes = ''
		self.__attr_contentastext = ''	

	def getDealsDay(self):
		try:
			self.startAt()
			deals_base_url = 'https://www.magazineluiza.com.br/selecao/ofertasdodia/?header=ofertasdodia.png&statute=ofertasdodia.html'
			deals_page_url = "https://www.magazineluiza.com.br/selecao/ofertasdodia?header=ofertasdodia.png&statute=ofertasdodia.html&page="

			base_response = requests.get(deals_base_url)
			self.attr_statuscode = base_response.status_code
			self.attr_contentasbytes = base_response.content
			self.attr_contentastext = base_response.text

			soup_data = soup(self.attr_contentastext, 'lxml')
			btnp = soup_data.find_all("a", attrs={"role": "button"})
			size_btnp = len(btnp) 
			text_btnp = ""
			for index in range(size_btnp):
				text_btnp = text_btnp + btnp[index].get_text() + ","

			tnp = text_btnp.split(",")[2:len(text_btnp.split(","))-2]
			np = len(tnp)+1

			for index_page in range(np):
				number_page = index_page+1
				#print(deals_page_url + str(index_page+1))
				response = requests.get(deals_page_url + str(number_page))
				soup_data = soup(response.text, 'lxml')

				data = self.collectData(soup_data)
				self.saveData(data, number_page)

			self.endAt()
		except Exception as e:
			print("An error was occurred.")
			raise e

	def collectData(self, spd):
		try:
			scr = spd.find_all("a", attrs={"name": "linkToProduct"})
			scr = str(scr)

			soup_data = soup(scr, 'lxml')
			std = soup_data.find_all("script")
			std = str(std)
			std = std.replace('[<script type="application/ld+json">', '')
			std = std.replace('</script>, <script type="application/ld+json">', ',')
			std = std.replace('</script>]', '')
			#std = std.replace("/\r?\n|\r/g", '')
			#print(std.replace('\n', ''))

			return std
		except Exception as e:
			raise e

	def saveData(self, std, number_page):
		try:
			size = len(str(std))
			f = open("data/saved/MAGALU_DEALSDAY_" + str(number_page) + "_" + datetime.datetime.now().strftime("%d%m%Y_%H%M%S") +".json","w+")
			for index in range(size):
				f.write(std[index])
				index = index + 1
			f.close()
		except (RuntimeError, NameError, TypeError) as e:
			print(e)
			raise e


	# BEGIN HANDLER PROCCESS
	def getDataForHandler(self):
		try:
			self.startAt()
			for file_json in glob.glob("data/saved/*.json"):
				tuple_path = os.path.split(file_json)
				string_filename = str(tuple_path[1]).split('.')[0]
				#print(string_filename)
				self.handlerData(string_filename)
			self.endAt()
		except Exception as e:
			raise e

	def handlerData(self, filename):
		try:

			# CONVERTS JSON FOR DICT  #
			test = []
			strt = ""
			count_product = 0
			
			for file_json in glob.glob("data/saved/" + filename + ".json"):
				file = open(file_json, "r") 
				for string in file:
					test.append(string)

			
			# VERIFY CONVERSION VALUE #
			#print(test)

			# HANDLE JSON IN DICT FORMAT FOR TO REMOVE \N #
			# problem: remove \n of name of productan and description
			size_test = len(test)
			for x in range(size_test):
				test[x] = test[x].replace('\n','')
				test[x] = test[x].replace('\t','')
				test[x] = test[x].replace(' ','')	
				#test[x] = test[x].replace(',','\r')
				test[x] = test[x].replace('},{', "}\r{")
				strt = strt + test[x]

			#print(strt)
			# SAVE THE HANDLED JSON #
			size_strt = len(strt)
			f = open("data/handled/" + filename + ".json", 'w')
			for index in range(size_strt):
				f.write(strt[index])
				index = index + 1
			f.close()


			#HANDLE STRING
			file = open("data/handled/" + filename + ".json", "r+") 
			for string in file.readlines(): #le a linha
				string = "'" + string + "'"
				#print(string)

				if (re.findall(r'\w"{1}\w', string) != []):
					str_match = re.findall(r'\w"{1}\w', string)
					#print(str_match)
					#print(str_match[0])
					string = string.replace(str_match[0], str(str_match[0]).replace('"', "")+"")
					string = "" + string + ""
					#print(string)
				
				elif (re.findall(r'[GalaxyTabA]\W+\d"{1}\W', string) != []):
					str_match = re.findall(r'[GalaxyTabA]\W+\d"{1}\W', string)
					#print(str_match)
					#print(str_match[0])
					string = string.replace(str_match[0], str(str_match[0]).replace('"', "")+"")
					string = "" + string + ""
					#print(string)				

				string = str(string).replace("'","")
				opened_file = open("data/cleaned/" + filename + ".json", 'a+')
				opened_file.write(string)
				opened_file.close()

				# COLECT VALUES #
				#json_object = json.dumps(string) <--- nao precisa fazer essa transformação para string
				#print(type(json_object))
				
				json_object = json.loads(string) # <--- transforma em dict
				#print(type(json_object))
				
				count_product = count_product + 1
				for key in json_object:
					value = json_object[key]
					if (type(value) == dict):
						
						string_data = json.dumps(value)
						string_data = string_data.replace('@', '')
						dict_data = json.loads(string_data)
						
						for key, value in dict_data.items():
							if (key in ('name', 'type', 'lowPrice', 'highPrice','priceCurrency', 'offerCount', 'sku', 'description')):
								if(value not in ('AggregateRating', 'AggregateOffer')):
									continue
									#print("KEY: 	" + str(key) + " 	VALUE:	" + str(value))

					elif (type(value) == str):
						if (key in ('name', 'type', 'lowPrice', 'highPrice','priceCurrency', 'offerCount', 'sku', 'description')):
							if(value not in ('AggregateRating', 'AggregateOffer')):
								continue
								#print("KEY: 	" + str(key) + " 	VALUE:	" + str(value))

					#elif (type(value) == list):
					#	print("list : " + str(value))
						#for k in value:
							#print(k)
							#v = value[k]						
							#print(str(type(v)) + "  " + v)

			file.close()
			#print("PRODUCT : " + str(count_product))
		except Exception as e:
			raise e
	# END HANDLER PROCCESS

	# LOG TRANSFORM IN A CLASS
	def startAt(self):
		try:
			print("Start:")
			print(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
		except Exception as e:
			raise e

	def endAt(self):
		try:
			print("End:")
			print(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
		except Exception as e:
			raise e
