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
               first='TopAgent', second='BottomAgent'):
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
class OffensiveAndDefensiveReflexAgent(ReflexCaptureAgent):
    """
    A reflex agent that seeks food. This is an agent
    we give you to get an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """

    favorHeight = 0.0

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
        currGPosition = gameState.getGhostPositions()

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
        return gameState.getScore() + (1 / minFoodDistance + rtrnVal) * (1 / rfVal * 1 / ncLeft)

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
        opponents = [successor.getAgentState(oppo) for oppo in self.getOpponents(successor)]
        # Ghost positions stores an array of tuple i.e., [ (0,3), ... ]
        ghostPos = []
        opponentPacmen = []
        for oppo in opponents:
            if oppo.getPosition() is not None:
                # If this opponent is not a pacman, then it's a ghost.
                if not oppo.isPacman:
                    ghostPos.append(oppo)
                else:
                    opponentPacmen.append(oppo)

        numFoods = len(foodList)
        distG = len(ghostPos)
        numCaps = len(cLeft)

        # If food is nearby #
        if numFoods > 0:
            minDistance = min([self.getMazeDistance(currentPos, food) for food in foodList])
            # features['distanceToFood'] = float(minDistance)/(walls.width * walls.height)
            features['distanceToFood'] = min([self.getSmartDistance(currentPos, food) for food in foodList])
            features['foodLeft'] = numFoods

        # If caps is nearby #
        if numCaps > 0:
            nearestDistance = min([self.getMazeDistance(currentPos, caps) for caps in cLeft])
            if nearestDistance == 0:
                nearestDistance = 1000
            features['distanceToCaps'] = nearestDistance

        features['enemyValues'] = self.getEnemyVals(currentPos, opponentPacmen)

        # If ghost is nearby #
        if distG > 0:
            evaluateG = 0.0
            dist = 0.0
            ghostR = self.getGhostPositions(ghostPos, True)
            ghostScared = self.getGhostPositions(ghostPos, False)
            distGR = len(ghostR)
            distGS = len(ghostScared)

            # If regular ghost is near #
            if distGR > 0:
                evaluateG = self.computeMinDistance(currentPos, ghostR)
                if evaluateG <= 1:
                    evaluateG = -float('inf')

            # If scared ghost is near #
            if distGS > 0:
                dist = self.computeMinDistance(currentPos, ghostScared)
            if dist < evaluateG or evaluateG == 0:
                if dist == 0:
                    features['ghostScared'] = 10000
            features['distanceToGhost'] = evaluateG

        # Uses feature function from baselineTeam's defensiveAgent #
        if action == Directions.STOP: features['stop'] = 1
        rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
        if action == rev: features['reverse'] = 1

        if self.goHome(gameState):
            features['timeToGoHome'] = self.getMazeDistance(self.start, currentPos) * 100000

        if self.goHomeOccasionally(gameState):
            features['goingHome'] = self.getMazeDistance(self.start, currentPos) * 100000

        return features

    def getWeights(self, gameState, action):
        return {'successorScore': 100, 'distanceToFood': -2, 'foodLeft': -2, 'distanceToCaps': -1, 'ghostScared': -10,
                'distanceToGhost': 3, 'enemyValues': -110, 'stop': -1000, 'reverse': -2, 'timeToGoHome': -20,
                'goingHome': -10}

    def getGhostPositions(self, ghostPos, isRegular):
        tempArr = []
        for ghost in ghostPos:
            if isRegular and ghost.scaredTimer == 0:
                tempArr.append(ghost)
            elif ghost.scaredTimer > 0:
                tempArr.append(ghost)
        return tempArr

    def computeMinDistance(self, currentPos, ghosts):
        # A temp array used for finding minimum distance between current position and the ghost
        ghostDistArr = []
        for ghost in ghosts:
            ghostDistArr.append(self.getMazeDistance(currentPos, ghost.getPosition()))
        return min(ghostDistArr)

    # If opponent pacman is nearby #
    def getEnemyVals(self, currentPos, opponentPacmen):
        numOppo = len(opponentPacmen)
        if numOppo > 0:
            distance = [self.getMazeDistance(currentPos, oppo.getPosition()) for oppo in opponentPacmen]
            distLength = len(distance)
            if distLength > 0:
                minDistance = min(distance)
                return minDistance
        return 0

    # Go home with food when time is almost up #
    def goHome(self, gameState):
        foodsCarried = gameState.getAgentState(self.index).numCarrying
        return gameState.data.timeleft < 250 and foodsCarried > 0

    # Go home with every 3 food pellet collected #
    def goHomeOccasionally(self, gameState):
        foodsCarried = gameState.getAgentState(self.index).numCarrying
        return foodsCarried > 2

    def getSmartDistance(self, myPos, food):
        return self.getMazeDistance(myPos, food) + abs(self.favorHeight - food[1])


class TopAgent(OffensiveAndDefensiveReflexAgent):
    def registerInitialState(self, gameState):
        OffensiveAndDefensiveReflexAgent.registerInitialState(self, gameState)
        self.favorHeight = gameState.data.layout.height


class BottomAgent(OffensiveAndDefensiveReflexAgent):
    def registerInitialState(self, gameState):
        OffensiveAndDefensiveReflexAgent.registerInitialState(self, gameState)
        self.favorHeight = 0.0

