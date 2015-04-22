class QueryObject:
	def __init__(self, selectivity,identifier):
		self.selectivity = selectivity
		self.identifier = identifier
	
	def getTerm(self):
		return "t{0}[o{0}[i]]".format(self.identifier)

	def __str__(self):
		return "[[{1}]->selectivity={0}]".format(self.selectivity, self.identifier)

class QueryNode:
	def __init__(self, arr):
		self.left = None
		self.right = None
		self.numSubterms = len(arr)
		self.bestCost = 0
		self.hasNoBranch = False
		self.subterms = arr
		self.totalSelectivity = self.calcSelectivity(arr)

	def addLeft(self,left):
		self.left = left

	def addRight(self,right):
		self.right = right

	def calcSelectivity(self,arr):
		selectivity = 1
		for item in arr:
			selectivity = selectivity * item.selectivity
			# print item.selectivity
		return selectivity

	def displayArr(self):
		for item in self.subterms:
			print item
		print self.bestCost

	def returnArr(self):
		return self.subterms

	def calculateLogAndCost(self, d):
		cost = 0 
		k = self.numSubterms
		if self.totalSelectivity <= 0.5:
			q = self.totalSelectivity
		else:
			q = 1 - self.totalSelectivity
		cost = k * d['r'] + (k-1)*d['l'] + k*d['f'] + d['t'] + \
				d['m']*q + self.totalSelectivity*d['a']
		return cost

	def calculateNoBranchCost(self, d):
		cost = 0
		k = self.numSubterms
		cost = k*d['r'] + (k-1)*d['l'] + k*d['f'] + d['a']
		return cost

	def checkIntersection(self,s2):
		ids_l1 = set(x.identifier for x in self.subterms)  # All ids in list 1
		intersection = [item for item in s2.subterms if item.identifier in ids_l1]
		if len(intersection) == 0:
			return 0
		else:
			return 1
			
	def calculateCmetric(self,d):
		k = self.numSubterms
		cost = k*d['r'] + (k-1)*d['l'] + k*d['f'] + d['t']
		first = (self.totalSelectivity - 1)/cost
		second = self.totalSelectivity
		return first, second 

	def calculateDmetric(self,d):
		k = self.numSubterms
		cost = k*d['r'] + (k-1)*d['l'] + k*d['f'] + d['t']
		first = cost
		second = self.totalSelectivity 
		return first, second
	
	def calculateBranchAndCost(self,s,d):
		k = self.numSubterms
		p = self.totalSelectivity
		if p < (1 - p):
			q = p
		else:
			q = 1 - p
		cost = k*d['r'] + (k-1)*d['l'] + k*d['f'] + d['t'] + \
			d['m']*q +  p*s.bestCost
		return cost


def generateCode(root):
	noBranch = findRightmost(root)
	if noBranch == None
	boolean = generateBoolean(root)
	# print boolean
	# noBranch = '(t1[o1[i]] & t2[o2[i]])'
	if not noBranch:
		return "if {0}".format(boolean)+"{\n\tanswer[j++]=i;\n}"
	else:
		return "if {0}".format(boolean)+"{\n\tanswer[j]=i;\n\tj+="+"{0};\n".format(noBranch)+"}"


def generateBoolean(root,identifier):
	# initate variables
	ans = ''
	right = None
	left = None
	noBranch = None

	if (not root.left) and (not root.right):
		ans += root.subterms[0].getTerm()
		if len(root.subterms) >1:
			for obj in root.subterms[1:]:
				ans += ' & ' + obj.getTerm()
			return '({})'.format(ans),noBranch
		else:
			return ans,noBranch

	#get left
	if root.left:
		left,noBranch = generateBoolean(root.left)
		ans += "{}".format(left)
		# get right
		if root.right:
			right,noBranch = generateBoolean(root.right)
			ans += " && {}".format(right)
		# print '{}'.format(ans)
		return '({})'.format(ans),noBranch
	else:
		right,noBranch = generateBoolean(root.right)
		ans += "{}".format(right)
		# print '( {} )'.format(ans)
		return '({})'.format(ans),noBranch


if __name__ == "__main__":
	q1 = QueryObject(.7,1)
	q2 = QueryObject(.5,2)
	q3 = QueryObject(.9,3)
	q4 = QueryObject(.1,4)

	# construct tree
	root = QueryNode([q1,q2,q3,q4])
	temp = QueryNode([q1])
	temp1 = QueryNode([q2,q3,q4])
	root.addLeft(temp)
	root.addRight(temp1)
	temp2 = QueryNode([q2])
	temp3 = QueryNode([q3,q4])
	temp1.addLeft(temp2)
	temp1.addRight(temp3)
	temp4 = QueryNode([q3])
	temp5 = QueryNode([q4])
	temp3.addLeft(temp4)
	temp3.addRight(temp5)

	print generateCode(root)

