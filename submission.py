import sys
import time
from collections import defaultdict

class CONST:
	def __init__(self, MAX_M, MAX_C, CAP_BOAT, MAX_TIME_S):
		self.MAX_M = MAX_M
		self.MAX_C = MAX_C
		self.CAP_BOAT = CAP_BOAT
		self.MAX_TIME = MAX_TIME_S

class Graph:

	def __init__(self):

		self.bfs_parent = {}
		self.dfs_parent = {}
	
	def BFS(self, s):
		queue = []
		queue.append(s)
		visited = {}
		self.bfs_parent[s] = None
		start_time = time.time()
		while len(queue):
			u = queue.pop(0)
			visited[(u.m_left, u.c_left, u.dir)] = 1
			# return if goal state i.e. cannibals = 0, missionaries = 0, boat direction = 0            
			if u.isGoalState():
				self.bfs_parent[TERMINAL_STATE] = u
				queue.clear()
				return self.bfs_parent
			
			if time.time()-start_time > u.CONSTANTS.MAX_TIME:
				queue.clear()
				return {}
			# Stops searching after a certain time limit            
			for v in u.successors():
				if visited.get((v.m_left, v.c_left, v.dir), 0) == 0:
					queue.append(v)
					self.bfs_parent[v] = u
		return {}       
				  
	def DFS(self, s):
		stack = []
		stack.append(s)
		visited = {}
		self.dfs_parent[s] = None
		start_time = time.time()
		while len(stack):
			u = stack.pop()
			visited[(u.m_left, u.c_left, u.dir)] = 1
			# return if goal state i.e. cannibals = 0, missionaries = 0, boat direction = 0            
			if u.isGoalState():
				self.dfs_parent[TERMINAL_STATE] = u
				stack.clear()
				return self.dfs_parent
			# Stops searching after a certain time limit             
			if time.time()-start_time > u.CONSTANTS.MAX_TIME:
				stack.clear()
				return {}
			
			for v in u.successors():
				if visited.get((v.m_left, v.c_left, v.dir), 0) == 0:
					stack.append(v)
					self.dfs_parent[v] = u
		return {}       
				  


	# Prints the path returned by BFS/DFS
	def printPath(self, parentList, tail):
		count = 0
		if parentList == {} or parentList is None or tail is None:
			return
		if tail == TERMINAL_STATE: 
			tail = parentList[tail]

		state_list = []
		while tail is not None:
			count+=1
			state_list.append(tail)
			tail = parentList[tail]

		while state_list:
			print(state_list.pop(-1))
		print("Count = ",count-1)


# Generate All possible next moves for each state to reduce number of iterations on each node
def genPossibleMoves(CAP_BOAT):
	moves = []
	for m in range(CAP_BOAT + 1):
		for c in range(CAP_BOAT + 1):
			if 0 < m < c:
				continue
			if 1 <= m + c <= CAP_BOAT:
				moves.append((m, c))
	return moves

MAX_M = 30
MAX_C = 30
CAP_BOAT = 20
CNST = None


class State(object):
	def __init__(self, m_left, c_left, dir, m_right, c_right, level, CONSTS,moves):
		self.m_left = m_left
		self.c_left = c_left
		self.dir = dir
		self.action = ""
		self.level = level
		self.m_right = m_right
		self.c_right = c_right
		self.CONSTANTS = CONSTS

		self.moves = moves

		global MAX_M
		global MAX_C
		global CAP_BOAT
		global CNST

		if not CONSTS is None:
			CNST = CONSTS
			MAX_M = CONSTS.MAX_M
			MAX_C = CONSTS.MAX_C
			CAP_BOAT = CONSTS.CAP_BOAT

	# pass True to count forward
	def successors(self):
		listChild = []
		if not self.isValid() or self.isGoalState():
			return listChild
		if self.dir == 1:
			sgn = -1
			direction = "from left to right"
		else:
			sgn = 1
			direction = "from right to left"
		for i in self.moves:
			(m, c) = i
			self.addValidSuccessors(listChild, m, c, sgn, direction)
		return listChild

	def addValidSuccessors(self, listChild, m, c, sgn, direction):
		newState = State(self.m_left + sgn * m, self.c_left + sgn * c, self.dir + sgn * 1,
							self.m_right - sgn * m, self.c_right - sgn * c, self.level + 1,
							self.CONSTANTS,self.moves)
		if newState.isValid():
			newState.action = "Move %d M and %d C %s." % (m, c, direction)
			listChild.append(newState)

	def isValid(self):
		# obvious
		if self.m_left < 0 or self.c_left < 0 or self.m_left > MAX_M or self.c_left > MAX_C or (self.dir != 0 and self.dir != 1):
			return False

		# then check whether m_left outnumbered by c_left in any shore
		if (self.c_left > self.m_left > 0) or (self.c_right > self.m_right> 0):  # more cannibals then missionaries on original shore
			return False

		return True

	def isGoalState(self):
		return self.c_left == 0 and self.m_left == 0 and self.dir == 0

	def __repr__(self):
		if self.dir == 1:
			text = "left"
		else:
			text = "right"
		return "\n%s\nState: Left (M : %d, C : %d), Boat Position: (%s), Right (M: %d, C: %d)" % (
			self.action, self.m_left, self.c_left, text, self.m_right,self.c_right)

	def __eq__(self, other):
		return self.m_left == other.m_left and self.c_left == other.c_left and self.dir == other.dir

	def __hash__(self):
		return hash((self.m_left, self.c_left, self.dir))

	def __ne__(self, other):
		return not (self == other)


TERMINAL_STATE = State(-1, -1, 0, -1, -1, 0, CNST,None)

def main():
	m = int(input("Number of Missionaries: "))
	c = int(input("Number of Cannibals: "))
	k = int(input("Boat Capacity: "))

	CNST = CONST(m, c, k, 100000)

	moves = genPossibleMoves(CNST.CAP_BOAT)

	INITIAL_STATE = State(CNST.MAX_M, CNST.MAX_C, 1, 0, 0, 0, CNST, moves)
	g = Graph()

	print("BFS")
	p = g.BFS(INITIAL_STATE)
	if len(p):
		g.printPath(p, TERMINAL_STATE)
	else:
		print("No Solution")

	print("DFS")
	p = g.DFS(INITIAL_STATE)
	if len(p):
		g.printPath(p, TERMINAL_STATE)
	else:
		print("No Solution")


if __name__ == '__main__':
	main()