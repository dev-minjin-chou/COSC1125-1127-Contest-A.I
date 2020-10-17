from captureAgents import CaptureAgent
import random
import util
from game import Directions
from util import nearestPoint


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
    return [eval(first)(firstIndex), eval(second)(secondIndex)]


##########
# Agents #
##########

# Define global constants for representing the weights of features
# Feature weights
WEIGHT_SCORE = 200
WEIGHT_FOOD = -5
WEIGHT_PANIC_GHOST = 0
WEIGHT_REGULAR_GHOST = 210
WEIGHT_SHOULD_ATTACK = 3000
WEIGHT_SHOULD_GO_BACK = 0
# Flags for offensive agent
TRUE = 1
FALSE = 0
ENFORCE_OFFENSE = 20
GHOST_SAFE_DISTANCE = 5
SHOULD_AVOID_UNMOVABLE = 1
MIN_COLLECTED_FOODS = 5
# Flags for defensive agent
REMAINING_FOODS = 4
SHOULD_DEFEND_COUNTER = 4


class ReflexCaptureAgent(CaptureAgent):

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


class OffensiveReflexAgent(ReflexCaptureAgent):
    """
    A reflex agent that seeks food. This is an agent
    we give you to get an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """

    def __init__(self, index):
        CaptureAgent.__init__(self, index)
        self.startingPosition = (0, 0)

        self.currentFoodSize = 10000000
        self.lastPostions = {}
        self.myPos = (-5, -5)
        self.counter = 0
        self.shouldAttack = False
        self.prevFoodList = []
        self.foodList = []
        self.shouldGoBack = 0
        self.homeTarget = None
        self.unmoveableList = []
        self.shouldComputeMonteCarlo = False
        self.modeTarget = None
        self.rapidConsumeQuota = 0
        self.firstGoal = []
        self.basicOperation = False
        self.amountOfCapsules = 0
        self.lastAmountCapsules = 0

    def registerInitialState(self, gameState):
        CaptureAgent.registerInitialState(self, gameState)
        self.distancer.getMazeDistances()
        self.startingPosition = gameState.getAgentState(self.index).getPosition()
        self.setInitialObjective(gameState)

    def chooseAction(self, gameState):
        self.myPos = gameState.getAgentState(self.index).getPosition()

        if self.myPos == self.startingPosition:
            self.basicOperation = True

        if self.myPos == self.firstGoal[0]:
            self.basicOperation = False

        if self.basicOperation:
            actions = gameState.getLegalActions(self.index)
            actions.remove(Directions.STOP)
            foodDistances = []

            for act in actions:
                newState = gameState.generateSuccessor(self.index, act)
                currentPos = newState.getAgentPosition(self.index)
                foodDistances.append(self.getMazeDistance(currentPos, self.firstGoal[0]))

            best = min(foodDistances)
            bestActions = [a for a, v in zip(actions, foodDistances) if v == best]
            bestAction = random.choice(bestActions)
            return bestAction

        if not self.basicOperation:
            return self.getActionNotBasicOp(gameState)

    def getFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)  # get the successor
        myPos = successor.getAgentState(self.index).getPosition()  # get the successor pos
        foodList = self.getFood(successor).asList()  # get the foodlist
        features['successorScore'] = self.getScore(successor)  # set score feature

        # If current agent is a pacman
        if successor.getAgentState(self.index).isPacman:
            features['shouldOffense'] = TRUE
        else:
            features['shouldOffense'] = FALSE

        # Compute distance to the nearest food
        if len(foodList) > 0:  # This should always be True,  but better safe than sorry
            # myPos = successor.getAgentState(self.index).getPosition()
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
                return {'shouldOffense': WEIGHT_SHOULD_ATTACK,
                        'successorScore': WEIGHT_SCORE,
                        'distanceToFood': WEIGHT_FOOD,
                        'distancesToGhost': WEIGHT_REGULAR_GHOST}
            else:
                return {'shouldOffense': WEIGHT_SHOULD_GO_BACK,
                        'successorScore': WEIGHT_SCORE,
                        'distanceToFood': WEIGHT_FOOD,
                        'distancesToGhost': WEIGHT_REGULAR_GHOST}

        successor = self.getSuccessor(gameState, action)  # get the successor
        myPos = successor.getAgentState(self.index).getPosition()  # get the successor pos

        # Compute distance to the ghost so that we can consider if the ghost is chasing our pacman
        minDistance = float("inf")
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
            weightGhost = WEIGHT_PANIC_GHOST
        else:
            weightGhost = WEIGHT_REGULAR_GHOST

        return {'shouldOffense': WEIGHT_SHOULD_GO_BACK,
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

    def getActionNotBasicOp(self, gameState):
        self.foodList = self.getFood(gameState).asList()
        self.amountOfCapsules = len(self.getCapsules(gameState))

        if len(self.prevFoodList) > len(self.foodList):
            self.shouldGoBack = 1
        self.prevFoodList = self.foodList
        self.lastAmountCapsules = self.amountOfCapsules

        if not gameState.getAgentState(self.index).isPacman:
            self.shouldGoBack = 0

        self.shouldAttack = self.compelledToAttack(gameState)

        shortestDistance = float("inf")
        enemies = [gameState.getAgentState(oppo) for oppo in self.getOpponents(gameState)]
        for enemy in enemies:
            if not enemy.isPacman and enemy.getPosition() is not None and not enemy.scaredTimer > 0:
                dist = self.getMazeDistance(self.myPos, enemy.getPosition())
                if shortestDistance > dist:
                    shortestDistance = dist

        self.shouldAvoidStuck(gameState)

        if self.lastAmountCapsules > self.amountOfCapsules:
            self.shouldComputeMonteCarlo = True
            self.rapidConsumeQuota = 0
        if shortestDistance <= 5:
            self.shouldComputeMonteCarlo = False
        if len(self.prevFoodList) > len(self.foodList):
            self.shouldComputeMonteCarlo = False

        return self.getActionFromMonteCarlo(gameState, shortestDistance)

    def getActionFromMonteCarlo(self, gameState, shortestDistance):
        legalActions = gameState.getLegalActions(self.index)
        legalActions.remove(Directions.STOP)

        actions = []
        for act in legalActions:
            if self.refineActions(gameState, act, 6) and shortestDistance > 3:
                actions.append(act)
            elif self.refineDangerousActions(gameState, act, 9):
                actions.append(act)

        if self.shouldComputeMonteCarlo:
            if not gameState.getAgentState(self.index).isPacman:
                self.rapidConsumeQuota = 0

            modeMinDistance = float("inf")

            if len(self.foodList) < len(self.prevFoodList):
                self.rapidConsumeQuota += 1

            # If there's no food nearby or carrying foods >= MIN_COLLECTED_FOODS, go home (starting position)
            if len(self.foodList) == 0 or self.rapidConsumeQuota >= MIN_COLLECTED_FOODS:
                self.modeTarget = self.startingPosition
            else:
                for food in self.foodList:
                    distance = self.getMazeDistance(self.myPos, food)
                    if distance < modeMinDistance:
                        modeMinDistance = distance
                        self.modeTarget = food

            actions = gameState.getLegalActions(self.index)
            actions.remove(Directions.STOP)
            foodDistances = []

            for a in actions:
                currentPos = gameState.generateSuccessor(self.index, a).getAgentPosition(self.index)
                foodDistances.append(self.getMazeDistance(currentPos, self.modeTarget))

            best = min(foodDistances)
            bestActions = [a for a, v in zip(actions, foodDistances) if v == best]
            bestAction = random.choice(bestActions)
            return bestAction

        else:
            self.rapidConsumeQuota = 0
            monteCarloValues = []
            for a in actions:
                newState = gameState.generateSuccessor(self.index, a)
                value = 0
                for i in range(1, 24):
                    value += self.monteCarlo(newState, 12)
                monteCarloValues.append(value)

            maxMonteCarlo = max(monteCarloValues)
            bestActions = [a for a, v in zip(actions, monteCarloValues) if v == maxMonteCarlo]
            bestAction = random.choice(bestActions)
        return bestAction

    def monteCarlo(self, gameState, rounds):
        simulatedState = gameState.deepCopy()
        while rounds > 0:
            simulatedAction = self.preferrableAction(simulatedState)
            simulatedState = simulatedState.generateSuccessor(self.index, simulatedAction)
            rounds = rounds - 1
        return self.evaluate(simulatedState, Directions.STOP)

    def refineActions(self, gameState, action, rounds):
        if rounds == 0:
            return True

        currentState = gameState.generateSuccessor(self.index, action)
        currentScore = self.getScore(gameState)
        newScore = self.getScore(currentState)
        currentFoods = self.getFood(gameState).asList()
        newFoods = self.getFood(currentState).asList()
        if currentScore < newScore:
            return True

        actions = currentState.getLegalActions(self.index)
        actions.remove(Directions.STOP)
        currentDirection = currentState.getAgentState(self.index).configuration.direction
        reversedDirection = Directions.REVERSE[currentDirection]
        if reversedDirection in actions:
            if len(currentFoods) != len(newFoods):
                return True
            else:
                actions.remove(reversedDirection)

        if len(actions) == 0:
            return False

        for action in actions:
            if self.refineActions(currentState, action, rounds - 1):
                return True
        return False

    def refineDangerousActions(self, gameState, action, rounds):
        if rounds == 0:
            return True

        currentState = gameState.generateSuccessor(self.index, action)
        currentScore = self.getScore(gameState)
        newScore = self.getScore(currentState)
        if currentScore < newScore:
            return True

        actions = currentState.getLegalActions(self.index)
        actions.remove(Directions.STOP)
        currentDirection = currentState.getAgentState(self.index).configuration.direction
        reversedDirection = Directions.REVERSE[currentDirection]
        if reversedDirection in actions:
            actions.remove(reversedDirection)
        else:
            return True

        if len(actions) == 0:
            return False

        for action in actions:
            if self.refineDangerousActions(currentState, action, rounds - 1):
                return True
        return False

    def setInitialObjective(self, gameState):
        mapLayout = getMapLayout(gameState)
        self.firstGoal = []
        for i in range(1, mapLayout['height'] - 1):
            centerX = int(mapLayout['centerX'])
            if not gameState.hasWall(centerX, i):
                self.firstGoal.append((centerX, i))
        while len(self.firstGoal) > 2:
            del self.firstGoal[0]
            self.firstGoal = self.firstGoal[:-1]
        if len(self.firstGoal) == 2:
            self.firstGoal.remove(self.firstGoal[0])

    def compelledToAttack(self, gameState):
        remainingFoods = self.getFood(gameState).asList()

        if len(remainingFoods) != self.currentFoodSize:
            self.currentFoodSize = len(remainingFoods)
            self.counter = 0
        else:
            self.counter = self.counter + 1

        initialPosition = gameState.getInitialAgentPosition(self.index)
        currentPosition = gameState.getAgentState(self.index).getPosition()
        if initialPosition == currentPosition:
            self.counter = 0
        if self.counter <= ENFORCE_OFFENSE:
            return False
        else:
            return True

    def shouldAvoidStuck(self, gameState):
        total = 0
        self.myPos = gameState.getAgentState(self.index).getPosition()

        if len(self.unmoveableList) > 9:
            self.unmoveableList.pop(0)

        if 2 in self.lastPostions and 4 in self.lastPostions:
            if self.myPos == self.lastPostions[2] and self.myPos == self.lastPostions[4]:
                if self.lastPostions[1] == self.lastPostions[3]:
                    self.unmoveableList.append(1)
                else:
                    self.unmoveableList.append(1)
            else:
                self.unmoveableList.append(0)

            self.lastPostions[4] = self.lastPostions[3]
            self.lastPostions[3] = self.lastPostions[2]
            self.lastPostions[2] = self.lastPostions[1]
            self.lastPostions[1] = self.lastPostions[0]

            if len(self.unmoveableList) < 9:
                return False
            else:
                for i in range(len(self.unmoveableList)):
                    total += self.unmoveableList[i]
                if total > SHOULD_AVOID_UNMOVABLE:
                    self.shouldComputeMonteCarlo = True
                    return True
                else:
                    return False


class DefensiveReflexAgent(ReflexCaptureAgent):
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

    def setPatrolArea(self, gameState):
        mapLayout = getMapLayout(gameState)

        for i in range(1, mapLayout['height'] - 1):
            centerX = int(mapLayout['centerX'])
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
