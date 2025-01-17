import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main():
    # Parse data as data frame
    df = pd.read_csv('./data/Foreign_Exchange_Rates.csv')
    
    # Plot
    fig, ax = plt.subplots()
    for i in range(2, len(df.columns)):
        x = df[df.columns[i]].to_numpy()
        for k in range(len(x)):
            if x[k] == 'ND':
                x[k] = x[k-1]
            else:
                x[k] = float(x[k])
        ax.plot(x, label=df.columns[i])

    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1),
              ncol=1, borderaxespad=0)
    ax.set_ylabel('Local Currency/USD')
    ax.set_xlabel('Days from 01/03/2000')
    fig.subplots_adjust(right=0.55)
    fig.suptitle('Foreign Exchange Rate with repsect to USD (e.g YEN/USD)',
                 va='top', size='large')

    leg = interactive_legend()
    return fig, ax, leg

def interactive_legend(ax=None):
    if ax is None:
        ax = plt.gca()
    if ax.legend_ is None:
        ax.legend()

    return InteractiveLegend(ax.get_legend())

class InteractiveLegend(object):
    def __init__(self, legend):
        self.legend = legend
        self.fig = legend.axes.figure

        self.lookup_artist, self.lookup_handle = self._build_lookups(legend)
        self._setup_connections()

        self.update()

    def _setup_connections(self):
        for artist in self.legend.texts + self.legend.legendHandles:
            artist.set_picker(10) # 10 points tolerance

        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def _build_lookups(self, legend):
        labels = [t.get_text() for t in legend.texts]
        handles = legend.legendHandles
        label2handle = dict(zip(labels, handles))
        handle2text = dict(zip(handles, legend.texts))

        lookup_artist = {}
        lookup_handle = {}
        for artist in legend.axes.get_children():
            if artist.get_label() in labels:
                handle = label2handle[artist.get_label()]
                lookup_handle[artist] = handle
                lookup_artist[handle] = artist
                lookup_artist[handle2text[handle]] = artist

        lookup_handle.update(zip(handles, handles))
        lookup_handle.update(zip(legend.texts, handles))

        return lookup_artist, lookup_handle

    def on_pick(self, event):
        handle = event.artist
        if handle in self.lookup_artist:

            artist = self.lookup_artist[handle]
            artist.set_visible(not artist.get_visible())
            self.update()

    def on_click(self, event):
        if event.button == 3:
            visible = False
        elif event.button == 2:
            visible = True
        else:
            return

        for artist in self.lookup_artist.values():
            artist.set_visible(visible)
        self.update()

    def update(self):
        for artist in self.lookup_artist.values():
            handle = self.lookup_handle[artist]
            if artist.get_visible():
                handle.set_visible(True)
            else:
                handle.set_visible(False)
        self.fig.canvas.draw()

    def show(self):
        plt.show()

if __name__ == '__main__':
    fig, ax, leg = main()
    plt.show()