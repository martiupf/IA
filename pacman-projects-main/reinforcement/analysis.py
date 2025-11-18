# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    # The reward of reaching the goal state (+10) is so little compared to
    # the reward of negative terminal states (-100). Therefore, the risk of ending
    # up in a negative state must be very low for crossing the bridge to be 
    # worth it. This is obtained by lowering the noise value and ensuring that the agent
    # always takes the desired action (left or right).
    answer_discount = 0.9
    answer_noise = 0 #Cambiem el noise a 0 perquè no hi hagi possibilitats de caure en un terminal state negatiu per mala sort.
    return answer_discount, answer_noise

def question3a():
    answer_discount = 0.3 #Valor baix per buscar la recompensa més propera (+1)
    answer_noise = 0 #Valor 0 perquè no hi hagi probabilitats de caure en el cliff
    answer_living_reward = 0 #0 perquè no influeixi el nombre de moviments per arribar a un terminal state
    return answer_discount, answer_noise, answer_living_reward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    answer_discount = 0.3 #Valor baix per buscar la recompensa més propera (+1)
    answer_noise = 0.2 #Valor alt de noise per tal que la IA prefereixi anar per la part de dalt per no jugarse-la anant a prop de la cliff 
    answer_living_reward = 0 #0 perquè no influeixi el nombre de moviments per arribar a un terminal state
    return answer_discount, answer_noise, answer_living_reward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    answer_discount = 0.9 #Valor elevat perquè busqui la recompensa més alta a llarg termini (+10)
    answer_noise = 0 #Valor 0 perquè no hi hagi probabilitats de caure en el cliff
    answer_living_reward = 0 #0 perquè no influeixi el nombre de moviments per arribar a un terminal state
    return answer_discount, answer_noise, answer_living_reward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    answer_discount = 0.9 #Valor elevat perquè busqui la recompensa més alta a llarg termini (+10)
    answer_noise = 0.2 #Valor alt de noise per tal que la IA prefereixi anar per la part de dalt per no jugarse-la anant a prop de la cliff
    answer_living_reward = 0 #0 perquè no influeixi el nombre de moviments per arribar a un terminal state
    return answer_discount, answer_noise, answer_living_reward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    answer_discount = 1
    answer_noise = 0
    answer_living_reward = 1 #Perquè la recompensa de no arribar a un terminal state sigui més gran que acabar el joc
    return answer_discount, answer_noise, answer_living_reward
    # If not possible, return 'NOT POSSIBLE'

def question6():
    return 'NOT POSSIBLE'

def question8():
    answer_epsilon = None
    answer_learning_rate = None
    return answer_epsilon, answer_learning_rate
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
