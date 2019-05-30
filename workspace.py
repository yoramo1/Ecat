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
			#YoUtil.debug_print('lst',xml_list)
			for xml_node in xml_list:
				tm = target_model(xml_node)
				self.target_list.append(tm)
		
	def to_string(self):
		ret = 'Workspace ==>> ' +str(len(self.target_list))+' targets'
		for tm in self.target_list:
			ret += '\n\t'+tm.to_string()
		return ret
		
class target_model:
	def __init__(self,xml_node):
		#YoUtil.debug_print(xml_node.tag,None)
		self.xml_node = xml_node
		self.item_type = None
		self.the_xml_node= None
		self.name=None
		self.type=None
		self.id=None	
		self.ParentGMASName=None
		self.TargetType=None
		self.CommunicationInfoString = None
		self.isMultiAxis=None
		self.load()
		
	def load(self):
		self.item_type = self.xml_node.find('item_type').text
		self.shrot_item_type = self.get_short_item_type()
		if self.shrot_item_type!=None:
			self.the_xml_node=self.xml_node.find(self.shrot_item_type)
			if self.the_xml_node!= None:
				self.name = self.the_xml_node.get('Name')
				self.ParentGMASName=self.the_xml_node.get('ParentGMASName')
				self.TargetType = self.the_xml_node.get('TargetType')
				self.id = self.the_xml_node.get('ID')
				self.CommunicationInfoString = self.the_xml_node.get('CommunicationInfoString')
				if self.shrot_item_type=='MaestroTargetModel':
					self.isMultiAxis = self.the_xml_node.get('IsMultiAxis')
		
	def get_short_item_type(self ):
		ret=None
		if self.item_type!= None:
			s = self.item_type.split(',')
			s1=s[0].split('.')
			l = len(s1)
			if l > 0:
				ret= s1[l-1]
		return ret
	
	def to_string(self):
		ret = 'TargetModel - '
		if self.shrot_item_type!= None:
			ret = self.shrot_item_type
		if self.name!= None:
			ret += '\t"'+self.name+'"'
		if self.id!= None:
			ret += '\tID='+self.id
		if self.ParentGMASName!= None:
			ret += '\t'+self.ParentGMASName
		if self.TargetType!= None:
			ret += '\tTargetType='+self.TargetType
		if self.isMultiAxis!= None:
			ret += '\tIsMultiAxis='+self.isMultiAxis
		#if self.CommunicationInfoString!= None:
			#ret += '\CommunicationInfoString='+self.CommunicationInfoString
		
		
		return ret
