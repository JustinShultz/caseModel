""" 
blocks.py contains the Block Class

Each Block has:
	(.name) string identifying the block's name (or ID)
	(.m) material, defined in materials.py
	(.state) physical state
	(.F) list of fluxes, which return a dictionary
	(.S) list of sources, which return a dictionary
		Sources and Fluxes do not need to be ordered 
		since they are never explicitly globally unwrapped
	(.t) time
	(.T) Time function, returns dict of coefficient on time terms

The equation for the block is
R(state) = Sum(Fluxes(state)) + Sum(Sources(state)) = 0
In the unsteady case
d/d(state) = R(state)

All blocks are connected through fluxes, defined in flux.py

These are blocks rather than volumes as they have no geometric info
All geometric info is in the fluxes, which are effectively
boundary conditions on the blocks
------------------------------------
function tests are run by doctest
python blocks.py

"""
import materials 
import numpy as np
from collections import OrderedDict
from math import log, pi

class Block(object):
	""" 
	Block Class

	__init__: 	Object Constructor

	input(s):   (s) string corresponding to block name
							(m) material
							(t) time
							(initialStates) Optional key-value pairs for
								 			 initial conditions
	output(s):	None
	"""

	def __init__(self,s,material,t = 0,**initialStates):
		self.name = s
		self.m = materials.__dict__.get(material,0)
		self.state = OrderedDict(initialStates)
		self.F = []
		self.S = []	
		self.t = t
		self.T = lambda state : dict([(s,1) for s in state])

	"""
	addFlux:
	addSource: Block Setup Functions

	input(s):  (F,S) Flux objects, Source objects
	output(s): None

	these functions don't add anything new, but make
	building blocks easier using addFlux/addSource instead
	of directly modifying the lists
	"""
	def addFlux(self,F):
		self.F.append(F)
		F.B = self

	def addSource(self,S):
		self.S.append(S)

	"""
	R: Residual function

	input(s):  None
	output(s): dict of states and residuals corresponding to state

	sums over sources and fluxes to calculate the residual
	"""
	def R(self):
		# print "printing block R"
		# self.printMe()
		# # print [F.F() for F in self.F]
		# # print [S.S(self) for S in self.S]
		R = OrderedDict([(s,0) for s in self.state])
		for d in [F.F() for F in self.F]+[S.S(self) for S in self.S]:
			for s in d:
				R[s] += d[s]
		return R
		# return reduce(lambda x, y: dict((k, v + y.get(k,0)) for k, v in x.iteritems()), \
		# 	[F.F() for F in self.F] + [S.S(self) for S in self.S])

	def printMe(self):
		print self.name, [s + '=' + str(self.state[s]) for s in self.state], self.m['name']


if __name__ == "__main__":
    import doctest
    doctest.testmod()
