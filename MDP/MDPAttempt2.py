# literally no clue what to pu there.
import pandas as pd
import numpy as np
from past.types import oldstr

states_1 = ["Dead", "no AAA", "<30 mm", "30-35 mm", "35-40 mm", "40-45 mm", "45-50 mm", "50-55 mm", "55-60 mm", "60-65 mm", "65-70 mm", "70-75 mm",  "75-80 mm", "> 80 mm"]

states_30 = [30, 31, 32, 33, 34, 35]
states_60 = [60, 61, 62, 63, 64, 65]

actions = ["surgery", "surveillance"]

epsilon = 1e-6 # not put in the spec, but seems necessary for convergence. at least in the examples I am looking at.

def run_fetcher(passed_age, gamma): # our data frame of choice (30 by default)
    if passed_age == 30:
        dfe = pd.read_csv("30-35 - survelliance.csv", index_col=0)
        dfy = pd.read_csv("30-35 - surgery.csv", index_col=0)
        states_2 = states_30
    elif passed_age == 40:
        dfe = pd.read_csv("40-45 - survelliance.csv", index_col=0)
        dfy = pd.read_csv("40-45 - surgery.csv", index_col=0)
        states_2 = states_30
    elif passed_age == 60:
        dfe = pd.read_csv("60-65 - surveilence.csv", index_col=0)
        dfy = pd.read_csv("60-65 - surgery.csv", index_col=0)
        states_2 = states_60
    else:
        print("THAT WAS WRONG")
        return

    # to access a data frame at an intended position, use df.loc["key1", "key2"] (in row, column order)
    states = [(health, possible_age) for health in states_1 for possible_age in states_2]  # creates cartesian product bc I am lazy
    state_indexes = {state: idx for idx, state in enumerate(states)}  # dictionary time (faster)

    V = np.zeros(len(states)) # so that way we have the outcome of every possible policy
    policy = {}
    converged = False
    while not converged: # make sure that you force transition if you can!!
        converged = True
        # so first lets find the reward
        for state in states:

            best_value = float("-inf")
            best_action = None

            state_index = state_indexes[state]
            old_value = V[state_index]

            reward = reward_function(state)

            for action in actions: # now lets consider every possible action
                df = dfy if action == "surgery" else dfe # to get the transition probs

                action_value = 0 # we start out with 0, bc thats the possible action payoff rn.

                for new_state in transition_states(state): # for every possible state we could go through
                    new_state_index = state_indexes[new_state] # get the new index
                    transition_probability = df.loc[state[0], new_state[0]] # get the transition probability based on the action and state
                    new_value = reward + (gamma * (transition_probability * V[new_state_index])) # get the new value
                    action_value += new_value # sum it up so we can look into the future and see which is better

                if action_value > best_value: # if our current value is better than anything else we have calcualted
                    best_value = action_value # set the stuff appropriately
                    best_action = action

            V[state_index] = best_value # put our best foot forward.
            policy[state] = best_action

            # check for convergence
            if abs(best_value - old_value) > epsilon:
                converged = False  # this breaks


    print(V)
    save_values_to_cvs(V, policy, states, passed_age, gamma)

def transition_states(state): # returns all the possible states from our current state
    possible_healths = ["Dead", "no AAA", "Same_size", "Size + 1"]

    new_states = []
    health, age = state

    if age == 35:
        new_age = 35
    elif age == 65:
        new_age = 65
    else:
        new_age = age + 1
    next_health = next_aneurysm_size(health)

    for new_health in possible_healths: # creates all of the possible new states
        # Do I need to disallow double dipping? I think its fine, we just need to consider the chances of it happening
        if new_health == "Dead":
            new_states.append(("Dead", new_age))
        if new_health == "No AAA":
            new_states.append(("No AAA", new_age))
        if new_health == "Same_size":
            new_states.append((health, new_age))
        if new_health == "Size + 1":
            new_states.append((next_health, new_age))

    return new_states



def reward_function(state):
    health = state[0]
    age = state[1]
    if health == "no AAA":
        return 100 - age
    elif health == "Dead":
        return -100
    else:
        return 0.9 * (100 - age)


def next_aneurysm_size(current_health):
    transitions = { # allows for growth to grow by one stage, tops.
        "no AAA": "<30 mm",
        "<30 mm": "30-35 mm",
        "30-35 mm": "35-40 mm",
        "35-40 mm": "40-45 mm",
        "40-45 mm": "45-50 mm",
        "45-50 mm": "50-55 mm",
        "50-55 mm": "55-60 mm",
        "55-60 mm": "60-65 mm",
        "60-65 mm": "65-70 mm",
        "65-70 mm": "70-75 mm",
        "70-75 mm": "75-80 mm",
        "75-80 mm": "> 80 mm",
        "> 80 mm": "> 80 mm",  # we can't grow any higher
    }
    if current_health in transitions:
        return transitions[current_health]
    else:
        return current_health  # in case death or whatever.

def save_values_to_cvs(V, policy, states, age, gamma):
    print("this is the age", age)
    filename = "Vfor" + str(age) + "." + str(gamma) + ".csv"
    print("this is the fiule name we are trtying to rping ", filename)
    df = pd.DataFrame({
        "Health" : [state[0] for state in states],
        "Age" : [state[1] for state in states],
        "Value" : V,
        "Best Action" : [policy.get(state, None) for state in states]
    })
    df.to_csv(filename, index=False)



if __name__ == '__main__':
    ages = [40]#, 60]
    gammas = [0.9]#, 0.7]
    for age in ages:
        for gamma in gammas:
            run_fetcher(age, gamma)
