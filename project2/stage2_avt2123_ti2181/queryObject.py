from copy import deepcopy
#a basic term with a selectivity and an identifier
class QueryObject:
	def __init__(self, selectivity,identifier):
		self.selectivity = selectivity
		self.identifier = identifier
	#construct C code for the basic term
	def getTerm(self):
		return "t{0}[o{0}[i]]".format(self.identifier+1)
	#string representation
	def __str__(self):
		return "[[{1}]->selectivity={0}]".format(self.selectivity, self.identifier)

#a list of the basic terms which is considered a record
class QueryNode:
	def __init__(self, arr):
		self.left = None
		self.right = None
		self.numSubterms = len(arr)
		self.bestCost = 0
		self.hasNoBranch = False
		self.subterms = arr
		self.totalSelectivity = self.calcSelectivity(arr)

	#produce the combined selectivity of the basic terms
	def calcSelectivity(self,arr):
		selectivity = 1
		for item in arr:
			selectivity = selectivity * item.selectivity
			# print item.selectivity
		return selectivity
	#prints out the basic terms
	def displayArr(self):
		for item in self.subterms:
			print item
		print self.bestCost
	#returns the list of basic terms
	def returnArr(self):
		return self.subterms
	#calculate the logical and cost
	def calculateLogAndCost(self, d):
		cost = 0 
		k = self.numSubterms
		#make sure it's the correct selectivity
		if self.totalSelectivity <= 0.5:
			q = self.totalSelectivity
		else:
			q = 1 - self.totalSelectivity
		cost = k * d['r'] + (k-1)*d['l'] + k*d['f'] + d['t'] + \
				d['m']*q + self.totalSelectivity*d['a']
		return cost
	#calculate the no branch cost
	def calculateNoBranchCost(self, d):
		cost = 0
		k = self.numSubterms
		cost = k*d['r'] + (k-1)*d['l'] + k*d['f'] + d['a']
		return cost
	#calculate the intersection between two lists of basic terms
	#outputs 0 if the intersection is the empty set
	def checkIntersection(self,s2):
		ids_l1 = set(x.identifier for x in self.subterms)  # All ids in list 1
		intersection = [item for item in s2.subterms if item.identifier in ids_l1]
		if len(intersection) == 0:
			return 0
		else:
			return 1
	#calculate the c metric of a QueryNode	
	def calculateCmetric(self,d):
		k = self.numSubterms
		cost = k*d['r'] + (k-1)*d['l'] + k*d['f'] + d['t']
		first = (self.totalSelectivity - 1)/cost
		second = self.totalSelectivity
		return first, second 
	#calculate the d metric of a QueryNode
	def calculateDmetric(self,d):
		k = self.numSubterms
		cost = k*d['r'] + (k-1)*d['l'] + k*d['f'] + d['t']
		first = cost
		second = self.totalSelectivity 
		return first, second
	#calculate the branch and cost
	def calculateBranchAndCost(self,s,d):
		k = self.numSubterms
		p = self.totalSelectivity
		#choose the minimum value of p and 1-p
		if p < (1 - p):
			q = p
		else:
			q = 1 - p
		# pc = p*s.bestCost
		cost = k*d['r'] + (k-1)*d['l'] + k*d['f'] + d['t'] + \
			d['m']*q +  p*s.bestCost
		return cost

# check most rightmost node to see if no branch. If so remove it
def checkRightmost(realRoot,root):
	# check if root only node
	if not root:
		return realRoot,None
	if not root.right:
		# only node
		if root.hasNoBranch:
			ans = ''
			ans += root.subterms[0].getTerm()
			if len(root.subterms) > 1:
				for obj in root.subterms[1:]:
					ans += ' & ' + obj.getTerm()
			if not root.left:
				return None, '({})'.format(ans)
			else:
				return realRoot.left, '({})'.format(ans)
		else:
			return realRoot,None

	#traverses to the right hand side of the tree
	temp = realRoot
	while root.right:
		root = root.right
		if root.right:
			temp = temp.right
	if root.hasNoBranch:
		#set pointer to node to none
		temp.right = None
		ans = ''
		ans += root.subterms[0].getTerm()
		if len(root.subterms) > 1:
			for obj in root.subterms[1:]:
				ans += ' & ' + obj.getTerm()
		return realRoot, '({})'.format(ans)
	else:
		return realRoot,None


def generateCode(root, line):
	intro = '==================================================================\n'
	intro += ' '.join(str(x) for x in line) 
	intro += '\n------------------------------------------------------------------\n'

	# check for no branch
	# find identifier of rightmost node
	dash = '------------------------------------------------------------------\ncost: ' + str(root.bestCost)
	root, noBranch = checkRightmost(root,deepcopy(root))
	if root:
		boolean = generateBoolean(root)
	else:
		if not noBranch:
			return None
		else:
			return intro + "answer[j] = i;\nj += "+"{0};\n\n".format(noBranch)+ dash
	
	# print boolean
	# noBranch = '(t1[o1[i]] & t2[o2[i]])'
	dash = '------------------------------------------------------------------\ncost: ' + str(root.bestCost)
	if not noBranch:
		return intro + "if{0}".format(boolean)+" {\n\tanswer[j++] = i;\n}\n" + dash
	else:
		return intro + "if{0}".format(boolean)+" {\n\tanswer[j] = i;\n\tj += "+"{0};\n".format(noBranch)+"}\n" + dash
	

def generateBoolean(root):
	# initate variables
	ans = ''
	right = None
	left = None
	

	if (not root.left) and (not root.right):
		ans += root.subterms[0].getTerm()
		if len(root.subterms) >1:
			for obj in root.subterms[1:]:
				ans += ' & ' + obj.getTerm()	
		return ans

	#get left
	if root.left:
		left = generateBoolean(root.left)
		ans += "{}".format(left)
		# get right
		if root.right:
			right = generateBoolean(root.right)
			ans += " && {}".format(right)
		# print '{}'.format(ans)
		return '({})'.format(ans)
	else:
		right = generateBoolean(root.right)
		ans += "{}".format(right)
		# print '( {} )'.format(ans)
		return '({})'.format(ans)


if __name__ == "__main__":
	q1 = QueryObject(.7,1)
	q2 = QueryObject(.5,2)
	q3 = QueryObject(.9,3)
	q4 = QueryObject(.1,4)

	# construct tree
	root = QueryNode([q1,q2,q3,q4])
	temp = QueryNode([q1])
	temp1 = QueryNode([q2,q3,q4])
	root.left = temp
	root.right = temp1
	temp2 = QueryNode([q2])
	temp3 = QueryNode([q3,q4])
	temp1.left = temp2
	temp1.right = temp3
	temp4 = QueryNode([q3])
	temp5 = QueryNode([q4])
	temp3.left = temp4
	temp3.right = temp5

	print generateCode(root)

