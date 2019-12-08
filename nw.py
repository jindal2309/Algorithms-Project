import time

timeout = 100000
maximum_missionary = 30

MAX_M = 30
MAX_C = 30
CAP_BOAT = 20
CNST = None


class CONST:
	def __init__(self, num_missionary, num_cannibals, boat_capacity):
		self.num_missionary = num_missionary
		self.num_cannibals = num_cannibals
		self.boat_capacity = boat_capacity

class Graph:

    def __init__(self):

        self.bfs_ancestor = {}
        self.dfs_ancestor = {}
    
    def BFS(self, s):
        queue = []
        queue.append(s)
        visited = {}
        self.bfs_ancestor[s] = None
        start_time = time.time()
        while len(queue):
            u = queue.pop(0)
            visited[(u.m_left, u.c_left, u.dir)] = 1
            # return if goal state i.e. cannibals = 0, missionaries = 0, boat direction = 0            
            if u.isGoalState():
                self.bfs_ancestor[TERMINAL_STATE] = u
                queue.clear()
                return self.bfs_ancestor
            
            if time.time()-start_time > timeout:
                queue.clear()
                return {}
            # Stops searching after a certain time limit            
            for v in u.successors():
                if visited.get((v.m_left, v.c_left, v.dir), 0) == 0:
                    queue.append(v)
                    self.bfs_ancestor[v] = u
        return {}       
                  
    def DFS(self, s):
        stack = []
        stack.append(s)
        visited = {}
        self.dfs_ancestor[s] = None
        start_time = time.time()
        while len(stack):
            u = stack.pop()
            visited[(u.m_left, u.c_left, u.dir)] = 1
            # return if goal state i.e. cannibals = 0, missionaries = 0, boat direction = 0            
            if u.isGoalState():
                self.dfs_ancestor[TERMINAL_STATE] = u
                stack.clear()
                return self.dfs_ancestor
            # Stops searching after a certain time limit             
            if time.time()-start_time > timeout:
                stack.clear()
                return {}
            
            for v in u.successors():
                if visited.get((v.m_left, v.c_left, v.dir), 0) == 0:
                    stack.append(v)
                    self.dfs_ancestor[v] = u
        return {}       
                  


    # Prints the path returned by BFS/DFS
    def printPath(self, parentList, tail):
        if parentList == {} or parentList is None or tail is None:
            return
        if tail == TERMINAL_STATE: 
            tail = parentList[tail]

        state_list = []
        while tail is not None:
            state_list.append(tail)
            tail = parentList[tail]

        while state_list:
            print(state_list.pop(-1))


class State(object):
	def __init__(self, m_left, c_left, dir, m_right, c_right, CONSTS,moves):
		self.m_left = m_left
		self.c_left = c_left
		self.dir = dir
		self.action = ""
		self.m_right = m_right
		self.c_right = c_right
		self.CONSTANTS = CONSTS

		self.moves = moves

		if not CONSTS is None:
			CNST = CONSTS
			num_missionary = CONSTS.num_missionary
			num_cannibals = CONSTS.num_cannibals
			boat_capacity = CONSTS.boat_capacity

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
							self.m_right - sgn * m, self.c_right - sgn * c,
							self.CONSTANTS,self.moves)
		if newState.isValid():
			newState.action = "Move %d M and %d C %s." % (m, c, direction)
			listChild.append(newState)

	def isValid(self):
		if self.m_left < 0 or self.c_left < 0 or self.m_left > MAX_M or self.c_left > MAX_C or (self.dir != 0 and self.dir != 1):
			return False
		if (self.c_left > self.m_left > 0) or (self.c_right > self.m_right > 0):  # more c_left then m_left on original shore
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

TERMINAL_STATE = State(-1, -1, 0, -1, -1, CNST,None)
m = int(input("Number of Missionaries: "))
c = int(input("Number of Cannibals: "))
k = int(input("Boat Capacity: "))
CNST = CONST(m, c, k)
moves = []
for i in range(k + 1):
	for j in range(k + 1):
		if 0 < i < j:
			continue
		if 1 <= i + j <= k:
			moves.append((i, j))

INITIAL_STATE = State(CNST.num_missionary, CNST.num_cannibals, 1, 0, 0, CNST, moves)
g = Graph()
print("\nAnswer for BFS: ")
p = g.BFS(INITIAL_STATE)
if len(p):
	g.printPath(p, TERMINAL_STATE)
else:
	print("No Solution")

print("\nAnswer for DFS: ")
p = g.DFS(INITIAL_STATE)
if len(p):
	g.printPath(p, TERMINAL_STATE)
else:
	print("No Solution")