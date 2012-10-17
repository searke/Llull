from ReprHelpers import *
from MalformedExpression import*
from ComplexStatement import *
from Statement import *
from HornClause import *

	#TODO debug

class Environment:
	"""Represents the current environment under which the computation is\
		being done"""
	
	def __init__(self, environment=None):
		self.Statements = environment.Statements if(environment) else []
		self.HornClauses = environment.HornClauses if (environment) else []

	def __repr__(self):
		show = lambda x: doto([mapString, ", ".join, curlyBrackets], x)
		return show(self.Statements) + " : " + show(self.HornClauses)
	
	def add(self, msg):
		"adds a simple/complex statement or hornclause to the environment"
		if isinstance(msg, HornClause):
			self.HornClauses.append(msg)
		elif(isinstance(msg,Statement) or isinstance(msg,ComplexStatement)):
			self.Statements.append(msg)
		else:
			raise MalformedExpression("only HornClauses and Statements" + \
										" may be added to an environment")

	def stmntsFor(self, statement):
		"""returns a list of all statements in the environment which are super
		statements of the argument statement"""
		proves = lambda x: x.implies(statement)==2
		return filter( proves, self.Statements)

	def stmntsAgainst(self, statement):
		"""returns a list of all statements disproving our statement"""
		disproves = lambda x: x.implies(statement)==0
		return filter( disproves, self.Statements)

	def clausesFor(self, statement):
		"""returns all horn clauses in the environment in the the implied
		part of the horn clause is a superStatement of the input"""
		implies = lambda x: x.Implied.implies(statement)==2
		return filter( implies, self.HornClauses)

	def clausesAgainst(self, statement):
		"returns all the horn clauses that imply that our statement is false"
		disproves = lambda x: x.Implied.implies(statement)==0
		return filter( disproves, self.HornClauses)

	#TODO were gonna need an inconsistant logic error
	
	def query(self,stmnt):
		result = self.unify(stmnt,[])
		if result[0]==2:
			print "Yes"
		elif result[0]==1:
			print "Dude, Iono..."
		elif result[0]==0:
			print "No"
			
		print result[1]	

	#acc is an accumulator for holding information for how it was unified
	# Assumes the model is logically consistant
	def unify(self, stmnt, acc=[]):
		"returns a pair of type trinary value and the contents of acc"
		
		#break up complex statements
		if isinstance(stmnt,ComplexStatement):
			if stmnt.Operator in UnaryOp:
				return stmnt.Operator(self.unify(stmnt.Stmnts))
			if stmnt.Operator in BinaryOp:
				return stmnt.Operator(map(self.unify,stmnt.Stmnts))
		
		#otherwise we have a simple statement
		proof = self.stmntsFor(stmnt)
		if proof:
			return (2,acc.append(proof))
		disproof = self.stmntsAgainst(stmnt)
		if disproof :
			return (0,acc.append(disproof))
		Hope4proof = self.clausesFor(stmnt)
		if Hope4proof :
			for hope in Hope4proof:
				result = self.unify(hope.Implier,[hope])
				if result[0]==2 :
					return (2,acc.append(result[1]))
		DespairOfDisproof = self.clausesAgainst(stmnt)	
		if DespairOfDisproof :
			for despair in DespairOfDisproof:
				result = self.unify(despair.Implier,[despair])
				if result[0]==2 :
					return(0,acc.append(result[1]))
		else:
			return (1,"Dude, Iono...")
