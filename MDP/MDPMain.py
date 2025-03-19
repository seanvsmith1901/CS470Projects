# literally no clue what to pu there.
import pandas as pd
import numpy as np

states_1 = ["Dead", "no AAA", "<30 mm", "30-35 mm", "35-40 mm", "40-45 mm", "45-50 mm", "50-55 mm", "55-60 mm", "60-65 mm", "65-70 mm", "70-75 mm",  "75-80 mm", "> 80 mm"]
states_2 = [65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120]
actions = ["surgery", "surveillance"]
gamma1 = 0.9
gamma2 = 0.7 # thats LOW.
epsilon = 1e-6 # not put in the spec, but seems necessary for convergence. at least in the examples I am looking at.
states = [(health, age) for health in states_1 for age in states_2] # creates cartesian product bc I am lazy
state_index = {state: idx for idx, state in enumerate(states)} # dictionary time (faster)

def run_fetcher(df, gamma): # our data frame of choice (30 by default)
    # to access a data frame at an intended position, use df.loc["key1", "key2"] (in row, column order)
    global states
    global state_index

    V = np.zeros(len(states)) # so that way we have the outcome of every possible policy
    converged = False
    while not converged:
        converged = True
        for state in states:
            health, age = state
            reward = reward_function(state)
            state_index = state_index[state]
            old_value = V[state_index]

            future_values = []
            for new_state in states:
                new_health, new_age = new_state
                transition_prob = df.loc[health, new_health]
                future_value = transition_prob * (reward + gamma * V[state_index[new_state]])
                future_values.append(future_value)

            new_value = max(future_values)
            V[state_index] = new_value

            if abs(new_value - old_value) > epsilon:
                converged = False

    print(V)

def reward_function(state):
    health = state[0]
    age = state[1]
    if health == "no_aneurysm":
        return 100 - age
    elif health == "death":
        return -100
    else:
        return 0.9 * (100 - age)


if __name__ == '__main__':
    df30 = pd.read_csv("60-65 - surveilence.csv")
    df60 = pd.read_csv("60-65 - surgery.csv")
    gamma = gamma1
    #gamma = gamma2
    run_fetcher(df30, gamma)