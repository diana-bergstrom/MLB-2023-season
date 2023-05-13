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

# create plot

fig, ax = plt.subplots(figsize=(20,20))
sns.set(font_scale = 2)
sns.scatterplot(x=my_data['SOS'],
                y=my_data['W-L%'],
                ax=ax)

# figure title
ax.set_title('Comparing Records and Strength of Schedules Amongst MLB Teams',size=34)

# axes titles
ax.set_xlabel('Strength of Schedule', size=27)
ax.set_ylabel('Win-Loss Percentage',size=27)

# create axes lines
ax.axvline(x=0, color='gray', alpha=0.2)
ax.axhline(y=0.5, color='gray', alpha=0.2)

# remove grid
ax.grid(False)

# use image logos on plot
# plt.imread function reads an image from the provided location
# zoom level reduces the image size
# alpha level makes images transparent in case they overlap
def getImage(path):
    return OffsetImage(plt.imread(path), zoom=.17, alpha = 1)

# add annotations
ax.annotate('losing team with easy schedule', xy=(-0.54, 0.18), xytext=(-0.54, 0.18),
            fontsize=22, color='red', alpha=1)

ax.annotate('losing team with hard schedule', xy=(0.2, 0.18), xytext=(0.2, 0.18),
            fontsize=22, color='orange', alpha=1)

ax.annotate('winning team with easy schedule', xy=(-0.54, 0.785), xytext=(-0.54, 0.785),
            fontsize=22, color='orange', alpha=1)

ax.annotate('winning team with hard schedule', xy=(0.18, 0.785), xytext=(0.18, 0.785),
            fontsize=22, color='green', alpha=1)

# create a new variable for each row of data called ‘ab’
# ab uses the AnnotationBbox function from matplotlib assign an x/y location to each image
# ax.add_artist function draws this on the plot
for index, row in my_data.iterrows():
    ab = AnnotationBbox(getImage(row['path']), (row['SOS'], row['W-L%']), frameon=False)
    ax.add_artist(ab)

# save image of figure
plt.savefig('MLB Team Records vs Strength of Schedule')
