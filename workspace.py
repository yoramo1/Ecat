import sys
from xml.etree.ElementTree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.etree 

import YoUtil

class workspace:
	def __init__(self,path):
		self.path = path
		self.target_list = list()
		self.load()


	def load(self):
		YoUtil.debug_print('loading ->', self.path)
		self.tree = ET()
		self.tree.parse(self.path)
		root = self.tree.getroot()	
		xml_list = root.findall('Workspace/Targets/item')
		if  xml_list != None:
			YoUtil.debug_print('lst',xml_list)
			for xml_node in xml_list:
				pass
				
		
	def to_string(self):
		ret = 'Workspace'
		for tm in self.target_list:
			ret += '\n\t'+tm.to_string()
		return ret