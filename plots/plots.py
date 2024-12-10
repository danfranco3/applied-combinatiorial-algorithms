import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

file_paths = {
    "1": "../first-assignment-5lig0/first-part/final_result.csv",
    "2": "../first-assignment-5lig0/second-part/final_result.csv",
    "3": "../first-assignment-5lig0/third-part/final_result.csv"
}

# First part

part1 = pd.read_csv(file_paths['1'])

part1_values = part1.loc[part1.comment.isin([f'{x}' for x in range (1, 6)])]

part1_easy = part1_values[:30]

part1_medium = part1_values[30:60]

part1_hard = part1_values[60:90]

part2 = pd.read_csv(file_paths['2'])

part2_values = part2.loc[part2.comment.isin([f'{x}' for x in range (1, 6)])]

part2_easy = part2_values[90:120]

part2_medium = part2_values[120:150]

part2_hard = part2_values[150:180]

part3 = pd.read_csv(file_paths['3'])

part3_values = part3.loc[part3.comment.isin([f'{x}' for x in range (1, 6)])]

part3_easy = part3_values[180:210]

part3_medium = part3_values[210:240]

part3_hard = part3_values[240:270]

l = [(part1_easy, 'Part 1 - Easy'), (part1_medium, 'Part 1 - Medium'), (part1_hard, 'Part 1 - Hard'), (part2_easy, 'Part 2 - Easy'), (part2_medium, 'Part 2 - Medium'), (part2_hard, 'Part 2 - Hard'), (part3_easy, 'Part 3 - Easy'), (part3_medium, 'Part 3 - Medium'), (part3_hard, 'Part 3 - Hard')]

for v, _name in l:

    if _name.__contains__('1') or _name.__contains__('3'):
        labels = range(4, 15, 2)
    else:
        labels = range(8, 19, 2)

    b = v['baseline makespan'].astype(float)
    m = v['your solution makespan'].astype(float)

    r = m/b

    data = [r[i:i + 5] for i in range(0, len(r), 5)]

    # Create a boxplot
    plt.figure(figsize=(4, 4))
    plt.boxplot(data, notch=False, patch_artist=True, showmeans=True,
                boxprops=dict(facecolor='lightcoral', color='black'),
                medianprops=dict(color='orange'),
                whiskerprops=dict(color='black'),
                capprops=dict(color='black'),
                meanprops=dict(marker='o', markerfacecolor='white', markeredgecolor='black'))

    # Add labels
    plt.title(f"{_name}")
    plt.xlabel("Mission length")
    plt.ylabel("Normalized Makespan")
    plt.xticks(labels=labels, ticks=range(1, 7))
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()