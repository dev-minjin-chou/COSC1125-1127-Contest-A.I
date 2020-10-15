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
               first='TopAgent', second='DefensiveAgent'):
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


def getMapLayout(gameState):
    mapInfo = {}
    width = gameState.data.layout.width
    height = gameState.data.layout.height
    centerX = int((width - 2) / 2)
    centerY = int((height - 2) / 2)

    mapInfo['width'] = width
    mapInfo['height'] = height
    mapInfo['centerX'] = centerX
    mapInfo['centerY'] = centerY

    return mapInfo


class OffensiveAndDefensiveAgent(ReflexCaptureAgent):
# Uses expectimax adversial searh for now, will improve offensive agent. #
class OffensiveAgent(ReflexCaptureAgent):
    """
    A reflex agent that seeks food. This is an agent
    we give you to get an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """

    def __init__(self, index):
        CaptureAgent.__init__(self, index)

        self.agentPosition = (0, 0)
        self.agentStartPosition = (0, 0)
        self.normalOp = False
        self.firstGoalArea = []

    def registerInitialState(self, gameState):
        ReflexCaptureAgent.registerInitialState(self, gameState)
        self.agentStartPosition = gameState.getAgentState(self.index).getPosition()
        self.setFirstGoalArea(gameState)

    def chooseAction(self, gameState):
        self.agentPosition = gameState.getAgentState(self.index).getPosition()

        actions = gameState.getLegalActions(self.index)
        actions.remove(Directions.STOP)
        scores = []

        if self.agentPosition == self.agentStartPosition:
            self.normalOp = True

        # If the agent reaches first goal area (middle of the map)
        if self.agentPosition == self.firstGoalArea:
            self.normalOp = False

        for action in actions:
            successorGameState = gameState.generateSuccessor(self.index, action)
            score = 0
            if self.normalOp:
                successor = self.getSuccessor(gameState, action)
                position = successor.getAgentPosition(self.index)
                scores.append(self.getMazeDistance(position, self.firstGoalArea[0]))
            else:
                for i in range(1, 24):
                    score += self.simulateMonteCarlo(successorGameState, 12)
                scores.append(score)
        best = min(scores)
        bestActions = [a for a, v in zip(actions, scores) if v == best]
        bestAction = random.choice(bestActions)
        return bestAction

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
            features['distanceToFood'] = minDistance
            features['foodLeft'] = numFoods

        # If caps is nearby #
        # if numCaps > 0:
        #     nearestDistance = min([self.getMazeDistance(currentPos, caps) for caps in cLeft])
        #     if nearestDistance == 0:
        #         nearestDistance = 1000
        #     features['distanceToCaps'] = nearestDistance

        # Chase enemy
        # features['enemyValues'] = self.getEnemyVals(currentPos, opponentPacmen)

        # If ghost is nearby #
        if distG > 0:
            evaluateG = 0.0
            # dist = 0.0
            ghostR = self.getGhostPositions(ghostPos, True)
            ghostScared = self.getGhostPositions(ghostPos, False)
            distGR = len(ghostR)
            # distGS = len(ghostScared)

            # If regular ghost is near #
            if distGR > 0:
                evaluateG = self.computeMinDistance(currentPos, ghostR)

            # If scared ghost is near #
            # if distGS > 0:
            #     dist = self.computeMinDistance(currentPos, ghostScared)
            # if dist < evaluateG or evaluateG == 0:
            #     if dist == 0:
            #         features['ghostScared'] = 10
            features['distanceToGhost'] = evaluateG

        # Uses feature function from baselineTeam's defensiveAgent #
        # if action == Directions.STOP:
        #     features['stop'] = 1
        # rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
        # if action == rev:
        #     features['reverse'] = 1

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

    def setFirstGoalArea(self, gameState):
        mapInfo = getMapLayout(gameState)
        for i in range(1, mapInfo['height'] - 1):
            if not gameState.hasWall(mapInfo['centerX'], i):
                self.firstGoalArea.append((mapInfo['centerX'], i))

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

    def simulateMonteCarlo(self, gameState, rounds):
        simulatedState = gameState.deepCopy()
        while rounds > 0:
            simulatedAction = self.decidingFavorableActions(simulatedState)
            simulatedState = simulatedState.generateSuccessor(self.index, simulatedAction)
            rounds = rounds - 1
        return self.evaluate(simulatedState, Directions.STOP)

    def decidingFavorableActions(self, simulatedState):
        actionsBase = simulatedState.getLegalActions(self.index)
        actionsBase.remove(Directions.STOP)
        if len(actionsBase) == 1:
            return actionsBase[0]
        else:
            backwardsDirection = Directions.REVERSE[simulatedState.getAgentState(self.index).configuration.direction]
            if backwardsDirection in actionsBase:
                actionsBase.remove(backwardsDirection)
            return random.choice(actionsBase)


SHOULD_DEFEND_COUNTER = 4
REMAINING_FOODS = 10


class DefensiveAgent(ReflexCaptureAgent):
    def __init__(self, index):
        CaptureAgent.__init__(self, index)
        self.defendingArea = []
        self.lastCheckedFoods = []
        self.goal = None
        self.counter = 0

    def registerInitialState(self, gameState):
        CaptureAgent.registerInitialState(self, gameState)
        self.distancer.getMazeDistances()
        self.setPatrolArea(gameState)

    def getMapLayout(self, gameState):
        mapInfo = {}
        width = gameState.data.layout.width
        height = gameState.data.layout.height
        centerX = int((width - 2) / 2)
        centerY = int((height - 2) / 2)

        mapInfo['width'] = width
        mapInfo['height'] = height
        mapInfo['centerX'] = centerX
        mapInfo['centerY'] = centerY

        return mapInfo

    def setPatrolArea(self, gameState):
        mapLayout = getMapLayout(gameState)

        for i in range(1, mapLayout['height'] - 1):
            centerX = mapLayout['centerX']
            if not gameState.hasWall(centerX, i):
                self.defendingArea.append((centerX, i))

        # Remove defending coordinate until only one coordinate left in the defendingArea
        while len(self.defendingArea) > 2:
            del self.defendingArea[0]
            # Remove last index
            self.defendingArea = self.defendingArea[:-1]

    def getPreferredDirections(self, gameState):
        # Filter out unwanted actions
        legalActions = gameState.getLegalActions(self.index)
        legalActions.remove(Directions.STOP)
        currentDirection = gameState.getAgentState(self.index).configuration.direction
        reversedDir = Directions.REVERSE[currentDirection]
        if reversedDir in legalActions:
            legalActions.remove(reversedDir)

        preferredDirections = []
        for act in legalActions:
            isPacman = gameState.generateSuccessor(self.index, act).getAgentState(self.index).isPacman
            if not isPacman:
                preferredDirections.append(act)

        if len(preferredDirections) == 0:
            self.counter = 0
        else:
            self.counter = self.counter + 1

        if self.counter == 0 or self.counter > SHOULD_DEFEND_COUNTER:
            preferredDirections.append(reversedDir)

        return preferredDirections

    def chooseAction(self, gameState):
        foods = self.getFoodYouAreDefending(gameState).asList()
        agentPosition = gameState.getAgentPosition(self.index)
        if agentPosition == self.goal:
            self.goal = None

        closestEnemies = []
        minDistance = float("inf")

        enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
        invaders = []
        for enemy in enemies:
            if enemy.isPacman and enemy.getPosition() is not None:
                oppentPos = enemy.getPosition()
                invaders.append(oppentPos)

        if len(invaders) > 0:
            for enemy in invaders:
                distance = self.getMazeDistance(enemy, agentPosition)
                if distance < minDistance:
                    minDistance = distance
                    closestEnemies.append(enemy)
            self.goal = closestEnemies[-1]
        else:
            # If number of current foods are less than last checked foods, it means
            # some foods had been consumed by the enemy and the defensive agent couldn't protect it.
            # So, set the goal to previously consumed food.
            if len(foods) < len(self.lastCheckedFoods):
                consumedFood = set(self.lastCheckedFoods) - set(foods)
                self.goal = consumedFood.pop()

        self.lastCheckedFoods = foods

        if self.goal is None:
            if len(foods) <= REMAINING_FOODS:
                importantFoods = foods + self.getCapsulesYouAreDefending(gameState)
                self.goal = random.choice(importantFoods)
            else:
                self.goal = random.choice(self.defendingArea)

        preferredDirections = self.getPreferredDirections(gameState)
        foodDist = []

        for direction in preferredDirections:
            pos = gameState.generateSuccessor(self.index, direction).getAgentPosition(self.index)
            foodDist.append(self.getMazeDistance(pos, self.goal))

        bestActions = [direction for direction, food in zip(preferredDirections, foodDist) if food == min(foodDist)]
        return random.choice(bestActions)
