####MAITRI SHASTRI 2014B2A70220P###############
from __future__ import division
from __future__ import absolute_import
import random

import sys
import time
import turtle

import heapq
import copy 

global number_nodes
global startarr
global startpos

global time_taken
global explored_states
explored_states=[]
global explored_states_greedy

global dim
global d 
global record_time
record_time=0
global record_time_roomsize
record_time_roomsize=0
global timearr
timearr=[]
global timearrroom
timearrroom=[]

#############DATA STRUCTURES###################
class PriorityQueue:

	def  __init__(self):
		self.heap = []
		self.count = 0

	def push(self, item, priority):
		# FIXME: restored old behaviour to check against old results better
		# FIXED: restored to stable behaviour
		entry = (priority, self.count, item)
		# entry = (priority, item)
		heapq.heappush(self.heap, entry)
		self.count += 1

	def pop(self):
		(_, _, item) = heapq.heappop(self.heap)
		#  (_, item) = heapq.heappop(self.heap)
		return item
	
	def isEmpty(self):
		return len(self.heap) == 0
	def size(self):
		return len(self.heap)	

class Stack:
	'''A container with LIFO property'''
	def __init__(self):
		self.list=[]
	def push(self,item):
		self.list.append(item)

	def pop	(self):
		return self.list.pop()
	def isEmpty(self):
		return len(self.list)==0
	def size(self):
		return len(self.list)	


#######RANDOM DIRT GENERATOR USING NUMPY#########################
'''generates a square matrix of p% 1s''' 
def dirtgenerator(p,d):

	
	if(p<=100 and p>=0):
		p_1=int(p/100*d*d)

		p_0=(d*d)-p_1
		arr=np.array([0]*p_0+[1]*p_1)
		np.random.shuffle(arr)
		final_arr=np.reshape(arr,(-1,d))
		return (final_arr)
	else:
		print("Invalid value of p")	
####################RANDOM DIRT GENERATOR WITHOUT USING NUMPY##################

def dirtgeneratorrandom(p,d):
        if(p<=100 and p>=0):
                numrange=d*d
                p_1=int(p/100*d*d)
                arr=[[0]*d for i in xrange(d)]
                l=xrange(0,d*d-1)
                listofnos=random.sample(l,p_1)
                for x in listofnos:
                        x_index=int(x/d)
                        y_index=x%d 
                        arr[x_index][y_index]=1
                return arr
        else:
                print("Invalid values of p")

###########START POSITION GENERATOR########
def startpositiongenerator():
	s=random.randint(1,5)
	if(s==1):
		startpos=[0,0]
	elif (s==2):
		startpos=[0,dim]
	elif(s==3):
		startpos=[dim,0]
	else :
		startpos=[dim,dim]
	return startpos



#######GUI#########################################################
'''black represents clean tile while yellow represents dirty tile'''
def turtlegraphicsroom(startgraphics):
	i=0
	j=0
	rt=turtle.Turtle()
	rt.setpos(0,0)
	xpos=0
	ypos=0
	rt.penup()
	for i in xrange(0,len(startgraphics)):
		xpos=0
		for j in xrange(0,len(startgraphics[0])):
			if(startgraphics[i][j]==0):
				
				
				
				rt.setpos(xpos,ypos)
				xpos=xpos+20

				rt.dot("black")
			else:

				
				
				
				
				rt.setpos(xpos,ypos)
				xpos=xpos+20
				rt.dot("yellow")
		ypos=ypos-20	

def turtlegraphics(actionseq,startpos,colorchoice):
	'''FUNCTION TO DISPLAY THE ACTION PATH USING 3 DIFFERENT COLOURS-RED FOR DFS ,BLUE FOR GREEDY SEARCHH2
		AND GREEN FOR GREEDY SEARCH H1'''

	rt=turtle.Turtle()
	
	rt.speed(1)
	rt.penup()
	posx=startpos[0]
	posy=startpos[1]
	if(posx==dim and posy==dim):
		posx=dim*20
		posy=-dim*20
	elif(posx==dim and posy==0):
		posy=-dim*20
		posx=0	
	elif(posx==0 and posy==dim):
		posx=dim*20	
		posy=0
	#print(posx,posy)
	rt.setpos(posx,posy)
	rt.pendown()
	if(colorchoice==1):
		rt.color("red")
	elif(colorchoice==2):
		rt.color("blue")
	elif(colorchoice==3):
		rt.color("green")		
	for act in actionseq:
		if(act=='up'):
			posy=posy+20
			rt.goto(posx,posy)
		elif(act=='down'):
			posy=posy-20
			rt.goto(posx,posy)
		elif(act=='right'):
			posx=posx+20
			rt.goto(posx,posy)
		elif(act=='left'):
			posx=posx-20
			rt.goto(posx,posy)
		elif(act=='suck'):
			rt.dot("blue")	
	time.sleep(5)		

		

#############NODE STRUCTURE#########################################
#DEFINES THE STRUCTURE OF THE NODE 
class Node:
	def __init__(self,state,parent,action,cost,depth):
		self.state=state
		self.parent=parent
		self.action=action
		self.cost=cost
		self.depth=depth
		
	def getState(self):
		return self.state
	def getParent(self):
		return self.parent
	def getAction(self):
		return self.action
	def getCost(self):
		return self.cost
	def getdepth(self):
		return self.depth
	def Setdepth(cost):
		self.depth=depth

#VACUUM STATE#########################################################
#VACUUM STATE IS MADE UP OF 2 ATTRIBUTES NAMELY:MATRIX AND VACUUM CLEANER POSITION
class Vacuumstate:
	def __init__(self,startingarr,startingpos):
		self.matrixstate=startingarr
		self.position=startingpos
		for i in xrange(0,len(startingarr)):
			for j in xrange (0,len(startingarr[0])):
				self.matrixstate[i][j]=startingarr[i][j]

	def isGoal(self):
		#CHECKS IF CURRENT STATE IS SAME AS GOAL STATE
		
		flag1=True
		flag2=False
		
		for row in xrange(0,len(self.matrixstate)):
			for col in xrange(0,len(self.matrixstate[0])):
				if(self.matrixstate[row][col]!=0):
					flag1=False
		if(self.position==[0,0] or self.position==[0,dim] or self.position==[dim,0] or self.position==[dim,dim]):
			flag2=True
		return (flag1 and flag2)
	
	def legalmoves(self):
		#RETURNS A LIST CONTAINING ALL ALLOWED MOVES
		moves=[]
		row=self.position[0]
		col=self.position[1]
		mat=self.matrixstate
		#print('row',row,col)
		#print('lenth',len(self.matrixstate))
		
		if(row!=0):
			moves.append('up')
		if(row!=dim):
			moves.append('down')
		if (col!=0):
			moves.append('left')
		if(col!=dim):
			moves.append('right')
		if(mat[row][col]==1):
			#print('appending to moves')
			moves.append('suck')	
		#print (moves)	
		return moves
	
	def result(self,move):
		#CREATES A LIST CONTAINING ALL ALLOWED STATES CORRESPONDING TO ALLOWED MOVES
		row=self.position[0]
		col=self.position[1]
		newrow=row
		newcol=col
		
		newmatrix=[[0]*d for i in xrange(d)]
		for i in xrange(0,d):
				for j in xrange(0,d):
					newmatrix[i][j]=self.matrixstate[i][j]
		
		if(move=='up'):
			newrow=row-1
		elif(move=='down'):
			newrow=row+1
		elif(move=='right'):
			newcol=col+1
		elif(move=='left'):
			newcol=col-1
		elif(move=='suck'):
			
			newmatrix[row][col]=0
			
		
		newstate=Vacuumstate(newmatrix,[newrow,newcol])	
		
		return newstate

	def __eq__(self,other):
		#OVERRIDES == OPERATOR TO CHECK FOR EQUALITY OF 2 STATES
		
		for row in xrange(0,d):
			for col in xrange(0,d):
				if(self.matrixstate[row][col]!=other.matrixstate[row][col]):
					return False
		if(self.position[0]!=other.position[0] or self.position[1]!=other.position[1]):
			return False
		return True	

	def __ne__(self,other):
		#OVERRIDES != OPERATOR TO CHECK FOR INEQUALITY OF 2 STATES
		dim=len(self.matrixstate)
		for row in xrange(0,d):
			for col in xrange(0,d):
				if(self.matrixstate[row][col]!=other.matrixstate[row][col]):
					return True
		if(self.position[0]!=other.position[0] or self.position[1]!=other.position[1]):
			return True


		return False

	def find(self):
		#RETURNS TRUE IF STATE IS ALREADY PRESENT IN LIST OF EXPLORED_STATES
		
		
		for other in explored_states:
			
			if( self==other):
				return True

		return False

	def getHashkey(self):
		###CAN BE USED TO IMPROVE TIME COMPLEXITY OF SEARCH OPERATION IN EXPLORED_STATES
		mat=self.matrixstate
		string=''
		numrows=len(mat)
		numcols=len(mat[0])
		for i in xrange(0,numrows):
			for j in xrange (0,numcols):
				if(mat[i][j]==1):
					string=string+'1'
				else :
					string=string+'0'			
		string=string+str(self.position[0])+str(self.position[1])
		return int(string)

				


###SEARCH PROBLEM DEFINITION#########################################################
###VACUUM PROBLEM IS DEFINED BY ITS INITIAL STATE AND KEEPS A TRACK OF NUMBER OF NODES
class vacuumproblem:
	def __init__(self,vinitialstate):
		
		
		self.startstate=vinitialstate
		self.number_nodes=0
		
	def Setnumber_nodes(self):
		self.number_nodes=self.number_nodes+1	
	def getnumber_nodes(self):
		return self.number_nodes	

	def getStartState(self):
		return self.startstate
		
	def isGoalstate(self,state):
		return state.isGoal()
	def getSuccessors(self,state):
		#USED TO GET A LIST OF TUPLES OF THE FORM(STATE,ACTION,COST)
		succ=[]
		for a in state.legalmoves():
			#print('inside the for loop of get suxxesors')
			if(a =='suck'):
				#print('Entering if condition for suck')
				succ.append((state.result(a),a,0))
				#print(state.result(a).position)
			else:
				#print('entering else part in get suxx')
				succ.append((state.result(a),a,2.0))
				#print(state.result(a).position)			
		return succ


	def expand(self,node):
		#CREATES NODES CORRESPONDING TO ALL SUCCESOR STATES RETURNED BY GETSUCCESORS FUNCTION
		nodeset=[]
		st=node.getState()
		succlist=self.getSuccessors(st)

		for t in succlist:
			#print(t[0].position)
			nodeset.append(Node(t[0],node,t[1],node.getCost()+t[2],node.getdepth()+1))
			
			self.Setnumber_nodes()
		return nodeset

##########CALCULATE PATH COST###################
def getCost(path):
	cost=0
	for item in path:
		if(item=='suck'):
			cost+=0
		else :
			cost+=2	
	return cost		

#######DFS GRAPH ALGO#############################
def dfs_tree(problem):

		
	t1=time.time()
	number_nodes=0
	maxstacksize=0
	path=[]
	fringe=Stack()
		
	ss=problem.getStartState()
	print(ss.matrixstate)
	startnode=Node(ss,None,None,0,0)
	
	mempernode=sys.getsizeof(startnode)
	fringe.push(startnode)
	
	if(fringe.size()>maxstacksize):
		maxstacksize=fringe.size()
	while( not fringe.isEmpty()):
		n=fringe.pop()
		
		nstate=n.state
		
		if(problem.isGoalstate(n.getState())):
			
			print('Goal state')
			
			#BACKTRACKING TO GET PATH
			path.append(n.getAction())
			par=n
			while(par.getParent()!=None):
				path.append(par.getAction())
				par=par.getParent()
			t2=time.time()
			time_taken=t2-t1
			path=path[1:]
			path.reverse()

			#PRINT STATISTICS###################
			print('Memory allocated to one node')
			print(mempernode)
			print('Maximum growth of stack ')
			print(maxstacksize)
			print('Memory used for nodes')
			print(mempernode*v.number_nodes)
			print('Memory used for stack')
			print(mempernode*maxstacksize)
			print('Memory used for keeping list of explored states')
			print(sys.getsizeof(nstate)*len(explored_states))
			print('\nThe amount of time taken')
			print(time_taken)
			###CLEAR CONTENTS OF EXPLORED_STATES FOR NEXT RUN
			explored_states[:]=[]
			return path
		#GRAPH VERSION TO AVOID REPEATED STATES		
		if(nstate.find()==False):
			explored_states.append(nstate)	
			
			
			nodeset=problem.expand(n)
			for h in nodeset:
				
				fringe.push(h)
			
		#KEEP TRACK OF STACK SIZE		
		if(fringe.size()>maxstacksize):
			maxstacksize=fringe.size()		

##########GREEDY ALGOS##########################
def greedy_searchh1(problem):
	t1=time.time()
	number_nodes=0
	maxqsize=0
	path=[]
	fringe=Stack()
	fringelist=[]
	
		
	ss=problem.getStartState()
	
	startnode=Node(ss,None,None,0,0)
	
	print(ss.position)
	mempernode=sys.getsizeof(startnode)
	fringe.push(startnode)
	
	if(fringe.size()>maxqsize):
		maxqsize=fringe.size()
	while( not fringe.isEmpty()):
		n=fringe.pop()
		
		nstate=n.state
		
		
		if(problem.isGoalstate(n.getState())):
			print('Goal state')
			print(n.getState().matrixstate)
			
			path.append(n.getAction())
			par=n
			while(par.getParent()!=None):
				path.append(par.getAction())
				
				par=par.getParent()
			t2=time.time()
			time_taken=t2-t1
			path=path[1:]
			path.reverse()
			###PRINT STATISTICS##################
			print('Memory allocated to one node')
			print(mempernode)
			print('Maximum growth of stack ')
			print(maxqsize)
			print('\nThe amount of time taken')
			print(time_taken)
			if(record_time==1):
				timearr.append(time_taken)
			if(record_time_roomsize==1):
				timearrroom.append(time_taken)	
			print('Memory used for nodes')
			print(mempernode*v.number_nodes)
			print('Memory used for stack')
			print(mempernode*maxqsize)
			print('Memory used for keeping list of explored states')
			print(sys.getsizeof(nstate)*len(explored_states))
			explored_states[:]=[]
			#path=path[1:]
			return path
				
		
			
		#GRAPH VERSION WAS IMPLEMENTED TO AVOID REPEATED STATES	
		#HERISTIC IS USED SO THAT ONLY CERTAIN STATES ARE ADDED TO STACK
		#ADD ALL NEIGHBOURS HAVING DIRTY TILES
		#ADD THOSE TILES WHICH ARE THEMSELVES NOT DIRTY BUT HAVE DIRTY TILES IN VICINITY
		#ADD THE CORNER POSITIONS TO FRINGE
		#IF ALL TILES ARE EMPTY ADD ALL SUCCESOR NODES TO FRINGE
		if(nstate.find()==False):	
			explored_states.append(nstate)
			
			nodeset=problem.expand(n)
			noneflag=0
			curxpos=nstate.position[0]
			curypos=nstate.position[1]
			if(nstate.matrixstate[curxpos][curypos]==1):
				for h in nodeset:
					if(h.getAction()=='suck'):
						fringe.push(h)
						noneflag=1	
					#print('suck condition')	
			else:			
				for h in nodeset:
					#print(h.getAction())
					
					if( h.state.matrixstate[h.state.position[0]][h.state.position[1]]==1 ):
						#print(h.getState().computeheuristic_2min()+h.getCost())
						fringe.push(h)
						noneflag=1
						#print('neighbors')
						
				if(noneflag==0):

					#print('all')
					noneflag2=0
					neighborx=h.state.position[0]
					neighbory=h.state.position[1]
					for h in nodeset:
						if(h.getAction()=='up' or h.getAction()=='down'):
							if(neighbory+1<=dim and neighbory+1>=0):
								if(h.state.matrixstate[neighborx][neighbory+1]==1):

									fringe.push(h)
									noneflag2=1
							if(neighbory-1<=dim and neighbory-1>=0):
								if( h.state.matrixstate[neighborx][neighbory-1]==1):
									fringe.push(h)
									noneflag2=1

						elif(h.getAction()=='right' or h.getAction()=='left'):
							if(neighborx+1<=dim and neighborx+1>=0):
								if(h.state.matrixstate[neighborx+1][neighbory]==1):

									fringe.push(h)
									noneflag2=1
							if(neighborx-1<=dim and neighborx-1>=0):
								if( h.state.matrixstate[neighborx-1][neighbory]==1):
									fringe.push(h)
									noneflag2=1
					if(noneflag2==0):
						for h in nodeset:
							fringe.push(h)	
				for h in nodeset:
						if(h.state.position==[0,dim] or h.state.position==[dim,0] or h.state.position==[dim,dim] or h.state.position==[0,0]):
							fringe.push(h)					

						
								
		#MAXQSIZE REFERS TO STACK SIZE	
		if(fringe.size()>maxqsize):
			maxqsize=fringe.size()



######GREEDY ALGO #######################################################
def greedy_searchh2(problem):
		t1=time.time()
		number_nodes=0
		maxqsize=0
		path=[]
		fringe=Stack()
		fringelist=[]
		
			
		ss=problem.getStartState()
		
		startnode=Node(ss,None,None,0,0)
		
		print(ss.position)
		mempernode=sys.getsizeof(startnode)
		fringe.push(startnode)
		
		if(fringe.size()>maxqsize):
			maxqsize=fringe.size()
		while( not fringe.isEmpty()):
			n=fringe.pop()
			
			nstate=n.state
			
			
			if(problem.isGoalstate(n.getState())):
				print('Goal state')
				print(n.getState().matrixstate)
				
				path.append(n.getAction())
				par=n
				while(par.getParent()!=None):
					path.append(par.getAction())
					par=par.getParent()
				t2=time.time()
				time_taken=t2-t1
				path=path[1:]
				path.reverse()
				print('Memory allocated to one node')
				print(mempernode)
				print('Maximum growth of stack ')
				print(maxqsize)
				print('\nThe amount of time taken')
				print(time_taken)
				if(record_time==1):
					timearr.append(time_taken)
				if(record_time_roomsize==1):
					timearrroom.append(time_taken)	
				print('Memory used for nodes')
				print(mempernode*v.number_nodes)
				print('Memory used for stack')
				print(mempernode*maxqsize)
				print('Memory used for keeping list of explored states')
				print(sys.getsizeof(nstate)*len(explored_states))
				explored_states[:]=[]
				#path=path[1:]
				return path
					
			
				
			#HEURISTIC BASED 
			#IF TILE IS DIRTY ADD ONLY SUCCESOR CORRESPONDING TO CLEAN TILE
			#ADD DIRTY SUCCESORS
			#IF NONE OF SUCCESORS ARE DIRT ADD ALL	
			if(nstate.find()==False):	
				explored_states.append(nstate)
				
				nodeset=problem.expand(n)
				noneflag=0
				curxpos=nstate.position[0]
				curypos=nstate.position[1]
				if(nstate.matrixstate[curxpos][curypos]==1):
					for h in nodeset:
						if(h.getAction()=='suck'):
							fringe.push(h)
							noneflag=1	
							
				else:			
					for h in nodeset:
						
						
						if( h.state.matrixstate[h.state.position[0]][h.state.position[1]]==1 ):
							
							fringe.push(h)
							noneflag=1
							
							
					if(noneflag==0):
						
						for h in nodeset:	
							fringe.push(h)
					for h in nodeset:
						if(h.state.position==[0,dim] or h.state.position==[dim,0] or h.state.position==[dim,dim] or h.state.position==[0,0]):
							fringe.push(h)				
				
			if(fringe.size()>maxqsize):
				maxqsize=fringe.size()


if __name__ == '__main__':
	#DRIVER FUNCTION
	option=int(input("Enter option 1/2/3/4"))
	

	
	if(option==1 or option==2 or option==3):
		p=int (input("Enter the percentage of tiles to get dirt (integer value)"))	
		d=int(input("Enter dimensions of matrix"))
		
		dim=d-1
		startarr=dirtgeneratorrandom(p,d)
		startpos=startpositiongenerator()
		print('Initial room condition')
		print(startarr)
		print('\n')

		print('Starting position')
		print(startpos)
		
		
		
		if(option==1):
			#DISPLAY ROOM
			turtlegraphicsroom(startarr)
		elif(option==2):
			#DISPLAY ACTION PATH USING DFS
			turtlegraphicsroom(startarr)
			

			vinitialstate=Vacuumstate(startarr,startpos)
			v=vacuumproblem(vinitialstate)
			number_nodes=0
			

			
			actionseq=dfs_tree(v)
			
			
			print('The dimensions and percentage of dirt are')
			print(str(p))
			print('and')
			print(str(d))
			print('Number of nodes generated till problem is solved')
			print(str(v.number_nodes))
			print('\n')
			
			print('\n')

			print('Action path :')
			print(str(actionseq))
			print('\n')
			print('Total cost using dfs')
			print(str(getCost(actionseq)))
		
			turtlegraphics(actionseq,startpos,1)	




		elif(option==3):
			#####SHOWS ACTION PATH OF BOTH THE GREEDY ALGOS#####################
			turtlegraphicsroom(startarr)
			startarr2=copy.deepcopy(startarr)
			startpos2=copy.deepcopy(startpos)


			vinitialstate=Vacuumstate(startarr,startpos)
			v=vacuumproblem(vinitialstate)
			number_nodes=0
			

			
			actionseq=greedy_searchh2(v)
			
	
		
			
			print('The dimensions and percentage of dirt are')
			print(str(p))
			print('and')
			print(str(d))
			print('Number of nodes generated till problem is solved')
			print(str(v.number_nodes))
			print('\n')
			print('Action path :')
			print(str(actionseq))
			print('\n')
			print('Total cost using greedy approach')
			print(str(getCost(actionseq)))
		
			turtlegraphics(actionseq,startpos,2)

			####BRING ROOM TO STARTING STATE AGAIN WITHOUT ERASING PREVIOUS PATH#####
			turtlegraphicsroom(startarr)


			vinitialstate2=Vacuumstate(startarr2,startpos2)
			v2=vacuumproblem(vinitialstate2)
			number_nodes=0
			

			
			actionseq2=greedy_searchh1(v2)
			
			
		
			
			print('The dimensions and percentage of dirt are')
			print(str(p))
			print('and')
			print(str(d))
			print('Number of nodes generated till problem is solved')
			print(str(v2.number_nodes))
			print('\n')
			
			print('\n')

			print('Action path :')
			print(str(actionseq2))
			print('\n')
			print('Total cost using greedy approach')
			print(str(getCost(actionseq2)))
		
			turtlegraphics(actionseq2,startpos,3)





	elif(option==4):
		#COMPARATIVE ANALYSIS FOR GREEDY METHOD AND DFS
		#Since there was no significant improvement even after using the second heuristic 
		#comparative analysis has only been done with dfs and one of the greedy algorithms


		#DISPLAY ACTION PATH USING DFS AND GREEDY ALGO##########################
		p=int (input("Enter the percentage of tiles to get dirt (integer value)"))	
		d=int(input("Enter dimensions of matrix"))
		
		dim=d-1
		startarr=dirtgeneratorrandom(p,d)
		startpos=startpositiongenerator()

		print('Initial room condition')
		print(startarr)
		print('\n')

		print('Starting position')
		print(startpos)
		turtlegraphicsroom(startarr)
		startpos2=copy.deepcopy(startpos)
		startarr2=copy.deepcopy(startarr)

		vinitialstate=Vacuumstate(startarr,startpos)
		v=vacuumproblem(vinitialstate)
		number_nodes=0
		

		
		actionseq=dfs_tree(v)
	
		
		print('The dimensions and percentage of dirt are')
		print(str(p))
		print('and')
		print(str(d))
		print('Number of nodes generated till problem is solved')
		print(str(v.number_nodes))
		print('\n')
		
		

		print('Action path :')
		print(str(actionseq))
		print('\n')
		print('Total cost using dfs')
		print(str(getCost(actionseq)))
	
		turtlegraphics(actionseq,startpos,1)

		turtlegraphicsroom(startarr)

		vinitialstate2=Vacuumstate(startarr2,startpos2)

		
		v2=vacuumproblem(vinitialstate2)
		print(vinitialstate2.matrixstate)
		number_nodes=0
	

		
		actionseq2=greedy_searchh2(v2)
		
		
	
		
		print('The dimensions and percentage of dirt are')
		print(str(p))
		print('and')
		print(str(d))
		print('Number of nodes generated till problem is solved')
		print(str(v2.number_nodes))
		print('\n')
		
	

		print('Action path :')
		print(str(actionseq2))
		print('\n')
		print('Total cost using greedy approach')
		print(str(getCost(actionseq2)))
	
		turtlegraphics(actionseq2,startpos2,2)




		print('#######################################################')
		print('Now calculating the average cost for 10 runs')
		costgreedy=[]
		costdfs=[]
		original_dirtp=copy.deepcopy(p)
		for x in xrange(0,10):
			startarr_avg=dirtgeneratorrandom(p,d)
			startpos_avg=startpositiongenerator()
			startpos2_avg=copy.deepcopy(startpos)
			startarr2_avg=copy.deepcopy(startarr)
			vinitialstate_avg=Vacuumstate(startarr_avg,startpos_avg)
			v_avg=vacuumproblem(vinitialstate_avg)
			actionseq_avg=dfs_tree(v_avg)
			costdfs.append(getCost(actionseq_avg))
			vinitialstate_avg2=Vacuumstate(startarr2_avg,startpos2_avg)
			v2_avg=vacuumproblem(vinitialstate_avg2)
			actionseq_avg2=greedy_searchh2(v2_avg)
			costgreedy.append(getCost(actionseq_avg2))

		sumgreedy=0
		sumdfs=0	

		for item in costgreedy:
			sumgreedy=sumgreedy+item
		for item in costdfs:
			sumdfs=sumdfs+item
		print("Average cost of dfs for 10 runs is\n",sumdfs/10)
		print('Average cost of greedy algorithm for 10 runs is \n',sumgreedy/10)			

		
		p=10
		timelist=[]
		print('###################################################################')
		print('Now varying dirt percentages in step sizes of 5 from 10%')
		while(p<100):
			steparr=dirtgeneratorrandom(p,d)
			stepstart=startpositiongenerator()
			vinitialstatestep=Vacuumstate(steparr,stepstart)
			vstep=vacuumproblem(vinitialstatestep)
			record_time=1
			actionstep=greedy_searchh2(vstep)


			p=p+5
		print(timearr)	
		##TIME ARR STORES THE TIME TAKEN TO COMPUTE SOLUTION BY VARYING DIRT % USING HEURISTIC(H2)


		print('#################################################################')
		print('Now varying room dimensions starting from 3')
		d=3
		dim=2
		while(d<=20):

			
			steparr=dirtgeneratorrandom(original_dirtp,d)
			stepstart=startpositiongenerator()
			vinitialstatestep=Vacuumstate(steparr,stepstart)
			vstep=vacuumproblem(vinitialstatestep)
			record_time_roomsize=1
			actionstep=greedy_searchh2(vstep)
			d=d+1
			dim=dim+1
		print(timearrroom)	
		#TIMEARRROOM STORES THE TIME TAKEN TO COMPUTE SOLUTION BY VARYING ROOM DIMENSIONS

        else:
                print("Invalid option given")
	
			


	
	    
	
	
	

	
	
								
