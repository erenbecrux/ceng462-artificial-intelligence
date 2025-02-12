import copy
import sys
from random import randrange, uniform, choice


class State:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return isinstance(other, State) and self.x == other.x and self.y == other.y


def initQValues(stateList,qvaluesDict, width):
    for state in stateList:
        stateidx = (state.x - 1) + (state.y - 1) * width
        stateValues = {'R':0,'L':0,'U':0,'D':0}
        qvaluesDict[stateidx] = stateValues

# Returns next state according to current action
def transitionFunction(currentState,currentAction,width,height,statesList):
    nextStateIndex = 0

    if (currentAction == "U"):
        if currentState.y == height:
            return "OUTSIDE"
        nextStateIndex = (currentState.x - 1) + (currentState.y) * width
    elif(currentAction == "R"):
        if currentState.x == width:
            return "OUTSIDE"
        nextStateIndex = (currentState.x) + (currentState.y - 1) * width
    elif (currentAction == "D"):
        if currentState.y == 1:
            return "OUTSIDE"
        nextStateIndex = (currentState.x - 1) + (currentState.y - 2) * width
    elif(currentAction == "L"):
        if currentState.x == 1:
            return "OUTSIDE"
        nextStateIndex = (currentState.x - 2) + (currentState.y - 1) * width


    nextState = statesList[nextStateIndex]
    return nextState

def rewardFunction(currentState,currentAction,width,height,statesList,pitList,obstacleList,pitReward,goalReward,obstacleReward,defaultReward,goal):
    nextState = transitionFunction(currentState,currentAction,width,height,statesList)

    if nextState == "OUTSIDE":
        return pitReward

    if nextState == goal:
        return goalReward

    for i in range(len(pitList)):
        pitState = pitList[i]
        if nextState == pitState:
            return pitReward

    for i in range(len(obstacleList)):
        obstacleState = obstacleList[i]
        if nextState == obstacleState:
            return obstacleReward

    #default
    return defaultReward

def epsilon_greedy(currentState,width,actionList,epsilonValue,qValDict):
    possibility = uniform(0, 1)
    currentStateidx = (currentState.x - 1) + (currentState.y - 1) * width
    if possibility <= epsilonValue:
        # random action
        randomActionIndex = randrange(4)
        randomAction = actionList[randomActionIndex]
        return randomAction
    else:
        maxQ = max(qValDict[currentStateidx].values())
        # random action with the same q-value
        bestActions = [action for action, qValue in qValDict[currentStateidx].items() if qValue == maxQ]
        return choice(bestActions)


def findMaxQ(stateS,width,qValDict):
    currentStateidx = (stateS.x - 1) + (stateS.y - 1) * width
    maxQ = max(qValDict[currentStateidx].values())
    # random action with the same q-value
    bestActions = [action for action, qValue in qValDict[currentStateidx].items() if qValue == maxQ]
    return choice(bestActions)


def sarsa(episodeNumber,alphaValue,gammaValue,epsilonValue,width,height,goal,pitList,obtsacleList,defaultReward,obstacleReward,pitReward,goalReward,stateList,actionList,obstacleList,qValDict):
    initQValues(stateList,qValDict,width)

    # initialize possible initial states
    possibleInitialStates = []
    for i in range(width):
        for j in range(height):
            stateIndex = i + j * width
            currentState = stateList[stateIndex]
            isPossible = True
            for obstacle in obstacleList:
                if obstacle == currentState:
                    isPossible = False
            for pitfall in pitList:
                if pitfall == currentState:
                    isPossible = False
            if goal == currentState:
                isPossible = False
            if isPossible:
                possibleInitialStates.append(currentState)

    for i in range(episodeNumber):

        # initialize state and action
        randomInitialStateIndex = randrange(len(possibleInitialStates))
        stateS = possibleInitialStates[randomInitialStateIndex]
        actionA = epsilon_greedy(stateS,width, actionList, epsilonValue, qValDict)

        while True:

            currentReward = rewardFunction(stateS, actionA,width,height,stateList,pitList, obstacleList, pitReward, goalReward, obstacleReward, defaultReward,goal)
            nextState = transitionFunction(stateS, actionA, width, height,stateList)

            movingToNextState = True
            for obstacle in obstacleList:
                if obstacle == nextState:
                    movingToNextState = False
                    break
            for pitfall in pitList:
                if pitfall == nextState:
                    movingToNextState = False
                    break

            if nextState == "OUTSIDE" or not movingToNextState:
                nextState = stateS

            nextAction = epsilon_greedy(nextState,width, actionList, epsilonValue, qValDict)

            # current q value
            stateSidx = (stateS.x - 1) + (stateS.y - 1) * width
            qValue = qValDict[stateSidx][actionA]

            nextStateidx = (nextState.x - 1) + (nextState.y - 1) * width
            updatingValue = currentReward + gammaValue * qValDict[nextStateidx][nextAction]

            # new q value
            newQValue = qValue + alphaValue * (updatingValue - qValue)


            # update q value
            qValDict[stateSidx][actionA] = newQValue

            stateS = nextState
            actionA = nextAction

            if stateS == goal:
                break


    return qValDict



def maxDifferenceBetweenValues(listToCalculate,listToCalculatePrime):
    result = 0
    for i in range(len(listToCalculate)):
        currentValue = abs(listToCalculate[i] - listToCalculatePrime[i])
        if currentValue > result:
            result = currentValue
    return result

def policy_evaluation(thetaValue,currentStatesList,currentPolicyList,width,height,statesList,pitList,obstacleList,pitReward,goalReward,obstacleReward,defaultReward,goal,gammavalue):

    vList = []
    vListPrime = []

    for i in range(len(currentStatesList)):
        vList.append(0)
        vListPrime.append(sys.maxsize)

    while maxDifferenceBetweenValues(vList,vListPrime) > thetaValue:

        vListPrime = copy.deepcopy(vList)

        for i in range(len(currentStatesList)):
            state = currentStatesList[i]
            currentAction = currentPolicyList[i]
            nextState = transitionFunction(state,currentAction,width,height,statesList)

            movingToNextState = True
            for obstacle in obstacleList:
                if obstacle == nextState:
                    movingToNextState = False
                    break
            for pitfall in pitList:
                if pitfall == nextState:
                    movingToNextState = False
                    break

            if nextState == "OUTSIDE" or not movingToNextState:
                nextState = state

            nextStateIndex = (nextState.x - 1) + (nextState.y - 1) * width
            vList[i] = rewardFunction(state,currentAction,width, height, statesList, pitList, obstacleList, pitReward, goalReward, obstacleReward, defaultReward,goal) + (gammavalue * vList[nextStateIndex])

    return vList

def policy_improvement(gammaValue, currentStatesList, currentValueList, currentPolicyList, actionList, width, height, statesList,pitList,obstacleList,pitReward,goalReward,obstacleReward,defaultReward,goal):
    improvedPolicyList = copy.deepcopy(currentPolicyList)

    for i in range(len(currentStatesList)):
        currentState = currentStatesList[i]
        maxQ = -sys.maxsize
        maxAction = ""
        for j in range(len(actionList)):
            currentAction = actionList[j]
            nextState = transitionFunction(currentState,currentAction,width,height,statesList)

            movingToNextState = True
            for obstacle in obstacleList:
                if obstacle == nextState:
                    movingToNextState = False
                    break
            for pitfall in pitList:
                if pitfall == nextState:
                    movingToNextState = False
                    break

            if nextState == "OUTSIDE" or not movingToNextState:
                nextState = currentState

            nextStateIndex = (nextState.x - 1) + (nextState.y - 1) * width
            currentQ = rewardFunction(currentState,currentAction,width, height, statesList, pitList, obstacleList, pitReward, goalReward, obstacleReward, defaultReward,goal) + (gammaValue * currentValueList[nextStateIndex])
            if currentQ > maxQ:
                maxQ = currentQ
                maxAction = currentAction
        improvedPolicyList[i] = maxAction

    return improvedPolicyList

def policy_iteration(gammaValue, thetaValue ,currentStatesList,actionList, width, height, statesList,pitList,obstacleList,pitReward,goalReward,obstacleReward,defaultReward,goal):
    # initialize pi, piPrime
    policyList = []
    policyListPrime = []

    for i in range(len(currentStatesList)):
        x = randrange(4)
        y = randrange(4)
        policyList.append(actionList[x])
        policyListPrime.append(actionList[y])

    while policyList != policyListPrime:

        policyListPrime = copy.deepcopy(policyList)
        valueListPi = policy_evaluation(thetaValue,currentStatesList,policyList, width, height, statesList,pitList,obstacleList,pitReward,goalReward,obstacleReward,defaultReward,goal,gammaValue)
        newPi = policy_improvement(gammaValue,currentStatesList,valueListPi,policyList,actionList, width, height, statesList, pitList, obstacleList, pitReward, goalReward, obstacleReward, defaultReward,goal)
        policyList = newPi

    return policyList

def policyIterationOutputProcess(policyList,M,N):
    outputData = ""
    outputAction = "" #0:North, 1:East, 2:South, 3:West
    for i in range(M):
        for j in range(N):
            if policyList[i + j * M] == "U":
                outputAction = 0
            if policyList[i + j * M] == "R":
                outputAction = 1
            if policyList[i + j * M] == "D":
                outputAction = 2
            if policyList[i + j * M] == "L":
                outputAction = 3
            currentLine = str(i+1) + " " + str(j+1) + " " + str(outputAction) + "\n"
            outputData += currentLine
    return outputData

def sarsaOutputProcess(qValDict,M,N):
    outputData = ""
    outputAction = ""  # 0:North, 1:East, 2:South, 3:West
    for i in range(M):
        for j in range(N):
            currentState = State(i+1,j+1)
            bestAction = findMaxQ(currentState,M,qValDict)
            if bestAction == "U":
                outputAction = 0
            if bestAction == "R":
                outputAction = 1
            if bestAction == "D":
                outputAction = 2
            if bestAction == "L":
                outputAction = 3
            currentLine = str(i + 1) + " " + str(j + 1) + " " + str(outputAction) + "\n"
            outputData += currentLine
    return outputData


def processInput(lines):
    if lines[0].strip() == "P":
        thetaPolicy = float(lines[1].strip())
        gammaPolicy = float(lines[2].strip())
        M,N = map(int,lines[3].strip().split())
        numOfObstacle = int(lines[4].strip())
        obstacles = []
        for i in range(numOfObstacle):
            x,y = map(int,lines[5+i].strip().split())
            obstacles.append(State(x,y))
        numOfPitfall = int(lines[5+numOfObstacle].strip())
        pitfalls = []
        for i in range(numOfPitfall):
            x,y = map(int,lines[6+numOfObstacle+i].strip().split())
            pitfalls.append(State(x,y))
        goalX,goalY = map(int,lines[6+numOfObstacle+numOfPitfall].strip().split())
        goalState = State(goalX,goalY)
        rewardDefault,rewardObstacle,rewardPitfall,rewardGoal = map(float,lines[7+numOfObstacle+numOfPitfall].strip().split())

        actionList = ['R','L','U','D']
        statesList = []
        for j in range(N):
            for i in range(M):
                statesList.append(State(i+1,j+1))

        resultPolicy = policy_iteration(gammaPolicy,thetaPolicy,statesList,actionList,M,N,statesList,pitfalls,obstacles,rewardPitfall,rewardGoal,rewardObstacle,rewardDefault,goalState)
        return policyIterationOutputProcess(resultPolicy,M,N)
    elif lines[0].strip() == "S":
        numberOfEpisodes = int(lines[1].strip())
        alphaSarsa = float(lines[2].strip())
        gammaSarsa = float(lines[3].strip())
        epsilonSarsa = float(lines[4].strip())
        M, N = map(int, lines[5].strip().split())
        numOfObstacle = int(lines[6].strip())
        obstacles = []
        for i in range(numOfObstacle):
            x, y = map(int, lines[7 + i].strip().split())
            obstacles.append(State(x, y))
        numOfPitfall = int(lines[7 + numOfObstacle].strip())
        pitfalls = []
        for i in range(numOfPitfall):
            x, y = map(int, lines[8 + numOfObstacle + i].strip().split())
            pitfalls.append(State(x, y))
        goalX, goalY = map(int, lines[8 + numOfObstacle + numOfPitfall].strip().split())
        goalState = State(goalX, goalY)
        rewardDefault, rewardObstacle, rewardPitfall, rewardGoal = map(float, lines[9 + numOfObstacle + numOfPitfall].strip().split())

        actionList = ['R', 'L', 'U', 'D']
        statesList = []
        for j in range(N):
            for i in range(M):
                statesList.append(State(i + 1, j + 1))

        QValuesDict = {}

        resultSarsaQValDict = sarsa(numberOfEpisodes,alphaSarsa,gammaSarsa,epsilonSarsa,M,N,goalState,pitfalls,obstacles,rewardDefault,rewardObstacle,rewardPitfall,rewardGoal,statesList,actionList,obstacles,QValuesDict)
        return sarsaOutputProcess(resultSarsaQValDict,M,N)

    else:
        print("Invalid method.")
        return


def main():
    if len(sys.argv) != 3:
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(input_file, 'r') as infile:
            lines = infile.readlines()
            outputData = processInput(lines)
    except FileNotFoundError:
        print("Error: File "+ input_file + " not found.")
        sys.exit(1)

    try:
        with open(output_file, 'w') as outfile:
            outfile.write(str(outputData))
    except Exception as e:
        print("Error writing to file " + output_file + " : " + e)
        sys.exit(1)

if __name__ == "__main__":
    main()