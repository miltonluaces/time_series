from os import path
import sys
sys.path.append('D:/source/repos')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='darkgrid')


def PlotTrends(dft):
    dft.reset_index(inplace=True)
    #dft.columns = ['open', '']
    plt.figure(figsize=(20, 10))
    ax = sns.lineplot(x=dft.index, y=dft['value'])
    ax.set(xlabel='Date')

    labels = dft['up'].dropna().unique().tolist()

    for label in labels:
        sns.lineplot(x=dft[dft['up']==label].index, y=dft[dft['up']==label]['value'], color='green')
        ax.axvspan(dft[dft['up'] == label].index[0], dft[dft['up'] == label].index[-1], alpha=0.2, color='green')

    labels = dft['down'].dropna().unique().tolist()

    for label in labels:
        sns.lineplot(x=dft[dft['down']==label].index, y=dft[dft['down']==label]['value'], color='red')
        ax.axvspan(dft[dft['down']==label].index[0], dft[dft['down']==label].index[-1], alpha=0.2, color='red')

    locs, _ = plt.xticks()
    labels = []

    for position in locs[1:-1]:
        labels.append(str(dft['Date'].loc[position])[:-9])

    plt.xticks(locs[1:-1], labels);
    
    
    
if __name__ == '__main__':

    va = VisualAssets()
    