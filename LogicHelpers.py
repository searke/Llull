
# performs logic on integers, Intended to be used for trinary
# 0 = false
# 1 = maybe
# 2 = true

# logical AND. The same an min x,y
And = lambda lst: reduce(lambda x,y: x if x<y else y, lst)

#logical OR. the same as max x,y
Or = lambda lst: reduce(lambda x,y: x if x>y else y, lst)

def Not(arg):
	if(arg==0):
		return 2;
	if(arg==2):
		return 0;
	else:
		return arg;

#maps between operators and their prefered representation
BinaryOp = {And:" & ", Or:" | "}
UnaryOp = {Not:" ! "}

# A Map that gives us the compliment of the binary operator
Compliment = {And:Or, Or:And}
