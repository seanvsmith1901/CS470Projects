# literally no clue what to pu there.
import pandas as pd
import numpy as np

states_1 = ["Dead", "no AAA", "<30 mm", "30-35 mm", "35-40 mm", "40-45 mm", "45-50 mm", "50-55 mm", "55-60 mm", "60-65 mm", "65-70 mm", "70-75 mm",  "75-80 mm", "> 80 mm"]

states_30 = [30, 31, 32, 33, 34, 35] # only considering the ages 30-35
states_60 = [60, 61, 62, 63, 64, 65] # only considering the ages 60-65

actions = ["surgery", "surveillance"] # the only possible actions in this space.

epsilon = 1e-6 # not put in the spec, but seems necessary for convergence. at least in the examples I am looking at.

def run_fetcher(passed_age, gamma): # our data frame of choice (which transition tables we use)
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
    policy = {} # keep track of what policies we use when

    converged = False
    while not converged: # make sure that you force transition if you can!!
        converged = True
        for state in states:
            health, age = state
            state_index = state_indexes[state] # we love dictionary lookups.
            if health == "Dead":
                V[state_index] = -100 # fixed reward here. will it help? no clue.
                # there is no policy here. Theere is nothing to do.
                continue # terminal state, don't expand.
            # geting rid of this makes it only ever recommend surgery.
            elif health == "no AAA": # this is wrong. tihs can expand.
                V[state_index] = reward_function(state)
                policy[state] = "surveillance"
                continue


            old_value = V[state_index] # need something to compare it to.

            best_value = float("-inf") # current best value from action
            best_action = None # current best action

            for action in actions: # have to try every action and go from there
                reward = reward_function(state, action)  # this is the reward where I am right now.

                future_value = 0 # expected value from that action
                if action == "surgery": # set up the transition tables
                    df = dfy
                else:
                    df = dfe

                new_states = transition_states(state, action) # get the new states given our action and our current state.
                for new_state in new_states: # go through every possible consequence
                    new_health, new_age = new_state
                    transition_prob = df.loc[health, new_health] # how likely we are to transition to a new state
                    # as far as I can tell its pulling the correct transition probabilities.
                    #print(f"Action: {action}, Current Health: {health}, Current Age: {age} New Health: {new_health}, Transition Prob: {transition_prob}")
                    if transition_prob > 0: # if its possible to occur
                        new_state_index = state_indexes[new_state] # find where the new state exists
                        future_value += transition_prob * V[new_state_index] # add the future value to it from all the new states

                future_action_value = reward + (gamma * future_value) # add the current reward, disctount the future rewared, consider

                if future_action_value > best_value: # if its a new best
                    best_value = future_action_value # let it stick around
                    best_action = action # keep track of best

            V[state_index] = best_value # after considering every action, find best vlauer we can get
            policy[state] = best_action # and keep track of the best action

            # check for convergence
            if abs(best_value - old_value) > epsilon:
                converged = False # this breaks


    print(V) # just for fun
    save_values_to_cvs(V, policy, states, passed_age, gamma) # helps me keep track of everything.

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

def get_new_age(state):
    _, age = state
    if age == 35:
        new_age = 35
    elif age == 65:
        new_age = 65
    else:
        new_age = age + 1
    return new_age

def transition_states(state, action): # returns all the possible states from our current state
    if action == "surveillance":
        possible_healths = ["Dead", "no AAA", "Same_size", "Size + 1", "Size + 2"]
    else:
        possible_healths = ["Dead", "no AAA"] # surgery either works or kills you. No other consideratino is made.

    new_states = []
    health, age = state

    if health == "Dead": # This never goes off, but just in case.
        return new_states

    if age == 35:
        new_age = 35
    elif age == 65:
        new_age = 65
    else:
        new_age = age + 1
    # new age never exceeds 35 or 65, so thats nice.
    next_health = next_aneurysm_size(health)
    next_next_health = next_aneurysm_size(next_health)

    for new_health in possible_healths: # creates all of the possible new states
        if new_health == "Dead":
            new_states.append(("Dead", new_age))
        if new_health == "no AAA":
            new_states.append(("no AAA", new_age))
        if new_health == "Same_size": # probability of staying
            new_states.append((health, new_age))
        if new_health == "Size + 1": # probability of moving on.
            new_states.append((next_health, new_age))
        if new_health == "Size + 2":  # probability of growing 2 sizes between visits.
            new_states.append((next_next_health, new_age))

    new_states = remove_duplicate_tuples(new_states) # exactly what it says on the tin. No double dipping!
    return new_states

def remove_duplicate_tuples(tuple_list):
    seen = set()
    new_list = []
    for tup in tuple_list:
        if tuple(tup) not in seen:
            new_list.append(tup)
            seen.add(tuple(tup))
    return new_list


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
    ages = [45]
    gammas = [0.9, 0.7]
    for age in ages:
        for gamma in gammas:
            run_fetcher(age, gamma)
