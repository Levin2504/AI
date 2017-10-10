# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import Directions
from game import Agent
from heuristics import scoreEvaluation
import random


class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0, len(actions) - 1)]


class GreedyAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generateSuccessor(0, action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(scoreEvaluation(state), action) for state, action in successors]
        # get best choice
        bestScore = max(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)


class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write BFS Algorithm instead of returning Directions.STOP
        legal = state.getLegalPacmanActions()
        lastLayerState = [(state.generatePacmanSuccessor(action), action) for action in legal]
        overtime = False

        for i in lastLayerState:
            if i[0].isWin():
                return i[1]

        while (True):
            tempState = []  # current layer nodes, frontier nodes
            for i in lastLayerState:  # for loop to extend all nodes in last layer and store in current layer
                legal = i[0].getLegalPacmanActions()
                for j in legal:
                    nextState = i[0].generatePacmanSuccessor(j)
                    if nextState is not None:  # if not timeout
                        if nextState.isLose():  # if child node is lose state, ignore
                            continue
                        elif nextState.isWin():
                            return i[1]
                        else:
                            tempState.append((nextState, i[1]))  # if not, extend it
                    else:
                        overtime = True
                        break
            if overtime:
                break
            else:
                lastLayerState = tempState  # explored node (only last layer)

        scored = []

        for i in lastLayerState:  # when timeout, check nodes in last layer
            scored.append((scoreEvaluation(i[0]), i[1]))

        bestScore = max(scored)[0]
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        return random.choice(bestActions)


class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write DFS Algorithm instead of returning Directions.STOP
        legal = state.getLegalPacmanActions()
        extendedNote = []  # explored node
        checkingStack = []  # frontier node
        overtime = False

        for i in legal:
            checkingStack.append((state.generatePacmanSuccessor(i), i))
            # tuple in stack: (state, firststep's direction)

        while (True):
            if not len(checkingStack):  # if no element in checking stack, go to evaluation
                break
            topElement = checkingStack.pop()  # check the top of the stack
            legal = topElement[0].getLegalPacmanActions()
            # extend top element
            for i in legal:
                childState = topElement[0].generatePacmanSuccessor(i)
                if childState is None:
                    overtime = True
                    break
                elif childState.isWin():
                    # if next state is win, put it into evaluation list but not check its future state
                    extendedNote.append((childState, topElement[1]))
                elif not childState.isLose():
                    # if next state is not lose, put it into checking stack for future
                    checkingStack.append((childState, topElement[1]))
                    # if next state is lose, never check it or evaluate it
            # record for evaluation
            extendedNote.append(topElement)
            if overtime:
                break

        extendedNote.extend(checkingStack)  # for evaluation, count on all known state

        scored = []
        for i in extendedNote:
            scored.append((scoreEvaluation(i[0]), i[1]))

        bestScore = max(scored)[0]
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        return random.choice(bestActions)


class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write A* Algorithm instead of returning Directions.STOP
        legal = state.getLegalPacmanActions()
        depthCoefficient = 1  # set a coefficient to modify
        overtime = False
        checkingList = []

        for i in legal:
            childState = state.generatePacmanSuccessor(i)
            cost = 1 * depthCoefficient - (scoreEvaluation(childState) - scoreEvaluation(state))
            checkingList.append((state.generatePacmanSuccessor(i), i, cost, 1))
            # tuple in list: (state, firststep's direction, cost, depth)

        for i in checkingList:
            if i[0].isWin():
                return i[1]

        while (True):
            if not len(checkingList):
                return Directions.STOP
            minCost = (checkingList[0])[2]
            for i in checkingList:
                if i[2] < minCost:
                    minCost = i[2]
            # minCost = min(checkingList)[2]
            bestNodes = [checkingList.index(i) for i in checkingList if i[2] == minCost]
            if not len(bestNodes):
                return
            choosenNode = checkingList.pop(random.choice(bestNodes))
            legal = choosenNode[0].getLegalPacmanActions()
            for i in legal:
                childState = choosenNode[0].generatePacmanSuccessor(i)
                if childState is None:
                    overtime = True
                    break
                elif childState.isWin():
                    return choosenNode[1]
                elif not childState.isLose():
                    cost = (1 + choosenNode[3]) * depthCoefficient - \
                           (scoreEvaluation(childState) - scoreEvaluation(state))
                    checkingList.append((childState, choosenNode[1], cost, choosenNode[3] + 1))
                    # if next state is lose, never check it or evaluate it
            if overtime:
                break

        # minCost = min(checkingList)[2]
        minCost = (checkingList[0])[2]
        for i in checkingList:
            if i[2] <= minCost:
                minCost = i[2]
        bestNodes = [checkingList.index(i) for i in checkingList if i[2] == minCost]
        return (checkingList[(random.choice(bestNodes))])[1]
