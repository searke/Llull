from MalformedExpression import *
from ComplexStatement import *
from Statement import *

class HornClause:
	""" Represents a horn clause"""

	def __init__(self, implied, implier):
		"takes two Statements an implied one and an implier"
		self.Implied = implied
		self.Implier = implier

		#make sure it is well formed
		fails = lambda x: not(isinstance(x,ComplexStatement) or \
								isinstance(x,Statement))
		if(fails(implied)):
			raise MalformedExpression(implied + " must be a Statement of some kind")

		if(fails(implier)):
			raise MalformedExpression(implier + " must be a Statement of some kind")

	def __repr__(self):
		return repr(self.Implied) + " :- " + repr(self.Implier)
	
