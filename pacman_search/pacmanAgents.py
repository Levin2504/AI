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
        extendedNote = []

        while (True):
            tempState = []
            for i in lastLayerState:
                legal = i[0].getLegalPacmanActions()
                for j in legal:
                    nextState = i[0].generatePacmanSuccessor(j)
                    if nextState is not None:
                        tempState.append((nextState, i[1]))
                    else:
                        overtime = True
                        break
            if overtime:
                break
            else:
                extendedNote.extend(tempState)
                lastLayerState = tempState

        scored = []

        for i in extendedNote:
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
        depth = 17
        legal = state.getLegalPacmanActions()
        overtime = False
        extendedNote = []
        checkingStack = [(state.generatePacmanSuccessor(action),
                          state.generatePacmanSuccessor(action).getLegalPacmanActions(), action) for action in legal]

        while (True):
            if not len(checkingStack):
                break
            last = len(checkingStack) - 1
            if last > depth:
                checkingStack.pop()
                continue
            topElement = checkingStack[last]
            if len(topElement[1]):

                if topElement[0].isWin():
                    return topElement[2]
                elif topElement[0].isLose():
                    checkingStack.pop()
                    continue
                newTop = topElement[0].generatePacmanSuccessor(
                    (topElement[1])[len(topElement[1]) - 1])
                tempTuple = checkingStack.pop()
                tempList = tempTuple[1]
                tempList.pop(int(random.random() * (len(tempList))))
                checkingStack.append((tempTuple[0], tempList, tempTuple[2]))
                if newTop is not None:
                    checkingStack.append((newTop, newTop.getLegalPacmanActions(), topElement[2]))
                    extendedNote.append((newTop, topElement[2]))
                else:
                    overtime = True
                    break
            else:
                checkingStack.pop()

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
        return Directions.STOP
