# literally no clue what to pu there.
import pandas as pd
import numpy as np

states_1 = ["Dead", "no AAA", "<30 mm", "30-35 mm", "35-40 mm", "40-45 mm", "45-50 mm", "50-55 mm", "55-60 mm", "60-65 mm", "65-70 mm", "70-75 mm",  "75-80 mm", "> 80 mm"]

states_30 = [30, 31, 32, 33, 34, 35]
states_60 = [60, 61, 62, 63, 64, 65]

actions = ["surgery", "surveillance"]

epsilon = 1e-6 # not put in the spec, but seems necessary for convergence. at least in the examples I am looking at.

def run_fetcher(age, gamma): # our data frame of choice (30 by default)
    if age == 30:
        dfe = pd.read_csv("30-35 - survelliance.csv", index_col=0)
        dfy = pd.read_csv("30-35 - surgery.csv", index_col=0)
        states_2 = states_30
    elif age == 60:
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
        for state in states:
            health, age = state
            state_index = state_indexes[state]
            if health == "Dead":
                V[state_index] = -100 # fixed reward here. will it help? no clue.
                continue # nothing to calcualte here.

            if age == 35:
                next_age = 35
            elif age == 65:
                next_age = 65
            else:
                next_age = age + 1

            reward = reward_function(state)
            old_value = V[state_index]

            action_values = []

            for action in actions:
                action_value = []
                if action == "surgery":
                    df = dfy
                else:
                    df = dfe
                for new_health in states_1:
                    if new_health == "Dead":
                        new_state = ("Dead", age)
                    else:
                        next_health = next_anuyerisn_size(health)
                        if (new_health == health or new_health == next_health):
                            new_state = (new_health, next_age)
                        else:
                            continue


                    transition_prob = df.loc[health, new_health]
                    if transition_prob > 0:
                        #print(f"State: {state}, Action: {action}, Transition to {new_state} with prob {transition_prob}")

                        new_state_index = state_indexes[new_state]
                        future_value = transition_prob * (reward + gamma * V[new_state_index])
                        action_value.append(future_value)

                if action_value:
                    best_action_value = max(action_value)
                    action_values.append(best_action_value)
                else:
                    action_values.append(float("-inf"))

            best_value = max(action_values)
            best_action = actions[action_values.index(best_value)]

            #print(f"State: {state}, Surgery Value: {action_values[0]}, Surveillance Value: {action_values[1]}")

            V[state_index] = best_value
            policy[state] = best_action

            # check for convergence
            if abs(best_value - old_value) > epsilon:
                converged = False # this breaks


    print(V)
    save_values_to_cvs(V, policy, states, age, gamma)

def reward_function(state):
    health = state[0]
    age = state[1]
    if health == "no AAA":
        return 100 - age
    elif health == "Dead":
        return -100
    else:
        return 0.9 * (100 - age)


def next_anuyerisn_size(current_health):
    transitions = { # allows for growth to grow by one stage, tops.
        "no AAA": ["no AAA", "<30 mm"],
        "<30 mm": ["<30 mm", "30-35 mm"],
        "30-35 mm": ["30-35 mm", "35-40 mm"],
        "35-40 mm": ["35-40 mm", "40-45 mm"],
        "40-45 mm": ["40-45 mm", "45-50 mm"],
        "45-50 mm": ["45-50 mm", "50-55 mm"],
        "50-55 mm": ["50-55 mm", "55-60 mm"],
        "55-60 mm": ["55-60 mm", "60-65 mm"],
        "60-65 mm": ["60-65 mm", "65-70 mm"],
        "65-70 mm": ["65-70 mm", "70-75 mm"],
        "70-75 mm": ["70-75 mm", "75-80 mm"],
        "75-80 mm": ["75-80 mm", "> 80 mm"],
        "> 80 mm": ["> 80 mm", "> 80 mm"],  # we can't grow any higher
    }
    if current_health in transitions:
        return transitions[current_health][1]
    else:
        return current_health

def save_values_to_cvs(V, policy, states, age, gamma):
    filename = "Vfor" + str(age) + "." + str(gamma) + ".csv"
    df = pd.DataFrame({
        "Health" : [state[0] for state in states],
        "Age" : [state[1] for state in states],
        "Value" : V,
        "Best Action" : [policy.get(state, None) for state in states]
    })
    df.to_csv(filename, index=False)



if __name__ == '__main__':
    ages = [30]#, 60]
    gammas = [0.9]#, 0.7]
    for age in ages:
        for gamma in gammas:
            run_fetcher(age, gamma)
