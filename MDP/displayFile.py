import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches  # Import for custom legend

def display_plot():
    possible_dfs = ["Vfor60.0.9.csv", "Vfor60.0.7.csv", "Vfor30.0.9.csv", "Vfor30.0.7.csv"]
    for df_file in possible_dfs:
        df = pd.read_csv(df_file)

        # pivot to make it easier for heatmaps, also drop the dead column.
        df_policy = df[(df["Health"] != "Dead") & (df["Health"] != "no AAA")].pivot(index="Age", columns="Health", values="Best Action")

        policy_colors = {"surgery" : 0, "surveillance" : 1}
        df_numeric = df_policy.replace(policy_colors)
        print(df_numeric)
        custom_map = ListedColormap(["blue", "red"])

        # Create the heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(df_numeric, cmap=custom_map, linewidths=0.5, cbar=False, vmin=0, vmax=1)

        surgery_patch = mpatches.Patch(color='blue', label='Surgery')
        surveillance_patch = mpatches.Patch(color='red', label='Surveillance')
        plt.legend(handles=[surgery_patch, surveillance_patch])

        plt.title("optimal policy heatmap")
        plt.xlabel("Aneurysm Size")
        plt.ylabel("Age")

        base_name = os.path.splitext(df_file)[0]
        save_path = fr"C:\Users\Sean\Documents\GitHub\CS470Projectrs\MDP\heatmap_{base_name}.png"

        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        plt.show()

if __name__ == '__main__':
    display_plot()