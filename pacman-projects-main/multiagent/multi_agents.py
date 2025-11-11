# multi_agents.py
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


from util import manhattan_distance
from game import Directions, Actions
from pacman import GhostRules
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


    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        Just like in the previous project, get_action takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legal_moves = game_state.get_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = random.choice(best_indices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (new_food) and Pacman position after moving (new_pos).
        new_scared_times holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successor_game_state = current_game_state.generate_pacman_successor(action)
        new_pos = successor_game_state.get_pacman_position()
        new_food = successor_game_state.get_food()
        new_ghost_states = successor_game_state.get_ghost_states()
        new_scared_times = [ghostState.scared_timer for ghostState in new_ghost_states]
        
        "YOUR CODE HERE"
        score = successor_game_state.get_score()    #Agafem el score actual
        if(action == Directions.STOP):              #Penalitzem que es quedi parat
            score -= 1000
        food_list = new_food.as_list()              #Obtenim la llista de menjars
        dist_min = 10000
        for food in food_list:                      #Calcula la distància al menjar més proper
            value = manhattan_distance(food, new_pos)
            if (dist_min>value):
                dist_min = value
        if (dist_min==10000):                       #Aquest if s'utilitza per fer que el Pac-man es mengi l'últim coco
            dist_min = 0
        score -= dist_min                           #Es penalitza el moviment que deixi al Pac man a més distància del coco més proper
        for ghost in new_ghost_states:              #Calculem distància als fantasmes
            ghost_pos = ghost.get_position()
            dist = manhattan_distance(new_pos, ghost_pos)
            if (ghost.scared_timer>0):              #Si els fantasmes estàn espantats el Pacman s'apropa
                score -= dist
            else:                                   #D'altra manera s'allunya
                if (dist <= 1):
                    return -10000
                score += dist

        return score

def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.get_score()

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

    def __init__(self, eval_fn='score_evaluation_function', depth='2'):
        super().__init__()
        self.index = 0 # Pacman is always agent index 0
        self.evaluation_function = util.lookup(eval_fn, globals())
        self.depth = int(depth) 

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def minimax(self, agent, game_state, depth):
        if game_state.is_win() or game_state.is_lose() or depth == self.depth:  #Cas base. Retorna el score actual
            return self.evaluation_function(game_state)
        actions = game_state.get_legal_actions(agent)
        nextAgent = agent + 1
        nextDepth = depth
        if nextAgent == game_state.get_num_agents():                #Per reiniciar el nombre d'agent que serà el següent a analitzar-se
            nextAgent = 0
            nextDepth = depth + 1
        maxScore = float("-inf")
        minScore = float("inf")
        for action in actions: #Apliquem l'algoritme minimax amb cada acció possible
            successor = game_state.generate_successor(agent, action)
            score = self.minimax(nextAgent, successor, nextDepth)
            maxScore = max(score, maxScore)
            minScore = min(score, minScore)
        if (agent==0): #Si l'agent és el Pacman retorna el maxScore perquè és el nostre node amb valor max
            return maxScore
        else: #Si és fantasma retorna el minScore
            return minScore

    def get_action(self, game_state):
        """
        Returns the minimax action from the current game_state using self.depth
        and self.evaluation_function.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
        Returns a list of legal actions for an agent
        agent_index=0 means Pacman, ghosts are >= 1

        game_state.generate_successor(agent_index, action):
        Returns the successor game state after an agent takes an action

        game_state.get_num_agents():
        Returns the total number of agents in the game

        game_state.is_win():
        Returns whether or not the game state is a winning state

        game_state.is_lose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        actions = game_state.get_legal_actions(0)
        maxScore = float("-inf")
        for action in actions: #Apliquem el minimax de manera que obtenim l'acció amb millor puntuació
            new_game_state = game_state.generate_successor(0, action)
            score = self.minimax(1, new_game_state, 0) #Analitzem directament els fantasmes ja que farem un minimax que ens retornarà la score per cada moviment possible del Pacman
            if score > maxScore:
                maxScore = score
                bestAction = action
        return bestAction
        



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def max_value(self, game_state, alpha, beta, depth):
        if game_state.is_win() or game_state.is_lose() or depth == self.depth: #Cas base
            return self.evaluation_function(game_state)
        actions = game_state.get_legal_actions(0)
        nextAgent = 1
        nextDepth = depth
        if nextAgent == game_state.get_num_agents(): #El mateix que al minimax
            nextAgent = 0
            nextDepth = depth + 1
        v=float("-inf")
        for action in actions:
            successor = game_state.generate_successor(0, action)
            if (nextAgent == 0): #Si l'agent següent és el pacman fem el max_value i si és un fantasma el min_value
                score = self.max_value(successor, alpha, beta, nextDepth)
            else:
                score = self.min_value(successor, alpha, beta, nextAgent, nextDepth)
            v = max(v,score) #Actualitzem v amb el max
            if v > beta: #Fem el beta cut si v>beta
                return v
            alpha = max(alpha, v) #Actualitzem alpha
        return v

    def min_value(self, game_state, alpha, beta, agent, depth):
        if game_state.is_win() or game_state.is_lose() or depth == self.depth:
            return self.evaluation_function(game_state)
        actions = game_state.get_legal_actions(agent)
        nextAgent = agent + 1
        nextDepth = depth
        if nextAgent == game_state.get_num_agents():
            nextAgent = 0
            nextDepth = depth + 1
        v=float("inf")
        for action in actions:
            successor = game_state.generate_successor(agent, action)
            if (nextAgent == 0):
                score = self.max_value(successor, alpha, beta, nextDepth)
            else:
                score = self.min_value(successor, alpha, beta, nextAgent, nextDepth)
            v = min(v,score)
            if v < alpha:
                return v
            beta = min(beta, v)
        return v

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluation_function
        """
        "*** YOUR CODE HERE ***"
        actions = game_state.get_legal_actions(0)
        v = float("-inf")
        alpha = float("-inf") #Definim alpha i beta
        beta = float("inf")
        for action in actions:
            new_game_state = game_state.generate_successor(0, action)
            if(game_state.get_num_agents() > 1): 
                score = self.min_value(new_game_state, alpha, beta, 1, 0)
            else: #Cas en que no hi ha fantasmes
                score = self.max_value(new_game_state, alpha, beta, 1)
            if score > v:
                v = score
                bestAction = action
            if v > beta: #beta cut
                break
            alpha = max(alpha, v)
        return bestAction #Retornem la millor acció


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluation_function

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raise_not_defined()

def better_evaluation_function(current_game_state):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raise_not_defined()
    


# Abbreviation
better = better_evaluation_function
