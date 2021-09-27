from matplotlib import ticker
import matplotlib.pyplot as plt
from typing import Counter
from utils.aggregateAnalysis import stats
from os import listdir
from matplotlib.patches import PathPatch
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

 # Plot roll distribution
def rollDistributionChart(rolledNumberCount: Counter, rollStatistics: stats, outputFolder: str, rollGraphFile: str) -> None:
    
    def tickFormatter(x, pos):
        return minorTickLabels[pos]
    
    column_names = [str(x) for x in range(1,100)]
    possibleRolls = list(range(1,100))
    
    formatter = ticker.FuncFormatter(tickFormatter)

    # Minor tick labels will be every second value in possibleRolls
    # Because minor labels start at x=-1 for some reason, add an extra 0 to the start of the label list
    minorTickLabels = [0]+possibleRolls[1::2]
    minorTickLabels.append(100)
    minorTickLabels.append(102)
    values = [rolledNumberCount[x] if x in rolledNumberCount else 0 for x in possibleRolls]
    plt.figure(figsize=(15,4),dpi=100)
    plt.bar(column_names, values)
    # Unclear why, but have to shift median and mean lines left 1 due to unexplainable offset
    plt.axvline(rollStatistics.mean-1, color='red', label='Mean Roll')
    plt.axvline(rollStatistics.median-1, color='black', label='Median Roll')
    plt.legend()
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.xaxis.set_minor_formatter(formatter)
    ax.tick_params(axis='x', which='minor', length=15)
    ax.autoscale(enable=True, axis='x',tight=True)
    try:
        plt.savefig(outputFolder+rollGraphFile, transparent=True)
    except OSError:
        print("Unable to save roll distribution chart. Is the file open?")

def img_to_pie( fn, wedge, xy, zoom=1, ax = None):
    if ax==None: ax=plt.gca()
    im = plt.imread(fn, format='png')
    path = wedge.get_path()
    patch = PathPatch(path, facecolor='none')
    ax.add_patch(patch)
    imagebox = OffsetImage(im, zoom=zoom, clip_path=patch, zorder=-10)
    ab = AnnotationBbox(imagebox, xy, xycoords='data', pad=0, frameon=False)
    ax.add_artist(ab)

positions = [(0,0),(0,0),(0,0),(0,0)]
zooms = [0.3,0.3,0.3,0.3]
positions = positions*4
zooms = zooms*4



def pieChartPercentWins(winPercents: dict, outputFolder: str, pieChartFile: str) -> None:
    labels = sorted([key for key in winPercents.keys()], key= lambda key: winPercents[key])
    sizes = [value[2] for value in winPercents.values()]
    sizes.sort()
    fig2, ax2 = plt.subplots()
    wedges, text, label = ax2.pie(sizes,labels=labels, autopct='%1.0f%%', startangle=90, wedgeprops={'color':(1.0,1.0,1.0,0.0), 'edgecolor':'k'}, pctdistance=0.8, counterclock=False)
    ax2.axis('equal')
    images = listdir(".\docs\cookies")
    images = images*4
    for i in range(len(labels)):
        fn = "docs/cookies/{}".format(images[i])
        img_to_pie(fn, wedges[i], xy=positions[i], zoom = zooms[i])
        wedges[i].set_zorder(10)
        text[i].set_zorder(10)
        label[i].set_zorder(10)

    plt.savefig(outputFolder+pieChartFile, transparent=True, bbox_inches='tight')

