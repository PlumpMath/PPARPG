#!/usr/bin/python
# -*- coding: utf8 -*-

from pandac.PandaModules import * 

from direct.task import Task
from direct.interval.IntervalGlobal import *
from direct.fsm.FSM import FSM

import sys, random

from gui import *

class Dialog:
	def __init__(self, gm, name):
		self.gm = gm # game map
		self.playerData = gm.player.data
		
		self.name = name
		self.gui = DialogGui(0,-0.5,name)
		self.intro()
		
	def destroy(self, args=[]):
		self.gui.destroy()
		self.gm.dialog = None
		
	def setMainText(self, text):
		self.gui.setMainText(text)
	
	def setMenu(self, menu):
		self.gui.setMenu(menu)
		
	def intro(self):
		msg1 = "'Hello, " + self.name + "!'"
		msg2 = "'So " + self.name + " is your name, huh?'"
		
		menu = [
			[msg1, self.l_hello, []],
			[msg2, self.l_askName, []],
			["Close", self.destroy, []],
		]
		self.setMenu(menu)
		return 1
		
	def l_hello(self, args=[]):
		msg1 = "Hi there, " + self.playerData["name"] + "..."
		self.setMainText(msg1)
		self.l_close()
		return 1
		
	def l_askName(self, args=[]):
		msg1 = self.name + " looks at you for a moment.\n\n" + self.name + " : 'That's my name, why do you care?'"
		self.setMainText(msg1)
		self.l_close()
		return 1
		
	def l_close(self, args=[]):
		menu = [["Close", self.destroy, []]]
		self.setMenu(menu)
		return 1
		
class DialogCamilla(Dialog):
	def __init__(self, gm):
		Dialog.__init__(self, gm, "Camilla")

	def getQuestValue(self):
		if self.name not in self.playerData:
			return 0
		else:
			return self.playerData[self.name]
			
			
		
	def intro(self):
		msg1 = "'Hello, " + self.name + "!'"
		msg2 = "'Camilla, you seem to know a lot of stuff about what's going on here...'"
		
		menu = [
			[msg1, self.l_hello, []],
			[msg2, self.l_askStuff, []],
			["Close", self.destroy, []]
		]
		self.setMenu(menu)
		return 1
		
	def l_hello(self, args=[]):
		if self.getQuestValue()>0:
			msg = "Camilla : '... hello again, " + self.playerData["name"] + "...'"
		else:
			msg = "Camilla : 'Oh hello there, young " + self.playerData["name"] + ".'"
			self.playerData[self.name] = 1
			
		self.setMainText(msg)
		self.l_close()
		return 1
		
	def l_askStuff(self, args=[]):
		if self.getQuestValue()>1:
			msg = "Camilla : 'Enough with that, i have no idea what you're talking\nabout!'"
			self.setMainText(msg)
			self.l_close()
		else:
			msg = "Camilla : 'A lot of stuff? what do you mean by that?'"
			self.playerData[self.name] = 1
			self.setMainText(msg)
			menu = [
				["'Come on, you know *exactly* what i'm talking about...'", self.l_insist, []],
				["'Ah, my bad, forget about that...'", self.l_close, []],
			]
			self.setMenu(menu)
		return 1
		
	def l_insist(self, args=[]):
		msg = "Camilla : 'No, really, i have no idea what you're talking about!'"
		self.playerData[self.name] = 2
		self.setMainText(msg)
		self.l_close();
		return 1
		
	
