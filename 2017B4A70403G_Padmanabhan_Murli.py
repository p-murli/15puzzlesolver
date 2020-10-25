#!/usr/bin/env python3
import time
import random
import numpy
from heapq import * # See heapq_test.py file to learn how to use. Visit : https://docs.python.org/3/library/heapq.html
# import pprint
# pp = pprint.PrettyPrinter(indent=4)
### Don't use fancy libraries. Evaluators won't install fancy libraries. You may use Numpy and Scipy if needed.
### Send an email to the instructor if you want to use more libraries.


# ********************************************************************


#                 YOUR CODE SHOULD GO HERE.

#                 WRITE YOUR CODE IN AN EASY TO READ MANNER.

#                 YOU MAY USE SEVERAL CLASSES AND FUNCTIONS 


#                 MODIFY THE BODY OF THE FUNCTION FindMinimumPath()


def swap(state, x,y, zerox, zeroy):

	'''
	Function that takes in the current state, the position of zero, and the position to swap with.

	Returns the state with the positions swapped
	'''

	l = list(state)

	pos = 4*x+y
	zpos = 4*zerox+zeroy

	l[pos], l[zpos] = l[zpos], l[pos]

	return ''.join(l)


def makepath(state, parents):

	'''
	
	Function that takes in the goal state and the parents dictionary.
	It generates the whole path and returns it as a list

	'''

	ans = []
	p = parents[state]



	while(p[0]!= -1):
		# if(len(ans)>1000):
		# 	break
		ans.append(p[1])
		p = parents[p[0]]


	return ans[::-1]

def shows(state):

	'''
	function to print the board at any time, i.e. the current state
	Note : have to import pprint library for this to work
	'''
	s = []
	for i in range(4):
		s.append(list(state[4*i:4*i+4]))

	pp.pprint(s)
	print("------------------------------")

def astar(initialstate, goalstate):

	
	'''
	Function that runs the astar algorithm.
	Takes in the initial state and the final state as input.

	Returns the minimum path and the number of nodes generated.

	Any node in the Heap is of this form
	node = [F value, state as string, parent, x, y, direction, moves_done]

	heap = heap data structure to store nodes and retrieve them
	visited = set data structure to store the visited nodes

	parents = dictionary data structure to store parent child relationships and generate minpath



	'''


	heap = []
	visited = set()
	
	minpath= []
	nodesGenerated = 1

	parents = dict()

	k = initialstate.index('0')
	zx = k//4
	zy = k%4

	root = [manhattan_heuristic(initialstate), initialstate, -1, zx,zy, -1, 0]

	parents[initialstate] = -1
	#print(root)
	heappush(heap, root)


	while(len(heap)!=0):

		Fvalue, state, parent, zx, zy, direction,moves = heappop(heap)
		

		visited.add(state)
		parents[state] = (parent, direction)

		if(state == goalstate):
			break

		

		dirs = [[1,0,'Down'],[0,1,'Right'],[-1,0,'Up'],[0,-1,'Left']]
		
		for d in dirs:

			newx = zx + d[0]
			newy = zy + d[1]

			if(newx>=0 and newx<4 and newy>=0 and newy<4):

				child = swap(state, newx, newy, zx, zy)
				
				if(child in visited):
					continue
				#childF = Fvalue + 1 - manhattan_heuristic(state) + manhattan_heuristic(child)

				childF = moves + 1 + manhattan_heuristic(child)
				childnode = [childF, child, state, newx, newy, d[2],moves+1]

				heappush(heap, childnode)
				nodesGenerated +=1

	minpath = makepath(goalstate, parents)

	return minpath, nodesGenerated

def manhattan_heuristic(state):
    """

    Takes in the current state 
    Returns the Manhattan distance to the goal state.
    """  
    distance = 0

    for idx, num in enumerate(state):
    	if(num=='0'):
    		continue
    	num = int(num,16)

    	distance += abs(idx//4 - num//4) + abs(idx%4 -num%4)

    return distance


def misplaced_heuristic(state):

	"""

    Takes in the current state 
    Returns the number of tiles that are misplaced
    """ 

	distance=0

	for idx, num in enumerate(state):

		if(num=='0'):
			continue

		num = int(num, 16)

		if(idx != num):
			distance +=1

	return distance


def manhattan_with_linear_conflicts(state):

	"""

    Takes in the current state 
    Returns the Manhattan distance + Linear conflict heuristic

    """ 

	total = manhattan_heuristic(state)
	solved = "0123456789ABCDEF"
	total += linear_conflicts(state, solved)

	return total



def linear_conflicts(candidate, solved):

	"""

    Takes in the current state and goal state
    Returns the linear conflicts in  the current state

    """ 

	count=0
	ans =0
	for i in range(4):

		solvedrow = [k for k in range(4*i, 4*i+4)]
		#print(solvedrow)
		for c1 in range(4*i,4*i+4):
			for c2 in range(c1+1, 4*i+4):
				#print(candidate[c1], candidate[c2])
				if(int(candidate[c1], 16) in solvedrow and int(candidate[c2], 16) in solvedrow and candidate[c1]>candidate[c2]):
					#print(" lin conflict bw ", c1, c2)
					count+=1

				#print(candidate[c1], candidate[c2], solved[i], solved[c2])

		#print("row done")

	ans += count*2

	count = 0
	for i in range(4):
		solvedcol = [i+4*k for k in range(4)]
		#print(solvedcol)
		currcol = [candidate[i+4*k] for k in range(4)]
		#print(currcol)
		for r1 in range(4):
			for r2 in range(r1+1, 4):
				#print(currcol[r1],currcol[r2])
				if(int(currcol[r1], 16) in solvedcol and int(currcol[r2], 16) in solvedcol and int(currcol[r1], 16)>int(currcol[r2], 16)):
					#print(" lin conflict bw ", r1, r2)
					count+=1

	ans += count*2

	#print(ans)
	return ans




def FindMinimumPath(initialState,goalState):
    minPath=[] # This list should contain the sequence of actions in the optimal solution
    nodesGenerated=0 # This variable should contain the number of nodes that were generated while finding the optimal solution
    
    ### Your Code for FindMinimumPath function
    ### Write your program in an easy to read manner. You may use several classes and functions.
    ### Your function names should indicate what they are doing
    
    
    ### Your Code ends here. minPath is a list that contains actions.
    ### For example, minPath = ['Up','Right','Down','Down','Left']

    
    #print(initialState)

    initstate = ""
    endstate = ""

    #Convert the states to string for speed
    for i in initialState:
    	for j in i:
    		initstate += j

    for i in goalState:
    	for j in i:
    		endstate += j

    #print(initstate, endstate)
   	
    minPath, nodesGenerated = astar(initstate,endstate)
    
    return minPath, nodesGenerated



#**************   DO NOT CHANGE ANY CODE BELOW THIS LINE *****************************


def ReadInitialState():
    with open("initial_state2.txt", "r") as file: #IMP: If you change the file name, then there will be an error when
                                                        #               evaluators test your program. You will lose 2 marks.
        initialState = [[x for x in line.split()] for i,line in enumerate(file) if i<4]
    return initialState

def ShowState(state,heading=''):
    print(heading)
    for row in state:
        print(*row, sep = " ")

def main():
    initialState = ReadInitialState()
    ShowState(initialState,'Initial state:')
    goalState = [['0','1','2','3'],['4','5','6','7'],['8','9','A','B'],['C','D','E','F']]
    ShowState(goalState,'Goal state:')
    
    start = time.time()
    minimumPath, nodesGenerated = FindMinimumPath(initialState,goalState)
    timeTaken = time.time() - start
    
    if len(minimumPath)==0:
        minimumPath = ['Up','Right','Down','Down','Left']
        print('Example output:')
    else:
        print('Output:')

    print('   Minimum path cost : {0}'.format(len(minimumPath)))
    print('   Actions in minimum path : {0}'.format(minimumPath))
    print('   Nodes generated : {0}'.format(nodesGenerated))
    print('   Time taken : {0} s'.format(round(timeTaken,4)))

if __name__=='__main__':
    main()
