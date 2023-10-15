# import packages and configure libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# upload dataset via csv directly to kaggle notebook
IL = pd.read_csv('/kaggle/input/mlb-injury-report-2023/InjuryReport_2023.csv')

# check that there are a total of 30 teams
total_teams = IL['Team'].nunique()
print(total_teams)
# result is 30

# create new column playoffs
# if Team = TOR, MIN, TEX, TBR, ARI, MIL, MIA, PHI, HOU, BAL, LAD, ATL then playoffs = yes
# all other teams playoffs = no
# list of teams that are in the playoffs
playoff_teams = ['TOR', 'MIN', 'TEX', 'TBR', 'ARI', 'MIL', 'MIA', 'PHI', 'HOU', 'BAL', 'LAD', 'ATL']

# create a new 'playoffs' column based on the conditions
# use lambda function to take each team name one by one and check if it exists in the playoff teams list using the in operator
IL['playoffs'] = IL['Team'].apply(lambda team: 'Yes' if team in playoff_teams else 'No')

# group the data by 'Team' and count the IL stints for each team, then sort in ascending order
sorted_IL = IL.groupby('Team')['ID'].count().reset_index().sort_values(by='ID', ascending=True)

# create a custom color palette based on the 'Playoff_Status' column
palette = {team: 'orange' if status == 'Yes' else 'blue' for team, status in zip(IL['Team'], IL['playoffs'])}

# define a custom color palette for x-axis labels
label_colors = {
    'Yes': 'red',   # Red for playoff teams
    'No': 'black'   # Black for non-playoff teams
}

# set figure size and background type
sns.set(style="white")
plt.figure(figsize=(14, 6))

# use sns.barplot to display the counts with the custom color palette
ax = sns.barplot(data=sorted_IL, x='Team', y='ID', palette=palette)

# set labels and title
plt.xlabel('')
plt.ylabel('')
plt.title('IL Stint Count for MLB Teams in 2023')

# rotate x-axis labels for better readability
plt.xticks(rotation=90)

# Remove y-axis tick marks
ax.set_yticks([])

# customize x-axis label colors based on the defined palette
for label in ax.get_xticklabels():
    team_name = label.get_text()
    playoffs_status = IL.loc[IL['Team'] == team_name, 'playoffs'].iloc[0]
    label.set_color(label_colors.get(playoffs_status, 'black'))
    
# create a legend
legend_labels = ['Playoff Teams', 'Non-Playoff Teams']
legend_colors = ['orange', 'blue']
legend_handles = [plt.Line2D([0], [0], marker='s', color='w', label=label, markersize=10, markerfacecolor=color) for label, color in zip(legend_labels, legend_colors)]
plt.legend(handles=legend_handles)

# set legend location and remove border
plt.legend(handles=legend_handles, loc='upper center', frameon=False)

# add the count above each bar and color according to playoff status
for index, row in enumerate(sorted_IL['ID']):
    playoff_status = IL.loc[IL['Team'] == sorted_IL['Team'].iloc[index], 'playoffs'].iloc[0]
    text_color = 'red' if playoff_status == 'Yes' else 'black'
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=10, color=text_color)

# save image
plt.savefig('Team Injury Count 2023.png')
