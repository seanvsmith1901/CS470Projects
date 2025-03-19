# literally no clue what to pu there.
import itertools # will create cartesian product for us
import pandas as pd


states_1 = ["death", "no_aneurysm", "<30", "30-35", "35-40", "40-45", "45-50", "50-55", "55-60", "60-65", "65-70", "70-75",  "75-80", ">80"]
states_2 = [65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120]
actions = ["surgery", "surveillance"]
gamma1 = 0.9
gamma2 = 0.7 # thats LOW.

def run_fetcher():
    states = cartesian_product(states_1, states_2)
    df30 = pd.read_csv("30-35 - Sheet1.csv")
    df60 = pd.read_csv("60-35 - Sheet1.csv")











def cartesian_product(arry1, arry2):
    return list(itertools.product(arry1, arry2))

if __name__ == '__main__':
    run_fetcher()