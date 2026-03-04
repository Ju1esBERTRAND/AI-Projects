# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman_AIC.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman_AIC.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newGhostsPos = [ghostState.getPosition() for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        print("NEW TURN")
        print(successorGameState)
        print(newPos)
        print(newFood.asList())
        print(newGhostStates)
        print(newScaredTimes)
        print(newGhostsPos)

        actionScore = 0  # variable that keeps track of the score

        currentGhost = 0
        for i in newGhostsPos: 
            if abs(newPos[0] - i[0]) + abs(newPos[1] - i[1]) <= 1:
                if newScaredTimes[currentGhost] == 0:  # we don't go next to a ghost
                    actionScore -= 100 
                else:                                  # we eat the ghost if we can
                    actionScore += 100
            currentGhost += 1

        if currentGameState.getPacmanPosition() == newPos:  # we discourage stationary play
            actionScore -= 25
    
        for i in currentGameState.getFood().asList():  # we encourage eating a fruit
            if abs(newPos[0] - i[0]) + abs(newPos[1] - i[1]) == 0:
                actionScore += 50
                return actionScore

        nearestFood = 999 
        for i in newFood.asList():  # we try going towards a fruit
            distance = abs(newPos[0] - i[0]) + abs(newPos[1] - i[1])
            if distance <= nearestFood:
                nearestFood = distance
        actionScore -= nearestFood

        return actionScore

      

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 5)
    """
    def MAX_VALUE(self, gameState, d):
        if gameState.isWin() or gameState.isLose() or d == 0:
            return self.evaluationFunction(gameState)
        else:
            legalMoves = gameState.getLegalActions(0)
            v = -2000000
            for a in legalMoves:
                v = max(v, self.MIN_VALUE(gameState.generateSuccessor(0, a), d - 1, 1))
            return v

    def MIN_VALUE(self, gameState, d, indexagent):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        else:
            legalMoves = gameState.getLegalActions(indexagent)
            v = 2000000
            if indexagent == gameState.getNumAgents() - 1:
                for a in legalMoves:
                    v = min(v, self.MAX_VALUE(gameState.generateSuccessor(indexagent, a), d))
                return v
            else:
                for a in legalMoves:
                    v = min(v, self.MIN_VALUE(gameState.generateSuccessor(indexagent, a), d, indexagent + 1))
                return v

    def MINIMAX_DECISION(self, gameState):
        legalMoves = gameState.getLegalActions(0)
        v = -2000000
        max = -2000000
        chosen_action = ''
        for a in legalMoves:
            v = self.MIN_VALUE(gameState.generateSuccessor(0,a),self.depth,1)
            if v >= max:
                max = v
                chosen_action = a
        return chosen_action

   
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.MINIMAX_DECISION(gameState)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 6)
    """
    def MAX_VALUE(self, gameState, d, alpha, beta):
        if gameState.isWin() or gameState.isLose() or d == 0:
            return self.evaluationFunction(gameState)
        else:
            legalMoves = gameState.getLegalActions(0)
            v = -2000000
            for a in legalMoves:
                v = max(v, self.MIN_VALUE(gameState.generateSuccessor(0, a), d - 1, 1, alpha, beta))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

    def MIN_VALUE(self, gameState, d, indexagent, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        else:
            legalMoves = gameState.getLegalActions(indexagent)
            v = 2000000
            if indexagent == gameState.getNumAgents() - 1:
                for a in legalMoves:
                    v = min(v, self.MAX_VALUE(gameState.generateSuccessor(indexagent, a), d, alpha, beta))
                    if v <= alpha:
                        return v
                    beta = min(beta, v)
                return v
            else:
                for a in legalMoves:
                    v = min(v, self.MIN_VALUE(gameState.generateSuccessor(indexagent, a), d, indexagent + 1, alpha, beta))
                    if v <= alpha:
                        return v
                    beta = min(beta, v)
                return v
            
    def ALPHA_BETA_SEARCH(self, gameState):
        legalMoves = gameState.getLegalActions(0)
        v = -2000000
        max = -2000000
        chosen_action = ''
        alpha = -2000000
        beta = 2000000
        for a in legalMoves:
            v = self.MIN_VALUE(gameState.generateSuccessor(0,a),self.depth,1, alpha, beta)
            if v >= max:
                max = v
                chosen_action = a
        return chosen_action

            

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.ALPHA_BETA_SEARCH(gameState)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 7)
    """

    def MAX_VALUE(self, gameState, d):
        if gameState.isWin() or gameState.isLose() or d == 0:
            return self.evaluationFunction(gameState)
        else:
            legalMoves = gameState.getLegalActions(0)
            v = -2000000
            for a in legalMoves:
                v = max(v, self.CHANCE_VALUE(gameState.generateSuccessor(0, a), d - 1, 1))
            return v

    def CHANCE_VALUE(self, gameState, d, indexagent):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        else:
            legalMoves = gameState.getLegalActions(indexagent)
            v = 0
            if indexagent == gameState.getNumAgents() - 1:
                for a in legalMoves:
                    v += self.MAX_VALUE(gameState.generateSuccessor(indexagent, a), d) * (1.0/len(legalMoves))
                return v
            else:
                for a in legalMoves:
                    v = self.CHANCE_VALUE(gameState.generateSuccessor(indexagent, a), d, indexagent + 1) * (1.0/len(legalMoves))
                return v

    def EXPECTIMAX(self, gameState):
        legalMoves = gameState.getLegalActions(0)
        v = -2000000
        max = -2000000
        chosen_action = ''
        for a in legalMoves:
            v = self.CHANCE_VALUE(gameState.generateSuccessor(0,a),self.depth,1)
            if v > max:
                max = v
                chosen_action = a
        return chosen_action

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.EXPECTIMAX(gameState)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 8).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction