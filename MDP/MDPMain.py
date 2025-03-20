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
state_indexs = {state: idx for idx, state in enumerate(states)} # dictionary time (faster)

def run_fetcher(dfe, dfy, gamma): # our data frame of choice (30 by default)
    # to access a data frame at an intended position, use df.loc["key1", "key2"] (in row, column order)
    global states
    global state_indexs

    V = np.zeros(len(states)) # so that way we have the outcome of every possible policy
    converged = False
    while not converged: # make sure that you force transition if you can!!
        converged = True
        for state in states:
            health, age = state
            state_index = state_indexs[state]
            if health == "Dead":
                V[state_index] = -100 # fixed reward here. will it help? no clue.
                continue # nothing to calcualte here.

            if age == 120:
                next_age = 120
            else:
                next_age = age + 1

            reward = reward_function(state)
            state_index = state_indexs[state]
            old_value = V[state_index]

            future_values = []
            for action in actions:
                if action == "surgery":
                    df = dfy
                else:
                    df = dfe
                action_future_values = []
                for new_health in states_1:
                    if new_health == "Dead":
                        new_state = ("Dead", age)
                    else:
                        new_state = (new_health, next_age) # force the transition



                    transition_prob = df.loc[health, new_health]
                    #print("and here is the transition prob ", transition_prob)
                    new_state_index = state_indexs[new_state]
                    future_value = transition_prob * (reward + gamma * V[new_state_index])
                    #print("here is the expected future value ", future_value)
                    action_future_values.append(future_value)

                future_values.append(np.sum(action_future_values))

            new_value = max(future_values)
            V[state_index] = new_value

            # check for convergence
            if abs(new_value - old_value) > epsilon:
                print("This is how close we were ", new_value - old_value)
                converged = False


    print(V)
    save_values_to_cvs(V)

def reward_function(state):
    health = state[0]
    age = state[1]
    if health == "no AAA":
        return 100 - age
    elif health == "Dead":
        return -100
    else:
        return 0.9 * (100 - age)

def save_values_to_cvs(V, filename="VFor65"):
    df = pd.DataFrame({
        "Health" : [state[0] for state in states],
        "Age" : [state[1] for state in states],
        "Value" : V
    })
    df.to_csv(filename, index=False)



if __name__ == '__main__':
    df30e = pd.read_csv("60-65 - surveilence.csv", index_col=0)
    df30y = pd.read_csv("60-65 - surgery.csv", index_col=0)
    gamma = gamma1
    #gamma = gamma2
    run_fetcher(df30e, df30y, gamma)