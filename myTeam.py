# myTeam.py
# ---------
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


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
from util import nearestPoint
from util import manhattanDistance
import game


#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first='OffensiveReflexAgent', second='DefensiveReflexAgent'):
    """
    This function should return a list of two agents that will form the
    team, initialized using firstIndex and secondIndex as their agent
    index numbers.  isRed is True if the red team is being created, and
    will be False if the blue team is being created.

    As a potentially helpful development aid, this function can take
    additional string-valued keyword arguments ("first" and "second" are
    such arguments in the case of this function), which will come from
    the --redOpts and --blueOpts command-line arguments to capture.py.
    For the nightly contest, however, your team will be created without
    any extra arguments, so you should make sure that the default
    behavior is what you want for the nightly contest.
    """

    # The following line is an example only; feel free to change it.
    return [eval(first)(firstIndex), eval(second)(secondIndex)]


##########
# Agents #
##########

class ReflexCaptureAgent(CaptureAgent):
    """
    A base class for reflex agents that chooses score-maximizing actions
    """

    def registerInitialState(self, gameState):
        self.start = gameState.getAgentPosition(self.index)
        CaptureAgent.registerInitialState(self, gameState)

    def chooseAction(self, gameState):
        """
        Picks among the actions with the highest Q(s,a).
        """
        actions = gameState.getLegalActions(self.index)

        # You can profile your evaluation time by uncommenting these lines
        # start = time.time()
        values = [self.evaluate(gameState, a) for a in actions]
        # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]

        foodLeft = len(self.getFood(gameState).asList())

        if foodLeft <= 2:
            bestDist = 9999
            for action in actions:
                successor = self.getSuccessor(gameState, action)
                pos2 = successor.getAgentPosition(self.index)
                dist = self.getMazeDistance(self.start, pos2)
                if dist < bestDist:
                    bestAction = action
                    bestDist = dist
            return bestAction

        return random.choice(bestActions)

    def getSuccessor(self, gameState, action):
        """
        Finds the next successor which is a grid position (location tuple).
        """
        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()
        if pos != nearestPoint(pos):
            # Only half a grid position was covered
            return successor.generateSuccessor(self.index, action)
        else:
            return successor

    def evaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights
        """
        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        return features * weights

    def getFeatures(self, gameState, action):
        """
        Returns a counter of features for the state
        """
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        features['successorScore'] = self.getScore(successor)
        return features

    def getWeights(self, gameState, action):
        """
        Normally, weights do not depend on the gamestate.  They can be either
        a counter or a dictionary.
        """
        return {'successorScore': 1.0}

# Uses expectimax adversial searh for now, will improve offensive agent. #
class OffensiveReflexAgent(ReflexCaptureAgent):
    """
    A reflex agent that seeks food. This is an agent
    we give you to get an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """
    def actions(self, gameState):
        legalMoves = gameState.getLegalActions(0)
        scores = []
        # Choose one of the best actions
        for move in legalMoves:
            successorGameState = gameState.generateSuccessor(0, move)
            scores.append(self.value(successorGameState, 1, 0))
        bestScore = max(scores)
        bestIndices = []

        for index in range(len(scores)):
            if scores[index] != bestScore:
                continue
            bestIndices.append(index)

        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best
        return legalMoves[chosenIndex]

    def value(self, gameState, agent, currentDepth):
        if gameState.isLose() or len(
                gameState.getLegalActions(0)) == 0 or self.depth == currentDepth or gameState.isWin():
            return self.evaluationFunction(gameState)

        if agent > 0 or agent < 0:
            return self.getExpValue(gameState, agent, currentDepth)
        else:
            return self.getMaxValue(gameState, currentDepth)

    def getMaxValue(self, gameState, currentDepth):
        maximum = -9999
        legalMoves = gameState.getLegalActions(0)
        tempArr = []
        for move in legalMoves:
            tempArr.append(max(maximum, self.value(gameState.generateSuccessor(0, move), 1, currentDepth)))
        return max(tempArr)

    def getExpValue(self, gameState, agent, currentDepth):
        minimum = 0
        if agent == gameState.getNumAgents():
            currentDepth += 1
            return self.value(gameState, 0, currentDepth)
        legalMoves = gameState.getLegalActions(agent)
        for move in legalMoves:
            minimum += self.value(gameState.generateSuccessor(agent, move), agent + 1, currentDepth)
        return minimum / len(legalMoves)

    def evaluationFunction(gameState):

        rValue = random.getrandbits(256)
        largeV = 100000
        currentP = gameState.getPacmanPosition()
        currFood = gameState.getFood().asList()
        foodD = []
        ghostD = []
        currGPosition= gameState.getGhostPositions()

        rtrnVal = 0
        if gameState.isWin():
            rtrnVal += largeV
        elif gameState.isLose():
            rtrnVal -= largeV

        minFoodDistance = 1
        for i in currFood:
            rangeDist = manhattanDistance(currentP, i)
            foodD.append(rangeDist)
            # Look for closest food. #
            minFoodDistance = min(foodD[0], rangeDist)

        for j in currGPosition:
            ghostD.append(manhattanDistance(currentP, j))

        for g in ghostD:
            if g < 2:
                return -(rValue + largeV)
            elif currentP == g:
                return -(rValue + largeV)

        rfVal = 1
        # Numbers of foods left. #
        rFoods = gameState.getNumFood()
        rfVal += rFoods * 999999

        # Numbers of capsules left.#
        cLeft = gameState.getCapsules()
        numCLeft = len(cLeft)
        ncLeft = 1
        ncLeft += numCLeft * 9999999

        # Better evaluation function hence take into account the additional factors. #
        return gameState.getScore() + (1/minFoodDistance + rtrnVal) * (1/rfVal * 1/ncLeft)

    def getFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        foodList = self.getFood(successor).asList()
        cLeft = self.getCapsules(gameState)
        features['successorScore'] = self.getScore(successor)

        # Get all states of ghost, food, opponent pacman, walls.
        walls = gameState.getWalls()
        currentState = successor.getAgentState(self.index)
        currentPos = currentState.getPosition()
        opponents = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        ghostPos = [x for x in opponents if not x.isPacman and x.getPosition() != None]
        opponentPacman = [y for y in opponents if y.isPacman and y.getPosition() != None]
        numFoods = len(foodList)
        distG = len(ghostPos)
        distOP = len(opponentPacman)
        numCaps = len(cLeft)

        # blueFood = gameState.getBlueFood().asList()
        # redFood = gameState.getRedFood().asList()
        # if gameState.isOnRedTeam(self.index):
        #     if len(blueFood) != 0:
        #         features['successorScore'] = -float(len(foodList)) / len(blueFood)
        # else:
        #     if len(redFood) != 0:
        #         features['successorScore'] = -float(len(foodList)) / len(redFood)

        # If food is nearby #
        if numFoods > 0:
            minDistance = min([self.getMazeDistance(currentPos, food) for food in foodList])
            features['distanceToFood'] = float(minDistance) /(walls.width * walls.height)
            features['foodLeft'] = numFoods

        # If caps is nearby #
        if numCaps > 0:
            minDistance = min([self.getMazeDistance(currentPos, caps) for caps in cLeft])
            if minDistance == 0:
                minDistance = -100
            features['distanceToCaps'] = minDistance

        # If opponent pacman is in our map
        if distOP > 0:
            minDistance = min([self.getMazeDistance(currentPos, i.getPosition()) for i in opponentPacman])
            features['distanceToOP'] = minDistance + 1

        # If ghost is nearby #
        # if distG > 0:
        #     evaluateG = 0.0
        #     dist = 0.0
        #     ghostR = [ghost for ghost in ghostPos if ghost.scaredTimer == 0]
        #     ghostScared = [ghost for ghost in opponents if ghost.scaredTimer > 0]
        #     distGR = len(ghostR)
        #     distGS = len(ghostScared)
        #
        #     if distGR > 0:
        #         evaluateG = min([self.getMazeDistance(currentPos, ghost.getPosition()) for ghost in ghostR])
        #         if evaluateG <= 1: evaluateG = -float('inf')
        #
        #     if distGS > 0:
        #         dist = min([self.getMazeDistance(currentPos, ghost.getPosition()) for ghost in ghostScared])
        #     if dist < evaluateG or evaluateG == 0:
        #         if dist == 0: features['scaredG'] = -10
        #     features['distanceToG'] = evaluateG

        if len(ghostPos) > 0:
            ghostEval = 0.0
            scaredDistance = 0.0
            regGhosts = [ghost for ghost in ghostPos if ghost.scaredTimer == 0]
            scaredGhosts = [ghost for ghost in ghostPos if ghost.scaredTimer > 0]
            if len(regGhosts) > 0:
                ghostEval = min([self.getMazeDistance(currentPos, ghost.getPosition()) for ghost in regGhosts])
                if ghostEval <= 1:  ghostEval = -float('inf')

            if len(scaredGhosts) > 0:
                scaredDistance = min([self.getMazeDistance(currentPos, ghost.getPosition()) for ghost in scaredGhosts])
            if scaredDistance < ghostEval or ghostEval == 0:
                if scaredDistance == 0: features['ghostScared'] = -10
            features['distanceToGhost'] = ghostEval

        # Uses feature function from baselineTeam's defensiveAgent #
        if action == Directions.STOP: features['stop'] = 1
        rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
        if action == rev: features['reverse'] = 1

        return features

    def getWeights(self, gameState, action):
        return {'successorScore': 100, 'distanceToFood': -2, 'foodLeft': -2, 'distanceToCaps': -1, 'distanceToOP': -70,
                'ghostScared': -1,  'distanceToGhost': 3, 'stop': -100, 'reverse': -2}

# Standard defensive agent implemented from baseline team, own defensive not implemented yet.
class DefensiveReflexAgent(ReflexCaptureAgent):
    """
    A reflex agent that keeps its side Pacman-free. Again,
    this is to give you an idea of what a defensive agent
    could be like.  It is not the best or only way to make
    such an agent.
    """

    def getFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)

        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # Computes whether we're on defense (1) or offense (0)
        features['onDefense'] = 1
        if myState.isPacman: features['onDefense'] = 0

        # Computes distance to invaders we can see
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
        features['numInvaders'] = len(invaders)
        if len(invaders) > 0:
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)

        if action == Directions.STOP: features['stop'] = 1
        rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
        if action == rev: features['reverse'] = 1

        return features

    def getWeights(self, gameState, action):
        return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}
