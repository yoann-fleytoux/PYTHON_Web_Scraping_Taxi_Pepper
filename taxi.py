import datetime
import time
import xml.etree.cElementTree as parser
import unidecode
import taxi_search_module
from naoqi import ALProxy, ALModule, ALBroker

class Taxi(ALModule):
	def __init__(self, name):
		ALModule.__init__(self, name)
		self.mem = ALProxy('ALMemory')

		self.search_engine = taxi_search_module.InfoAssistantManager()	
		self.mem.subscribeToEvent('SetCityWithDepartment', name,  'set_city_with_nom_departement')
		self.mem.subscribeToEvent('SetCity', name,  'show_taxi_tablet')
		self.mem.subscribeToEvent('SetPostalCode', name,  'remove_with_postal_codes')

	def show_taxi_tablet(self,key, value, message):
		print("show tablet from dialog event")
		where = value
		self.search_engine.research_on("taxi",where)
		self.search_engine.infoAssistant.print_data_tablet()
        #use this line and the code on the tablet git to show the GUI
		#self.search_engine.infoAssistant.get_string_for_tablet()
		#self.mem.raiseMicroEvent('ShowingTaxiDone')
	
    #update what is shown by removing the taxis who are not in the right postal code
	def remove_with_postal_codes(self,key, value, message):
		print("Update data")
		district = value
		self.search_engine.infoAssistant.remove_data_with_district_post_merged(district)
		self.search_engine.infoAssistant.print_data_tablet()
        #use this line and the code on the tablet git to show the GUI
		#self.search_engine.infoAssistant.get_string_for_tablet()
		#self.mem.raiseMicroEvent('ShowingTaxiDone')

	def set_city_with_nom_departement(self,key,value, message):
		departement = value
		e = parser.parse('listCityFrance.xml').getroot()
		city_list = []
		code_postal_list = []
		for i in range(0,len(e)):
			for j in range(0,len(e.getchildren()[i].getchildren())):
				if (str(e.getchildren()[i].getchildren()[j].get("name").encode('utf-8'))==value):
					for k in range(0,len(e.getchildren()[i].getchildren()[j].getchildren())):
						city_list.append(e.getchildren()[i].getchildren()[j].getchildren()[k].get("name"))
						codePostal = e.getchildren()[i].getchildren()[j].getchildren()[k].get("codePostal")
						if codePostal not in code_postal_list:
							code_postal_list.append(codePostal)
		ALDialog.setConcept("cities", "frf", city_list)
		ALDialog.setConcept("postalCodes", "frf", code_postal_list)
		
	def set_city_with_region(self,key,value, message):
		region = value
		e = parser.parse('listCityFrance.xml').getroot()
		city_list = []
		code_postal_list = []
		for i in range(0,len(e)):
			if (str(e.getchildren()[i].get("name").encode('utf-8'))==value):
				for j in range(0,len(e.getchildren()[i].getchildren())):
					for k in range(0,len(e.getchildren()[i].getchildren()[j].getchildren())):
						city_list.append(e.getchildren()[i].getchildren()[j].getchildren()[k].get("name"))
						codePostal = e.getchildren()[i].getchildren()[j].getchildren()[k].get("codePostal")
						if codePostal not in code_postal_list:
							code_postal_list.append(codePostal)
		ALDialog.setConcept("city", "frf", city_list)
		ALDialog.setConcept("code_postal", "frf", code_postal_list)


	def set_city_with_numero_departement(self,key,value, message):
		departement = value
		e = parser.parse('listCityFrance.xml').getroot()
		city_list = []
		code_postal_list = []
		for i in range(0,len(e)):
			for j in range(0,len(e.getchildren()[i].getchildren())):
				if (str(e.getchildren()[i].getchildren()[j].get("numero").encode('utf-8'))==value):
					for k in range(0,len(e.getchildren()[i].getchildren()[j].getchildren())):
						city_list.append(e.getchildren()[i].getchildren()[j].getchildren()[k].get("name"))
						codePostal = e.getchildren()[i].getchildren()[j].getchildren()[k].get("codePostal")
						if codePostal not in code_postal_list:
							code_postal_list.append(codePostal)
		ALDialog.setConcept("city", "frf", city_list)
		ALDialog.setConcept("code_postal", "frf", code_postal_list)

myBroker = ALBroker("myBroker","0.0.0.0",0,"192.168.1.124",9559)
Taxi = Taxi('taxi')
global ALDialog
ALDialog = ALProxy("ALDialog")
ALDialog.setLanguage("French")
ALDialog.subscribe("Topic_test")

path = "/var/persistent/home/nao/pge/dialog_topics/taxi_dialog.top"
topicName = ALDialog.loadTopic(path.encode('utf-8'))
print topicName

ALDialog.activateTopic(topicName)
	
print ALDialog.getActivatedTopics()

try:
	while True:
		time.sleep(2)
except KeyboardInterrupt:
	print "Fin du game"
ALDialog.unsubscribe("Topic_test")
ALDialog.desactivateTopic(topicName)
ALDialog.unloadTopic(topicName)		


