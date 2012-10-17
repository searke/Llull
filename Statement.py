from ReprHelpers import *
from MalformedExpression import *
from LogicHelpers import *
from ComplexStatement import *
import copy

class Statement:
	"""Represents a Statement as long as they aren't/
		 joined with logic operators"""
	#notes: The use of the None keyword as any of the theta marked arguments
	# is exactly the same as deleting that theme	

	def __init__(self, pred, argdict):
		" Takes a predicate and a dictionary of format Theme -> Argument"
		#	Initialize the predicate and the Map of type Themes->Arguments
		self.Pred		= pred
		self.ArgDict	= argdict
		self.primedTheme= None
		self.VariableMap= {}
		
		# Make sure the Statement is well formed
		self.checkForForm()
		
		# A dictionary that helps us handle variables which all start 
		# with a question mark Map of type Variable -> list of Themes
		self.setVariableMap()
	
	#TODO in theory complex statements should be allowed to be arguments as well
	def checkForForm(self):
		"raises an error if self is not well formed"
		if not isinstance(self.Pred, str):
			raise MalformedExpression("Predicate must be a String")
		
		#check everytheme and argument for wellformedness
		for theme in self.ArgDict.keys():
			if not isinstance(theme, str):
				raise MalformedExpression("Themes must be strings")
			arg = self.ArgDict[theme]
			if not(isinstance(arg,str) or isinstance(arg,Statement)):
				raise MalformedExpression("Arguments must be strings" + \
												" or Statements")

	def setVariableMap(self):
	 	"Sets up the Statements internal Map which takes  care of variables.\
			Assumes that the Statement is well formed"
		self.VariableMap = {}
		for theme in self.ArgDict.keys():
			arg = self.ArgDict[theme]
			#if its a variable
			if "?" in arg[:2] and isinstance(arg,str):
				
				#if its already in the map
				if arg in self.VariableMap:
					#append this theme to the list it points to
					self.VariableMap[arg].append(theme)
				#else we need to add a single elemnt list with this to the Map
				else:
					self.VariableMap[arg] = [theme]

	#TODO make leftrepresent
	def __repr__(self):
		operations = [mapRepresent, depair, ", ".join, paren]
		return self.Pred + doto(operations, self.ArgDict.items())
	
	def __eq__(self, stmnt):
		if not isinstance(stmnt,Statement):
			return 0
		else:
			#inefficent hack
			return And([ self.implies(stmnt), stmnt.implies(self)])

	def __getitem__(self, theme):
		return self.ArgDict.get(theme)

	def __setitem__(self,theme, arg):
		self.ArgDict[theme]=arg
		#test to see if its a variable. If so reset the VariableMap
		if isinstance(arg,str) and "?" in arg[:2]:
			self.setVariableMap()

	#type: stmnt -> trinary
	def implies(self, stmnt):
		"returns wether a statement implies another for use in unification"
		#if the predicates do not match return 1 since they don't tell us
		# anything about each other
		if(self.Pred!=stmnt.Pred):
			return 1
		
		#simpleStmnt->simpleStmnt Case		
		if isinstance(stmnt, Statement):
			"returns  2 if this statement implies the other other one else 1"
			#all themes in stmnt
			for theme in stmnt.ArgDict.keys():
				#self's arg
				thisArg = (self.ArgDict.get(theme))
				#stmnt's arg
				Arg		= (stmnt.ArgDict.get(theme))
			
				#if were testing a variable
				if Arg in stmnt.VariableMap.keys():
					#get a list of all the themes that variable is part of
					themeLst = stmnt.VariableMap[Arg]
					# Make a list of all the argument values of those themes
					# in this statement
					ArgLst = map(lambda x:self[x], themeLst)
					# Check to see everything in that list is equal
					# this works because we can assume that none of the args
					# are boolean values
					allequal = lambda lst: reduce(lambda x,y:x&y,\
											map(lambda x:x==lst[0], lst))
					if not allequal(ArgLst):
						return 0
				
				#if were testing against a variable
				if thisArg in self.VariableMap.keys():
					#get a list of all themes that the variable is a part of
					themeLst = self.VariableMap[thisArg]
					# Make a list of all the argument value of those themes
					# in stmnt
					ArgLst = map(lambda x:stmnt[x], themeLst)
					#Check to see everything in that list is equal
					# this works because we can assume that one of the items
					# in the list are boolean values
					allequal = lambda lst: reduce(lambda x,y:x&y,\
											map(lambda x: x==lst[0], lst))
					if not allequal(ArgLst):
						return 0
			  
				# if were not testing a variable
				if thisArg not in self.VariableMap.keys() and \
					Arg not in stmnt.VariableMap.keys():
					if Arg!=thisArg:
						return 1
			
			#if everything checks out return true				
			return 2
		#handle case where it is a ComplexStatement
		else:
			#unary case
			if(stmnt.Operator in UnaryOp):
				return stmnt.Operator(self.implies(stmnt.Stmnts))
			#binary case
			else:
				return stmnt.Operator( map (self.implies, stmnt.Stmnts))

	#TODO this should also subsitute variables in arguments which are 
	# simple or complex statements themselves
	def variableSub(self, subMap):
		"""returns a statement based on self where the variables have been 
			subsituted with the values specifed in the inputed Map
			type: (map from variable to value) -> Statement"""
		#create a copy of our Statement
		returned = copy.deepcopy(self)
		
		#for every variable specified in the input map
		for variable in subMap.keys():
			# get all the themes it corresponds to
			if variable in returned.VariableMap.keys():
				themes = returned.VariableMap[variable]
				#set all of the themes to the variable specificed
				for theme in themes:
					if theme in returned.ArgDict.keys():
						returned[theme] = subMap[variable]
		return returned
