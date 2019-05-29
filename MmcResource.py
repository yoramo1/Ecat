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
		self.io_list = list()
		self.general_list = list()
		self.virtual_list = list()
		self.gateway_list = list()
		
	def load(self):
		YoUtil.debug_print('loading ->', self.path)
		self.tree = ET()
		self.tree.parse(self.path)
		root = self.tree.getroot()
		xml_list = root.findall('GLOBAL_PARAMS/NAME')
		if xml_list != None:
			#YoUtil.debug_print('xml_list=',xml_list)
			for xml_name in xml_list:
				res_id =  xml_name.get('RES_ID')
				#YoUtil.debug_print('Res_ID=',res_id)
				if res_id != None:
					self.res_id =res_id
		xml_list = root.findall('MOTION_DEVICES/NODE')
		if xml_list != None:
			#YoUtil.debug_print('Nodes xml_list=',xml_list)
			for xml_node in xml_list:
				self.load_node(xml_node)
		
		xml_list = root.findall('IO_DEVICES/NODE')
		if xml_list != None:
			#YoUtil.debug_print('Nodes xml_list=',xml_list)
			for xml_node in xml_list:
				self.load_io(xml_node)
				
		xml_list = root.findall('GENERAL_DEVICES/NODE')
		if xml_list != None:
			#YoUtil.debug_print('Nodes xml_list=',xml_list)
			for xml_node in xml_list:
				self.load_general(xml_node)
				
		xml_list = root.findall('VIRTUAL_OBJECTS/VIRTUAL_OBJECT')
		if xml_list != None:
			#YoUtil.debug_print('Nodes xml_list=',xml_list)
			for xml_node in xml_list:
				self.load_virtual(xml_node)

				
	def load_node(self,xml_node):
		#YoUtil.debug_print('node->',xml_node)
		if xml_node != None:
			node = MmcNode(xml_node)
			self.node_list.append(node)
			
	def load_io(self,xml_node):
		#YoUtil.debug_print('node->',xml_node)
		if xml_node != None:
			node = MmcNode(xml_node)
			self.io_list.append(node)
		
	def load_general(self,xml_node):
		#YoUtil.debug_print('node->',xml_node)
		if xml_node != None:
			node = MmcNode(xml_node)
			self.general_list.append(node)
			
	def load_virtual(self,xml_node):
		#YoUtil.debug_print('node->',xml_node)
		if xml_node != None:
			node = virtual_object(xml_node)
			self.virtual_list.append(node)
		
		
	def print(self):
		print('MMCResource ->',self.path)
		print('RES_ID=',self.res_id)
		print('MOTION_DEVICES:')
		for node in self.node_list:
			print('\t',node.to_string())
		print('IO_DEVICES:')
		for node in self.io_list:
			print('\t',node.to_string())
		print('GENERAL_DEVICES:')
		for node in self.general_list:
			print('\t',node.to_string())
		print('VIRTUAL_OBJECTS:')
		for node in self.virtual_list:
			print('\t',node.to_string())
		print('SUBGATEWAY:')
		for node in self.gateway_list:
			print('\t',node.to_string())
		
		
		
		
		
class MmcNode:
	def __init__(self,xml_node):
		self.xml_node = xml_node
		self.name=None
		self.type=None
		self.id=None
		self.node_name = None
		self.node_offset=None
		self.subtype = None
		self.drive_type=None
		self.load()
		
	def load(self):
		pass
		self.name=self.xml_node.get('NAME')
		self.type=self.xml_node.get('TYPE')
		self.id=self.xml_node.get('ID')
		self.node_name = self.xml_node.get('NODE_NAME')
		self.node_offset = self.xml_node.get('NODE_OFFSET')
		self.subtype = self.xml_node.get('SUBTYPE')
		self.drive_type = self.xml_node.get('DRIVE_TYPE')
		
	def to_string(self):
		ret= 'Node Name='+self.name+'\tID='+self.id
		if self.node_name != None:
			ret = ret+'\tNode_Name='+self.node_name
		if self.node_offset != None:
			ret = ret+'\tNode_Offset='+self.node_offset
		if self.subtype != None:
			ret = ret+'\tSubtype='+self.subtype
		if self.drive_type != None:
			ret = ret+'\tDriveType='+self.drive_type
		return ret
		
class virtual_object:
	def __init__(self,xml_node):
		self.xml_node = xml_node
		self.name=None
		self.type=None
		self.id=None
		self.member_list = list()
		self.load()
		
	def load(self):
		pass
		self.name=self.xml_node.get('NAME')
		self.type=self.xml_node.get('TYPE')
		self.id=self.xml_node.get('ID')
		xml_list = self.xml_node.findall('MEMBER')
		if xml_list!= None:
			for xml_node in xml_list:
				member = virtual_object_member(xml_node)
				self.member_list.append(member)
		
	def to_string(self):
		ret= 'Virtual Name='+self.name+' ID='+self.id
		if self.type != None:
			ret = ret+'\ttype='+self.type
		if len(self.member_list) > 0:
			for member in self.member_list:
				ret+= '\n\t\t'+member.to_string()
		return ret
		
class virtual_object_member:
	def __init__(self,xml_node):
		self.xml_node = xml_node
		self.name=None
		self.type=None
		self.id=None
		self.index_in_group = None
		self.member_list = list()
		self.load()
		
	def load(self):
		pass
		self.name=self.xml_node.get('NAME')
		self.type=self.xml_node.get('TYPE')
		self.id=self.xml_node.get('ID')
		self.index_in_group = self.xml_node.get('INDEX_IN_GROUP')
		
	def to_string(self):
		ret= 'Member Name='+self.name
		if self.id != None:
			ret+=' ID='+self.id
		if self.type != None:
			ret = ret+'\ttype='+self.type
		if self.index_in_group != None:
			ret = ret+'\tIndex_in_group='+self.index_in_group
			
		return ret