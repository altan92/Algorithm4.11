Alfred Tan (avt2123) and Tommy Inouye (ti2181)

There is no need for the makefile. To run the program, use 'python queryEvaluator.py query.txt config.txt' 

The queryObject.py has two objects: QueryObject and QueryNode. The QueryObject is essentially the basic term, but it stores the selectivity of that term and has an identifier which becomes useful later on for functions such as intersection and union. It also contains a function that translates the basic term into C code corresponding with the t array and the o offsets. 

The QueryNode is essentially the record and is a subset of the basic terms. It contains all the values that is needed for the record including the left and right child which would also store QueryNodes. The three different cost functions are stored within this QueryNode object, but calculateBranchAndCost is a little different because it also takes a QueryNode as an object. This is necessary in order to obtain the value for C in the cost function which is basically the QueryNode's best cost. The intersection is similar because it also takes a QueryNode as an argument and outputs a 0 if the intersection between the two QueryNodes is the empty set. This means the QueryNodes do not have matching basic terms. The c-metric and d-metric are also calculated within the QueryNode object. The output of the C code is mainly done through the generateCode and generateBoolean functions. These functions are traversing a tree of QueryNodes and the terms in the nodes are joined via & while the leaves are joined via &&. The checkRightmost function is used for implementing no branch and finds the rightmost &-term so that it could output C code for that term using no branch if the no branch bit flag is set to True. 

The queryEvaluator.py file is where the reading, writing, and the algorithm is implemented. In the main function, the config.txt is read in as a dictionary and the query.txt is read in line by line to be proccesed in the function processQuery. The processQuery function implements Algorithm 4.11 and its two stages. Important things to note are the use of QueryObjects as the basic terms and the QueryNodes as the collection of the QueryObjects. Thus, each element in the power set is a QueryNode. Since we implemented it this way, the union in Stage 2 is a little tricky because we don't use a hash-key value to obtain the records. Thus, we have to create a for loop through S and match the union with the correct QueryObject in S and then we can finally update that record. Finally, after all the processing has finished, the optimal plan can be generated into C code. 

Here is an example using the branch misprediction code on 0.5 0.5 0.5 0.5:

Elapsed time: 1.220117092 seconds
CPU Cycles:           3565115752 
Instructions:         4781639625 
IPC:                  1.341230
Branch misses:        2289608 
Branch instructions:  205640710 
Branch mispred. rate: 1.113402%

overall selectivity = 0.063227720
theoretical selectivity = 0.062500000
