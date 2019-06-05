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
		ret = 'Workspace ==>> ' +str(len(self.target_list))+' targets:'
		for tm in self.target_list:
			ret += '\n'+tm.to_string()
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
		self.device_type = None
		self.group_name = None
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
				self.device_type = self.the_xml_node.get('DeviceType')
				self.group_name = self.the_xml_node.get('GroupName')
		
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
		if self.shrot_item_type != 'MaestroTargetModel' and (self.ParentGMASName== None or len(self.ParentGMASName)==0):
			ret = '  ! - '
		else:
			ret = '  '
		if self.shrot_item_type!= None:
			ret+= '{:<33}'.format(self.shrot_item_type)
		
		if self.name!= None:
			ret+= '"{:<15}"'.format(self.name)
		if self.id!= None:
			ret += '\t'+'ID='+self.id
		if self.ParentGMASName!= None:
			ret += '   {:<5}'.format(self.ParentGMASName)
		if self.TargetType!= None:
			ret+= '\tTargetType={:<22}'.format(self.TargetType)
		if self.device_type!= None:
			ret+= '\tDeviceType={:<10}'.format(self.device_type)
		if self.group_name!= None:
			ret += '\t'+'GroupName='+self.group_name
		#if self.CommunicationInfoString!= None:
			#ret += '\CommunicationInfoString='+self.CommunicationInfoString
		
		
		return ret
