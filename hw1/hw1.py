import copy


class State:
    def __init__(self, grid= [], parent= None, g= 0, h= 0, f= 0):
        self.grid = grid
        self.g = g
        self.h = h
        self.f = f
        self.parent = parent

    def isGoalState(self,goal):
        if(self.grid == goal.grid):
            return True
        else:
            return False


    def printState(self):
        for i in range(4):
            row = []
            for j in range(4):
                row.append(self.grid[i][j])

            for i in range(4):
                if i != 3:
                    print(row[i], end =" ")
                else:
                    print(row[i], end="\n")

    def expand(self):

        possibleStates = []

        # find empty cell
        emptyCellX = 0
        emptyCellY = 0
        for i in range(4):
            for j in range(4):
                if(self.grid[i][j] == '_'):
                    emptyCellX = i
                    emptyCellY = j

        # find possible moves

        # up 1
        if (emptyCellX + 1 <= 3):
            newGrid = copy.deepcopy(self.grid)
            newGrid[emptyCellX][emptyCellY] = self.grid[emptyCellX + 1][emptyCellY]
            newGrid[emptyCellX + 1][emptyCellY] = '_'
            childState = State(newGrid, self, self.g + 2,self.h,self.f+2)
            possibleStates.append(childState)

        # down 1
        if(emptyCellX - 1 >= 0):
            newGrid = copy.deepcopy(self.grid)
            newGrid[emptyCellX][emptyCellY] = self.grid[emptyCellX - 1][emptyCellY]
            newGrid[emptyCellX - 1][emptyCellY] = '_'
            childState = State(newGrid,self, self.g + 2,self.h,self.f+2)
            possibleStates.append(childState)

        # left 1
        if (emptyCellY + 1 <= 3):
            newGrid = copy.deepcopy(self.grid)
            newGrid[emptyCellX][emptyCellY] = self.grid[emptyCellX][emptyCellY + 1]
            newGrid[emptyCellX][emptyCellY + 1] = '_'
            childState = State(newGrid, self, self.g + 2,self.h,self.f+2)
            possibleStates.append(childState)

        # right 1
        if (emptyCellY - 1 >= 0):
            newGrid = copy.deepcopy(self.grid)
            newGrid[emptyCellX][emptyCellY] = self.grid[emptyCellX][emptyCellY - 1]
            newGrid[emptyCellX][emptyCellY - 1] = '_'
            childState = State(newGrid, self, self.g + 2,self.h,self.f+2)
            possibleStates.append(childState)

        # up 2
        if (emptyCellX + 2 <= 3):
            newGrid = copy.deepcopy(self.grid)
            newGrid[emptyCellX][emptyCellY] = self.grid[emptyCellX + 2][emptyCellY]
            newGrid[emptyCellX + 2][emptyCellY] = '_'
            childState = State(newGrid, self, self.g + 3,self.h,self.f+3)
            possibleStates.append(childState)

        # down 2
        if(emptyCellX - 2 >= 0):
            newGrid = copy.deepcopy(self.grid)
            newGrid[emptyCellX][emptyCellY] = self.grid[emptyCellX - 2][emptyCellY]
            newGrid[emptyCellX - 2][emptyCellY] = '_'
            childState = State(newGrid, self, self.g + 3,self.h,self.f+3)
            possibleStates.append(childState)

        # left 2
        if (emptyCellY + 2 <= 3):
            newGrid = copy.deepcopy(self.grid)
            newGrid[emptyCellX][emptyCellY] = self.grid[emptyCellX][emptyCellY + 2]
            newGrid[emptyCellX][emptyCellY + 2] = '_'
            childState = State(newGrid, self, self.g + 3,self.h,self.f+3)
            possibleStates.append(childState)

        # right 2
        if (emptyCellY - 2 >= 0):
            newGrid = copy.deepcopy(self.grid)
            newGrid[emptyCellX][emptyCellY] = self.grid[emptyCellX][emptyCellY - 2]
            newGrid[emptyCellX][emptyCellY - 2] = '_'
            childState = State(newGrid, self, self.g + 3,self.h,self.f+3)
            possibleStates.append(childState)

        return possibleStates


def LimitedDepthSearch(state,goal,limit):

    if(state == None):
        return None

    if(state.isGoalState(goal)):
        # return solution
        return state

    if(limit == 0):
        # cutoff
        return None #no solution

    notFound = None
    expandedStates = state.expand()
    for expandedState in expandedStates:
        result = LimitedDepthSearch(expandedState,goal,limit-1)

        if(result == None):
            notFound = None
        elif (result.isGoalState(goal)):
            return result  # SOLUTION

    return notFound

def IterativeDeepeningSearch(initialState,goal,limit):
    for i in range(limit+1):
        result = LimitedDepthSearch(initialState,goal,i)
        if(result != None):
            path = []
            printingState = result
            while(printingState.parent != None):
                path.append(printingState)
                printingState = printingState.parent

            print("SUCCESS")
            print("")
            initialState.printState()
            print("")
            for state in range(len(path)):
                currentIndex = len(path) - 1 - state
                path[currentIndex].printState()
                print("")

            return ""

    return "FAILURE"

def calculateManhattan(state,goal):

    distance = 0
    for i in range(4):
        for j in range(4):
            currentGrid = state.grid[i][j]
            if(currentGrid != '_'):
                for x in range(4):
                    for y in range(4):
                        if(currentGrid == goal.grid[x][y]):
                            distance += abs(i-x) + abs(j-y)

    return distance

def AStar(stateInitial,goal,limit):

    stateInitial.h = calculateManhattan(stateInitial,goal)
    stateInitial.f = stateInitial.g + stateInitial.h
    stateOpenList = []
    stateClosedList = []

    stateOpenList.append(stateInitial)

    while(True):
        if len(stateOpenList) == 0:
            return "FAILURE"

        stateMinF = stateOpenList[0]
        stateMinF.h = calculateManhattan(stateMinF, goal)
        stateMinF.f = stateMinF.h + stateMinF.g

        for statePossible in stateOpenList:

            if (statePossible.f < stateMinF.f):
                stateMinF = statePossible

        stateOpenList.remove(stateMinF)

        if (stateMinF.f > limit):
            return "FAILURE"


        if(stateMinF.isGoalState(goal)):
            path = []
            printingState = stateMinF
            while (printingState.parent != None):
                path.append(printingState)
                printingState = printingState.parent

            print("SUCCESS")
            print("")
            stateInitial.printState()
            print("")
            for state in range(len(path)):
                currentIndex = len(path) - 1 - state
                path[currentIndex].printState()
                print("")
            return ""

        isThereState = False
        for state in stateClosedList:
            if(state.grid == stateMinF.grid and state.f <= stateMinF.f):
                isThereState = True

        if isThereState == False:
            stateClosedList.append(stateMinF)
            NList = stateMinF.expand()

            for expandedState in NList:
                expandedState.h = calculateManhattan(expandedState, goal)
                expandedState.f = expandedState.h + expandedState.g
                stateOpenList.append(expandedState)



algorithm = input()
limitation = int(input())
initialGrid = []
goalGrid = []
for i in range(4):
    rowString = input()
    cells = rowString.split()

    row = []
    for cell in cells:
        if(cell != '_'):
            row.append(int(cell))
        else:
            row.append(cell)

    initialGrid.append(row)

for i in range(4):
    rowString = input()
    cells = rowString.split()

    row = []
    for cell in cells:
        if(cell != '_'):
            row.append(int(cell))
        else:
            row.append(cell)

    goalGrid.append(row)

initialState = State(initialGrid)
goalState = State(goalGrid)
if(algorithm == "A*"):
    print(AStar(initialState,goalState,limitation))
if(algorithm == "DIFDS"):
    print(IterativeDeepeningSearch(initialState,goalState,limitation))

