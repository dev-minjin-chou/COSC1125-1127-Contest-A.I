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
import random, util
from game import Directions
from util import nearestPoint


#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first='OffensiveAgent', second='DefensiveAgent'):
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

# Define global constants for representing the weights of features
# Flags for offensive agent
TRUE = 1
FALSE = 0
ENFORCE_OFFENSE = 20
GHOST_SAFE_DISTANCE = 5
WEIGHT_SCORE = 200
WEIGHT_FOOD = -5
WEIGHT_SCARED_GHOST = 0
WEIGHT_NORMAL_GHOST = 210
WEIGHT_SHOULD_ATTACK = 3000
WEIGHT_SHOULD_GO_BACK = 0

# Flags for defensive agent
REMAINING_FOODS = 4
SHOULD_DEFEND_COUNTER = 4

class ReflexCaptureAgent(CaptureAgent):
    """
    A base class for reflex agents that chooses score-maximizing actions
    """

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

#
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
        self.shouldAttack = False
        self.shouldGoBack = 0

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

        successor = self.getSuccessor(gameState, action)  # get the successor
        myPos = successor.getAgentState(self.index).getPosition()  # get the successor pos
        foodList = self.getFood(successor).asList()  # get the foodlist
        features['successorScore'] = self.getScore(successor)  # set score feature

        # if the agent at the successor's pos becomes an pacman,
        if successor.getAgentState(self.index).isPacman:
            features['forcedOffensive'] = TRUE
        else:
            features['forcedOffensive'] = FALSE

        # Compute distance to the nearest food
        if len(foodList) > 0:  # This should always be True,  but better safe than sorry
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance

        # Compute distance to the ghost so that we can consider if the ghost is chasing our pacman
        distancesToGhosts = []
        # Get all opponent ghosts's positions
        for oppoIndex in self.getOpponents(successor):
            oppo = successor.getAgentState(oppoIndex)
            if not oppo.isPacman and oppo.getPosition() is not None:
                distancesToGhosts.append(self.getMazeDistance(myPos, oppo.getPosition()))

        if len(distancesToGhosts) > 0:
            minDisToGhost = min(distancesToGhosts)
            if minDisToGhost < GHOST_SAFE_DISTANCE:
                features['distanceToGhost'] = minDisToGhost + features['successorScore']
            else:
                features['distanceToGhost'] = 0

        return features

    def getWeights(self, gameState, action):

        if self.shouldAttack:
            if self.shouldGoBack == 0:
                return {'forcedOffensive': WEIGHT_SHOULD_ATTACK,
                        'successorScore': WEIGHT_SCORE,
                        'distanceToFood': WEIGHT_FOOD,
                        'distancesToGhost': WEIGHT_NORMAL_GHOST}
            else:
                return {'forcedOffensive': WEIGHT_SHOULD_GO_BACK,
                        'successorScore': WEIGHT_SCORE,
                        'distanceToFood': WEIGHT_FOOD,
                        'distancesToGhost': WEIGHT_NORMAL_GHOST}

        successor = self.getSuccessor(gameState, action)  # get the successor
        myPos = successor.getAgentState(self.index).getPosition()  # get the successor pos

        # Compute distance to the ghost so that we can consider if the ghost is chasing our pacman
        minDistance = 10000000
        scaredGhost = []
        ghostScared = False
        # Get all opponent ghosts's positions
        for oppoIndex in self.getOpponents(successor):
            oppo = successor.getAgentState(oppoIndex)

            if not oppo.isPacman and oppo.getPosition() is not None:
                dist = self.getMazeDistance(myPos, oppo.getPosition())
                if dist < minDistance:
                    minDistance = dist
                    scaredGhost.append(oppo)

        if len(scaredGhost) > 0:
            if scaredGhost[-1].scaredTimer > 0:
                ghostScared = True

        if ghostScared:
            weightGhost = WEIGHT_SCARED_GHOST
        else:
            weightGhost = WEIGHT_NORMAL_GHOST

        return {'forcedOffensive': WEIGHT_SHOULD_GO_BACK,
                'successorScore': WEIGHT_SCORE,
                'distanceToFood': WEIGHT_FOOD,
                'distancesToGhost': weightGhost}

    def preferrableAction(self, simulatedState):
        actions = simulatedState.getLegalActions(self.index)
        actions.remove(Directions.STOP)
        if len(actions) == 1:
            return actions[0]
        else:
            reversedDir = Directions.REVERSE[simulatedState.getAgentState(self.index).configuration.direction]
            if reversedDir in actions:
                actions.remove(reversedDir)
            return random.choice(actions)

    def monteCarlo(self, gameState, rounds):
        simulatedState = gameState.deepCopy()
        while rounds > 0:
            simulatedAction = self.preferrableAction(simulatedState)
            simulatedState = simulatedState.generateSuccessor(self.index, simulatedAction)
            rounds = rounds - 1
        return self.evaluate(simulatedState, Directions.STOP)

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
