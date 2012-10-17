#import everything through environment
from Environment import *

AND = lambda x,y: ComplexStatement(And,[x,y])
OR  = lambda x,y: ComplexStatement(Or,[x,y])
NOT = lambda x: ComplexStatement(Not,x)

