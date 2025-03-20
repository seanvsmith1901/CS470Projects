import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches  # Import for custom legend

def display_plot():
    df = pd.read_csv("VFor35.0.7.csv")
    # pivot to make it easier for heatmaps, also drop the dead column.
    df_policy = df[(df["Health"] != "Dead") & (df["Health"] != "no AAA")].pivot(index="Age", columns="Health", values="Best Action")

    policy_colors = {"surgery" : 1, "surveillance" : 0}
    df_numeric = df_policy.replace(policy_colors)
    custom_map = ListedColormap(["blue", "red"])

    # Create the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(df_numeric, cmap=custom_map, linewidths=0.5, cbar=False)

    plt.title("optimal policy heatmap")
    plt.xlabel("Aneurysm Size")
    plt.ylabel("Age")

    save_path = r"C:\Users\Sean\Documents\GitHub\CS470Projectrs\MDP\heatmap.png"

    plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()

if __name__ == '__main__':
    display_plot()