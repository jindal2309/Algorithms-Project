import sys
import time

class Direction:
	OLD_TO_NEW = 1
	NEW_TO_OLD = 0


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
            visited[(u.missionaries, u.cannibals, u.dir)] = 1
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
                if visited.get((v.missionaries, v.cannibals, v.dir), 0) == 0:
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
            visited[(u.missionaries, u.cannibals, u.dir)] = 1
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
                if visited.get((v.missionaries, v.cannibals, v.dir), 0) == 0:
                    stack.append(v)
                    self.dfs_parent[v] = u
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


CON_IN = sys.stdin
CON_OUT = sys.stdout

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


def runBFS(g, INITIAL_STATE):
	print("\n\nBFS :: \n")
	p = g.BFS(INITIAL_STATE)
	if len(p):
		g.printPath(p, TERMINAL_STATE)
	else:
		print("No Solution")


def runDFS(g, INITIAL_STATE):
	print("\n\nDFS :: \n")
	p = g.DFS(INITIAL_STATE)
	if len(p):
		g.printPath(p, TERMINAL_STATE)
	else:
		print("No Solution")


MAX_M = 30
MAX_C = 30
CAP_BOAT = 20
CNST = None


class State(object):

	def __init__(self, missionaries, cannibals, dir, missionariesPassed, cannibalsPassed, level, CONSTS,moves):
		self.missionaries = missionaries
		self.cannibals = cannibals
		self.dir = dir
		self.action = ""
		self.level = level
		self.missionariesPassed = missionariesPassed
		self.cannibalsPassed = cannibalsPassed
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
		if self.dir == Direction.OLD_TO_NEW:
			sgn = -1
			direction = "from the original shore to the new shore"
		else:
			sgn = 1
			direction = "back from the new shore to the original shore"
		for i in self.moves:
			(m, c) = i
			self.addValidSuccessors(listChild, m, c, sgn, direction)
		return listChild

	def addValidSuccessors(self, listChild, m, c, sgn, direction):
		newState = State(self.missionaries + sgn * m, self.cannibals + sgn * c, self.dir + sgn * 1,
							self.missionariesPassed - sgn * m, self.cannibalsPassed - sgn * c, self.level + 1,
							self.CONSTANTS,self.moves)
		if newState.isValid():
			newState.action = " take %d missionaries and %d cannibals %s." % (m, c, direction)
			listChild.append(newState)

	def isValid(self):
		# obvious
		if self.missionaries < 0 or self.cannibals < 0 or self.missionaries > MAX_M or self.cannibals > MAX_C or (
				self.dir != 0 and self.dir != 1):
			return False

		# then check whether missionaries outnumbered by cannibals in any shore
		if (self.cannibals > self.missionaries > 0) or (
				self.cannibalsPassed > self.missionariesPassed > 0):  # more cannibals then missionaries on original shore
			return False

		return True

	def isGoalState(self):
		return self.cannibals == 0 and self.missionaries == 0 and self.dir == Direction.NEW_TO_OLD

	def __repr__(self):
		return "\n%s\n\n< State (%d, %d, %d, %d, %d) >" % (
			self.action, self.missionaries, self.cannibals, self.dir, self.missionariesPassed,
			self.cannibalsPassed)

	def __eq__(self, other):
		return self.missionaries == other.missionaries and self.cannibals == other.cannibals and self.dir == other.dir

	def __hash__(self):
		return hash((self.missionaries, self.cannibals, self.dir))

	def __ne__(self, other):
		return not (self == other)


TERMINAL_STATE = State(-1, -1, Direction.NEW_TO_OLD, -1, -1, 0, CNST,None)

def main():
#	m = int(input("m="))
#	c = int(input("c="))
#	k = int(input("k="))
#	t = int(input("TIME_LIMIT_s="))

	m = 4
	c = 4
	k = 3
	t = 10000
	CNST = CONST(m, c, k, t)
	moves = genPossibleMoves(CNST.CAP_BOAT)

	INITIAL_STATE = State(CNST.MAX_M, CNST.MAX_C, Direction.OLD_TO_NEW, 0, 0, 0, CNST, moves)
	g = Graph()

	sys.stdout = CON_OUT
	print("\nRunning BFS>")
	runBFS(g, INITIAL_STATE)
	print("Executed BFS>")

	print("\nRunning DFS>")
	runDFS(g, INITIAL_STATE)
	sys.stdout = CON_OUT
	print("Executed DFS>")


if __name__ == '__main__':
	main()
