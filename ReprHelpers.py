#auxillary functions for the representation functions
	
#only calls represent on things that are not functions
#this is important for keeping printing pretty
represent = lambda x: x if isinstance(x,str) else repr(x)

#maps the repsresent function to a lst
mapRepresent = lambda lst: map(lambda x:map(represent,x),lst)

#used when we only need the representation of everything in the list
mapString = lambda lst: map(repr, lst)

#all pairs(a,b) in the list become (a.b)
depair =lambda lst: map(lambda x:".".join(x), lst)

#reverses all the pairs in a list
twist = lambda lst: map(lambda x:(x[1],x[0]), lst)

#puts parenthesis around a string
paren = lambda x: "("+x+")"

#puts curly brackets around a string
curlyBrackets = lambda x: "{"+x+"}"

#applies all the functions in the list to the argument in listed order
def doto(lst,arg):
	for fun in lst:
		arg = fun(arg)
	return arg
