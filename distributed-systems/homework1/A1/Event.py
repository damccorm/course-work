# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 18:07:23 2018

@author: dongg
"""

import time
import json

class Event:
 
	# initializer to define content based event
   # construct infor1 which contains weather information 
   # construct infor2 which contains traffic information
	def __init__(self, content, information1 = 'weather', information2 = 'traffic', target, history, createdAt = time.time()):
		self.content = content
		self.information1 = information1
      self.information = information
      self.target = target
      self.record = {target : content}
      self.history = []
		self.createdAt = time.time()
      
	
	def serialize(self):
		msg = {'content':self.content,'information1':self.information1,'information2':self.information2, 'target': self.target, 'createdAt':self.createdAt}
		return msg
		

	def __str__(self):
		return {'content':self.content,'information1':self.information1,', 'information2':self.information2, 'target':self.target,'createdAt':self.createdAt}.__str__()

	@staticmethod
	def deSerialize(msg):
		
		return Event(msg['content'],msg['information1'],msg['information2'], msg['target'])
