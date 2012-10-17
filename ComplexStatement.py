from MalformedExpression import *
from ReprHelpers import *
from Statement import *
from LogicHelpers import *


# Warning: Negation Leads to unexpected results in certain cases
class ComplexStatement:
	""" Represents a Statements with logical operators applied"""
	
	def __init__(self, operator, stmnts):
		"takes a unary operator and a stmnt, or an operator and list of stmnts"
		self.Operator = operator
		self.Stmnts = stmnts
		
		# make sure the input to our ComplexStatement is wellformed
		self.checkForForm()
	
	def checkForForm(self):
		#cs1 and cs2 are restricted to being a Statement or a Complex Statement
		fails = lambda x: not(isinstance(x,ComplexStatement) or \
							isinstance(x,Statement))
		
		if(not (self.Operator in BinaryOp or self.Operator in UnaryOp)):
			raise MalformedExpression("invalid operator given")
			
		#negation, !, is a unary operator
		if (self.Operator in UnaryOp) and fails(self.Stmnts) :
			raise MalformedExpression("! is a unary operator")

		#were dealing with binary operators
		elif(self.Operator in BinaryOp):
			#if anything in the list fails...
			if reduce(lambda x,y:x and y, map(fails,self.Stmnts)):
				raise(MalformedExpression("Requires list of Statements"))

	def __repr__(self):
		if(self.Operator in BinaryOp):
			operations = [mapString, BinaryOp[self.Operator].join, paren]
			return doto( operations, self.Stmnts)
		elif(self.Operator in UnaryOp):
			return paren(UnaryOp[self.Operator] + repr(self.Stmnts))

	def implies(self, stmnt):
		"""Returns a trinary value of wether or not this returns implies /
			the statement"""
		#first handle the simple case that it is a simple statement
		if(isinstance(stmnt,Statement)):
			#Unary cases
			if(self.Operator in UnaryOp):
				return self.Operator(self.Stmnts.implies(stmnt))
			#Binary cases
			else:
				SelfImplies = lambda x:x.implies(stmnt)
				return Compliment[self.Operator](map( SelfImplies, self.Stmnts))
	
		#Second handle the more complicated Statements
		elif(isinstance(stmnt,ComplexStatement)):
			#Unary cases
			if(stmnt.Operator in UnaryOp):
				return stmnt.Operator(self.implies(stmnt.Stmnts))
			#Binary cases
			return stmnt.Operator( map( self.implies, stmnt.Stmnts))

	def variableSub(self,subMap):
		"""returns a complex statement based on self where the variables have 
			been subsituted with the values specified in the inputed Map
			type: (map from variable to value) -> ComplexStatement"""
		if(self.Operator in UnaryOp):
			return ComplexStatement(self.Operator, \
									 self.Stmnts.variableSub(subMap))
		else:
			return ComplexStatement(self.Operator, \
									map( lambda x:x.variableSub(subMap),\
										self.Stmnts))
