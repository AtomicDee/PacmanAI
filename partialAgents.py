# partialAgent.py
# parsons/15-oct-2017
#
# Version 1
#
# The starting point for CW1.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
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

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
from game import Actions
import api
import random
import game
import util

class PartialAgent(Agent):

    # Initialise variables
    def __init__(self):
        self.lastmove = Directions.STOP
        self.lastloc = (0,0)
        self.current_food_loc = (0,0)

        self.food = set()
        self.food_eaten = False

    # Reset food set every game
    def final(self, state):
        self.food = set()
        self.food_eaten = False
        #print "Game Over!"

    def getAction(self, state):
        # Load legal moves, remove 'STOP' from legal move options
        legal = api.legalActions(state)
        if Directions.STOP in legal:
           legal.remove(Directions.STOP)

        # Save pacman and ghost locations
        pacman = api.whereAmI(state)
        theGhosts = api.ghosts(state)

        # Concatenate any newly discovered food into the food set
        self.food = self.food | set(api.food(state)) | set(api.capsules(state))

        # The following bloc runs for each direction in legal
        for l in legal :
            # Create a vector of the current direction
            vec = Actions.directionToVector(l)
            # Find coordinates of the next space if this vector is followed
            loc = (pacman[0] + int(vec[0]), pacman[1] + int(vec[1]))
            loc2 = (pacman[0] + 2*int(vec[0]), pacman[1] + 2*int(vec[1]))

            # Check if the next space has a ghost
            if loc in theGhosts :
                # remove this direction from legal options to avoid ghost
                legal.remove(l)
            # Check two spaces ahead for ghosts
            elif loc2 in theGhosts :
                legal.remove(l)

            # Check if the next space contains food
            elif loc in self.food :
                # Remove this food location from the set, as it has been eaten
                self.food.remove(loc)
                self.food_eaten = True
                # Move pacman to eat the food
                #print 'return food eat'
                return api.makeMove(l, legal)

        # Runs only when food has been eaten
        if self.food_eaten is True :
            # Reset eating boolean
            self.food_eaten = False
            # Reset distance to next food
            dist = float('Inf')
            # Find the next closest piece of food in the self.food set
            for f in self.food :
                if util.manhattanDistance(pacman, f) < dist:
                    dist  = util.manhattanDistance(pacman, f)
                    # update the current target food location
                    self.current_food_loc = f

        # If food has not been found or eaten in the next step, run this bloc
        else :
            for l in legal :
                # Create a vector of the current direction
                vec = Actions.directionToVector(l)
                # Find coordinates of the next space
                loc = (pacman[0] + int(vec[0]), pacman[1] + int(vec[1]))

                # Calculate whether the next space is closer to the target than
                # pacman's current location
                next_dist_to_target = util.manhattanDistance(self.current_food_loc, loc)
                dist_to_target = util.manhattanDistance(self.current_food_loc, pacman)

                # If the next space is closer to the target, move pacman there
                if next_dist_to_target < dist_to_target :
                    #print 'return distant food'
                    return api.makeMove(l, legal)

        # Clause to catch the case where all legal options have been removed,
        # pacman stops for one step, preventing the program from throwing an
        # error of legal being empty.
        if not legal :
            legal.append(Directions.STOP)

        # if none of the conditions are fulfilled, pacman makes a random move
        #print 'return random'
        return api.makeMove(random.choice(legal), legal)

class GoWestAgent(Agent) :

    def getAction(self, state) :
        legal = api.legalActions(state)
        
        if Directions.WEST in legal :
            return api.makeMove(Directions.WEST, legal)
        else :
            return api.makeMove(random.choice(legal), legal)
