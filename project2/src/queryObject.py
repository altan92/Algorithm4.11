class QueryObject:
	def __init__(self, selectivity,identifier):
		self.selectivity = selectivity
		self.identifier = identifier
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

	def addLeft(left):
		self.left = left

	def addRight(right):
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
	def calculateLogAndCost(self, dict):
		cost = 0 
		k = self.numSubterms
		if self.totalSelectivity <= 0.5:
			q = self.totalSelectivity
		else:
			q = 1 - self.totalSelectivity
		cost = k * dict['r'] + (k-1)*dict['l'] + k*dict['f'] + dict['t'] + \
				dict['m']*q + self.totalSelectivity*dict['a']
		return cost

	def calculateNoBranchCost(self, dict):
		cost = 0
		k = self.numSubterms
		cost = k*dict['r'] + (k-1)*dict['l'] + k*dict['f'] + dict['a']
		return cost
	



if __name__ == "__main__":
	q1 = QueryObject(.7,1)
	q2 = QueryObject(.5,2)

	temp = QueryNode([q1,q2])
	print temp.totalSelectivity
	print temp.numSubterms
	temp.displayArr()
	print
	print temp.returnArr()

