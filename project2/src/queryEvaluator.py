from queryObject import *
import sys


# defines usage for file
def usage():
    sys.stderr.write("Usage: python queryEvaluator.py [query.txt] [config.txt]\n")

# opens up both files if it exists
def read_files(file1,file2):
	# open query file
	try:
		q = open(file1,'r')
	except:
		print "Query file not found"
		print file1
		sys.exit(1)

	# open config file
	try:
		c = open(file2,'r')
	except:
		print "Config file not found"
		print file2
		sys.exit(1)
	return q, c

def processQuery(line,identifier):
	print line,identifier
	f = open("output_file{}".format(identifier),'w')
	for num in line:
		f.write(str(num) + " ")
	f.write('\n')

def list_powerset(lst):
    return reduce(lambda result, x: result + [subset + [x] for subset in result],
                  lst, [[]])

# main function
if __name__ == "__main__":
	if len(sys.argv)!=3:
		print "Improper use of file!"
		usage()
		sys.exit(1)
	q,c = read_files(sys.argv[1],sys.argv[2])
	# parse config file and store specs for config in dictionary
	configArr = {}
	for line in c.read().split('\n'):
		line = line.split()
		if len(line) == 3:
			configArr[line[0]] = line[2]
	# print configArr

	# read every line in q and output a file for it
	lines = q.read().split('\n')
	for i in range(len(lines)):
		line = lines[i]
		line = line.split()
		if len(line) != 0:
			processQuery(line,i)

	# creating the power set for each line 
	for i in range(len(lines)-1):
		lineArr = []
		S =[]
		line = lines[i]
		line = line.split()
		# making S into QueryObjects 
		for j in range(len(line)):
			temp = QueryObject(float(line[j]),j)
			lineArr.append(temp)
		# constructing the powerset
		A = list_powerset(lineArr)
		A.pop(0)
		# making the elements of the powerset into QueryNodes
		for k in range(len(A)):
			s = QueryNode(A[k])
			S.append(s)
		print i
		for l in range(len(S)):
			print l
			S[l].displayArr()










