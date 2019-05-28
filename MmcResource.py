import sys
import os
from xml.etree.ElementTree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.etree 

import YoUtil


class MmcResource:
	def __init__(self,path):
		self.path = path
		self.res_id  = None
		self.node_list=list()

		
	def load(self):
		YoUtil.debug_print('loading ->', self.path)
		self.tree = ET()
		self.tree.parse(self.path)
		root = self.tree.getroot()
		xml_list = root.findall('GLOBAL_PARAMS/NAME')
		if xml_list != None:
			YoUtil.debug_print('xml_list=',xml_list)
			for xml_name in xml_list:
				res_id =  xml_name.get('RES_ID')
				YoUtil.debug_print('Res_ID=',res_id)
				if res_id != None:
					self.res_id =res_id
		xml_list = root.findall('MOTION_DEVICES/NODE')
		if xml_list != None:
			YoUtil.debug_print('Nodes xml_list=',xml_list)
			for xml_node in xml_list:
				self.load_node(xml_node)
				
	def load_node(self,xml_node):
		#YoUtil.debug_print('node->',xml_node)
		if xml_node != None:
			node = MmcNode(xml_node)
			self.node_list.append(node)
		
		
	def print(self):
		print('MMCResource ->',self.path)
		print('RES_ID=',self.res_id)
		for node in self.node_list:
			print(node.to_string())
		
		
		
		
		
class MmcNode:
	def __init__(self,xml_node):
		self.xml_node = xml_node
		self.name=None
		self.type=None
		self.id=None
		self.load()
		
	def load(self):
		pass
		self.name=self.xml_node.get('NAME')
		self.type=self.xml_node.get('TYPE')
		self.id=self.xml_node.get('ID')
		
	def to_string(self):
		ret= 'Node Name='+self.name+'ID='+self.id
		
		return ret