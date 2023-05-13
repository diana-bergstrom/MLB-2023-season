# import packages and confirgure libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import seaborn as sns

# uploaded a dataset via csv directly to a kaggle notebook
my_data = pd.read_csv('/kaggle/input/mlbstandings-updated/mlbstandings_2023_updated.csv')

# add a column to set up path for team logo images
my_data['path'] = '/kaggle/input/mlbteamlogos/' + my_data['Tm'] + '.png'
my_data = my_data.drop(my_data[my_data['Tm'] == 'Average'].index)

# create two new columns for the separated values
my_data[['above_500_wins', 'above_500_loss']] = my_data['≥.500'].str.split('-', expand=True)
my_data[['below_500_wins', 'below_500_loss']] = my_data['<.500'].str.split('-', expand=True)

# convert data types to float
my_data[['above_500_wins','above_500_loss']] = my_data[['above_500_wins','above_500_loss']].astype(float)
my_data[['below_500_wins','below_500_loss']] = my_data[['below_500_wins','below_500_loss']].astype(float)

# calculate win% for each team against teams above and below .500
# convert data types to float
my_data['win%_above_500'] = my_data['above_500_wins'] / (my_data['above_500_wins'] + my_data['above_500_loss'])
my_data['win%_above_500'] = my_data['win%_above_500'].astype(float)

my_data['win%_below_500'] = my_data['below_500_wins'] / (my_data['below_500_wins'] + my_data['below_500_loss'])
my_data['win%_below_500'] = my_data['win%_below_500'].astype(float)

# drop columns with W-L records
my_data = my_data.drop(columns=['≥.500', '<.500'])

# convert team column to string data type
my_data['Tm'] = my_data['Tm'].astype(str)

# create plot
fig, ax = plt.subplots(figsize=(20, 20))
sns.set(font_scale = 2)
sns.scatterplot(x=my_data['win%_below_500'],
                y=my_data['win%_above_500'],
                ax=ax)

# figure title
ax.set_title('Win% against >=.500 teams vs. <.500 teams',size=34)

# axes titles
ax.set_xlabel('win% against teams <.500', size=27)
ax.set_ylabel('win% against teams  >=.500',size=27)

# add vertical line for x-axis average
ax.axvline(x=my_data['win%_below_500'].mean(), color='gray', linestyle='--')

# add horizontal line for y-axis average
ax.axhline(y=my_data['win%_above_500'].mean(), color='gray', linestyle='--')

# add annotations to each quadrant
ax.annotate('below average vs. everyone', xy=(0.2, 0.17), xytext=(0.2, 0.17),
            fontsize=16, color='red', alpha=1)

ax.annotate('above average vs. bad teams\nbelow average vs. good teams', xy=(0.75, 0.17), xytext=(0.75, 0.17),
            fontsize=16, color='orange', alpha=1)

ax.annotate('above average vs. good teams\nbelow average vs. bad teams', xy=(0.2, 0.655), xytext=(0.2, 0.655),
            fontsize=16, color='orange', alpha=1)

ax.annotate('above average vs. everyone', xy=(0.765, 0.664), xytext=(0.765, 0.664),
            fontsize=16, color='green', alpha=1)

# add a solid black border
for spine in ax.spines.values():
    spine.set_edgecolor('black')
    spine.set_linewidth(2)

# set the facecolor to white
ax.set_facecolor('white')

# turn on gridlines
ax.grid(True)

# set the color of the gridlines
ax.grid(color='gray', linestyle='--', linewidth=1, alpha=0.5)

# plot team logo images
def getImage(path):
    return OffsetImage(plt.imread(path), zoom=0.2)

for index, row in my_data.iterrows():
    ab = AnnotationBbox(getImage(row['path']), (row['win%_below_500'], row['win%_above_500']), frameon=False)
    ax.add_artist(ab)
    
# save image of figure
plt.savefig('MLB Win% vs Teams Above and Below Average Records')
