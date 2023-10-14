import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import seaborn as sns

# adjustable constants
FONT_SCALE = 2
TITLE_FONT_SIZE = 36
TITLE_COLOR = 'black'
AXES_FONT_SIZE = 27
ANNOTATION_FONT_SIZE = 17
GRID_COLOR = 'gray'
GRID_ALPHA = 0.2
XLIM = (-0.22, 0.22)
YLIM = (0.28, 0.67)
SUBTITLE_TEXT = '2023 MLB Teams'
SUBTITLE_FONT_SIZE = 30
SUBTITLE_COLOR = 'black'
CITATION_TEXT = 'data obtained from https://www.baseball-reference.com/leagues/MLB-standings.shtml'
CITATION_FONT_SIZE = 17
CITATION_COLOR = 'gray'
ARROW_COLOR = 'gray'
ARROW_STYLE = '->'

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def create_image_annotation(path):
    return OffsetImage(plt.imread(path), zoom=0.17, alpha=1)

def create_plot(data):
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.set(font_scale=FONT_SCALE)
    sns.scatterplot(x=data['SOS'], y=data['W-L%'], ax=ax)
    
    ax.set_title('Comparing Records and Strength of Schedules', size=TITLE_FONT_SIZE, color=TITLE_COLOR)
    ax.set_xlabel('Strength of Schedule', size=AXES_FONT_SIZE)
    ax.set_ylabel('Win-Loss Percentage', size=AXES_FONT_SIZE)
    ax.grid(False)
    
    ax.axvline(x=0, color=GRID_COLOR, alpha=GRID_ALPHA)
    ax.axhline(y=0.5, color=GRID_COLOR, alpha=GRID_ALPHA)
    
    ax.set_xlim(XLIM)
    ax.set_ylim(YLIM)
    
    return fig, ax

def add_annotations(ax, data):
    annotations = [
        ('losing teams with easy schedules', -0.215, 0.295, 'red'),
        ('losing teams with hard schedules', 0.1, 0.295, 'orange'),
        ('winning teams with easy schedules', -0.215, 0.66, 'orange'),
        ('winning teams with hard schedules', 0.095, 0.66, 'green')
    ]

    for text, x, y, color in annotations:
        ax.annotate(text, xy=(x, y), xytext=(x, y), fontsize=ANNOTATION_FONT_SIZE, color=color, alpha=1)

    for index, row in data.iterrows():
        ab = AnnotationBbox(create_image_annotation(row['path']), (row['SOS'], row['W-L%']), frameon=False)
        ax.add_artist(ab)

def main():
    data = load_data('/kaggle/input/mlb-standings-2023/standings_2023.csv')
    
    # add a column for 'path' for team images
    data['path'] = '/kaggle/input/mlbteamlogos/' + data['Tm'] + '.png'
    
    # drop rows with 'Tm' equal to 'Average'
    data = data.drop(data[data['Tm'] == 'Average'].index)
    
    sns.set_style("whitegrid")
    fig, ax = create_plot(data)
    add_annotations(ax, data)
    
    # add the subtitle as a text annotation below the title
    ax.annotate(SUBTITLE_TEXT, xy=(0.5, 0.97), xycoords='axes fraction', fontsize=SUBTITLE_FONT_SIZE, color=SUBTITLE_COLOR, ha='center')
    # add citation for data as a text annotation at bottom of plot
    ax.annotate(CITATION_TEXT, xy=(0.5, 0.01), xycoords='axes fraction', fontsize=CITATION_FONT_SIZE, color=CITATION_COLOR, ha='center')
    
    # define text for annotations where team logos are not visible
    text1 = 'San Diego Padres\nbehind\nCincinnati Reds'
    text2 = 'Pittsburgh Pirates\nbehind\nNew York Mets'
    
    # define coordinates for the arrowheads and text
    arrow_xy1 = (0.01, 0.506)
    text_xy1 = (0.05, 0.525)
    arrow_xy2 = (0.01, 0.467)
    text_xy2 = (0.05, 0.44)
    
    # define arrow properties
    arrow_props = dict(facecolor=ARROW_COLOR, edgecolor=ARROW_COLOR, arrowstyle=ARROW_STYLE)
    
    # add the annotations with adjusted coordinates for team logos that are blocked
    ax.annotate(text1, xy=arrow_xy1, xytext=text_xy1, fontsize=ANNOTATION_FONT_SIZE, color=ARROW_COLOR, alpha=1, ha='center', va='center', arrowprops=arrow_props)
    ax.annotate(text2, xy=arrow_xy2, xytext=text_xy2, fontsize=ANNOTATION_FONT_SIZE, color=ARROW_COLOR, alpha=1, ha='center', va='center', arrowprops=arrow_props)
    
    # save the figure as a PNG image
    plt.savefig('MLB_Team_Records_v_Strength_of_Schedule_2023.png')
    plt.show()

if __name__ == "__main__":
    main()
