from pattern.web import URL, DOM, plaintext
from pattern.web import NODE, TEXT, COMMENT, ELEMENT, DOCUMENT
from operator import itemgetter
import re

class InfoService:

	def __init__(self):
		self.names=[]
		self.adresses=[] 
		self.districts=[] 
		self.contacts=[]
		self.data=[]

	def clear_data(self):
		del self.names[:]
		del self.adresses[:]
		del self.districts[:]
		del self.contacts[:]
		del self.data[:]

	def print_info(self):
		for i in range(0,len(self.names)):
			print(self.names[i])
			print(self.adresses[i])
			print(self.districts[i])
			print(self.contacts[i])
			print

	def print_info_merged(self):
		for i in range(0,len(self.data)):
			print(self.data[i][0])
			print(self.data[i][1])
			print(self.data[i][2])
			print

	def generate_string_numbers(self,i):
		s=""
		for tel in self.data[i][2]:
			s=s+str(tel)+"/"
		return s[:-1]

	def generate_string_for_tablet(self):
		s="DEBUG?"+str(len(self.data))
		for i in range(0,len(self.data)):
			s=s+"$"+self.data[i][0]+"$"+self.data[i][1]+"$"+self.generate_string_numbers(i)
		return s

	def sort_and_merge(self):
		for i in range(0, len(self.names)): 
   			self.data.append((self.names[i], self.adresses[i],self.contacts[i], self.districts[i]))
   		self.data=sorted(self.data,key=itemgetter(3))

   	def sort_and_merge_with_district(self,district_value):
   		for i in range(0, len(self.names)): 
   			if(int(self.districts[i])==int(district_value)):
   				self.data.append((self.names[i], self.adresses[i],self.contacts[i], self.districts[i]))
   		self.data=sorted(self.data,key=itemgetter(3))

   	def remove_data_with_district_post_merged(self, district_value):
   		temp_data_list=[]
   		for d in self.data: 
   			if(int(d[3])==int(district_value)):
   				temp_data_list.append(d)
   		self.data=temp_data_list   		

class InfoAssistantManager:

	def __init__(self):
		self.myInfo = InfoService()

	def clear_data(self):
		self.myInfo.clear_data()

	def research_on_with_districts(self,what,where,district):
		self.research_on(what,where)
		self.myInfo.remove_data_with_district_post_merged(district)

	def research_on(self,what,where):

		url = URL("https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui="+what+"&ou="+where+"&proximite=0")
		dom = DOM(url.download(cached=True))

		for a in dom.by_tag("div.main-title pj-on-autoload "):
			for e in a.by_tag("span.denombrement"):
				number_of_results=int(self.decode_if_unicode(plaintext(e.content))[:3])

		number_of_page_results=number_of_results/20
		if(number_of_results%20 > 0):
			number_of_page_results+=1

		self.exctract_values(dom,self.myInfo)

		for i in range(2,number_of_page_results+1):
			url = URL("https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui="+what+"&ou="+where+"&proximite=0+""&page="+str(i))
			dom = DOM(url.download(cached=True))
			self.exctract_values(dom,self.myInfo)

		self.myInfo.sort_and_merge()

		
	def print_data(self):
		self.myInfo.print_info_merged()
		print("nb results stored=="+str(len(self.myInfo.data)))

	def print_data_tablet(self):
		print(self.get_string_for_tablet())

	def get_string_for_tablet(self):
		return self.myInfo.generate_string_for_tablet()

	def decode_if_unicode (self,a_string):
		if type(a_string) == unicode:
			a_string = a_string.encode('utf-8')
		return a_string

	def exctract_values(self,dom,myInfo):
		for a in dom.by_tag("a.denomination-links pj-lb pj-link"): # First <a class="title"> in entry.
	   	 	myInfo.names.append(self.decode_if_unicode(plaintext(a.content)))

		#adresses
		for a in dom.by_tag("a.adresse pj-lb pj-link"): # First <a class="title"> in entry.
			myInfo.adresses.append(self.decode_if_unicode(plaintext(a.content)))
			numbers=re.findall(r'\d+',self.decode_if_unicode(plaintext(a.content)))
			myInfo.districts.append(numbers[-1])

		#telephones
		for a in dom.by_tag("ul.main-contact-container clearfix"): # First <a class="title"> in entry.	
			contact=[]
			for e in a.by_tag("div.tel-zone noTrad"):
				contact.append(self.decode_if_unicode(plaintext(e.content))[-14:])
				'''
				telephone_number=re.findall(r'\d+',self.decode_if_unicode(plaintext(a.content)))
				telephone_string=""
				for s in telephone_number:
					telephone_string=telephone_string+str(s)
				contact.append(telephone_string)
				'''
			myInfo.contacts.append(contact)

if __name__ == "__main__":
	what="taxi"
	where="toulouse"
	district=33000
	infoAssistant = InfoAssistantManager()
	infoAssistant.research_on(what,where)
	infoAssistant.remove_data_with_district_post_merged(district)
	#infoAssistant.research_on_with_districts(what,where,district)
	infoAssistant.print_data()
	#infoAssistant.print_data_tablet()