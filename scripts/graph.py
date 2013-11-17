import numpy, sys, re

from matplotlib import pyplot
from matplotlib.axes import Axes
from scipy import stats

class LineGraph:
    """
        2013-11-01: Wrapper for pyplot
    """
    
    def __init__(self):
        self.graph = pyplot
        # self.graph.axis([0, 700000, 0, 1.4])
        # self.colors = ["r", "b", "g", ...]
        self.nextColor = 0

    def addLine(self, xs, ys, color):
        """
            2013-11-01:
                asdf
        """
        self.graph.plot(xs, ys, color=color)

    def updateLine(self, xs, ys):
        # TODO need a way to update one line. To pick one and update only that.
        # Sorta useful: http://stackoverflow.com/questions/10944621/dynamically-updating-plot-in-matplotlib
        pass

    def save(self, filename):
        self.graph.savefig(filename)

    def show(self):
        # self.graph.relim()
        # self.graph.autoscale_view()
        self.graph.show()

class IBParser:

    def __init__(self, filename):
        self.filename = filename
        # First time we start collecting at (assumes every time is the 'seconds since last epoch')
        self.initial_time = None

        # Info from top of feed
        self.meta = {}

        self.bestAsks = []
        self.bestBids = []
        self.priceWeightedAverage = []
        self.timeValues = []

    def parseAll(self):
        """
            2013-11-01: Read in allll the data from the file
        """
        with open(self.filename) as f:
            # Parse 2 lines of metadata
            for _ in xrange(0, 2):
                key, val = next(f).rstrip().split(":", 1)
                self.meta[key] = val
            # Parse the books until there are none left
            while True:
                try:
                    time = int(next(f).split(":", 1)[0])
                    if not self.initial_time: 
                        self.initial_time = time
                    self.timeValues.append(time - self.initial_time)
                    bestBid = 0
                    bestAsk = 0
                    prices = []
                    weights = []
                    for _ in xrange(0, 5):
                        bidData, askData = next(f).strip().split(" | ")

                        pStr, qStr = bidData.split(" ")
                        p, q = float(pStr), int(qStr)
                        bestBid = max(bestBid, p)
                        prices.append(p)
                        weights.append(q)

                        pStr, qStr = askData.split(" ")
                        p, q = float(pStr), int(qStr)
                        bestAsk = max(bestAsk, p)
                        prices.append(p)
                        weights.append(q)

                    self.bestBids.append(bestBid)
                    self.bestAsks.append(bestAsk)
                    wAvg = numpy.average(prices, weights=weights)
                    self.priceWeightedAverage.append(wAvg)
                    print("BID = %s , ASK = %s , AVG = %s" % (bestBid, bestAsk, wAvg))
                except StopIteration:
                    break
            return

def plotScatter(xs, ys, fig_name=None):
    """
        2013-11-01:
            Plot the points defined by `zip(xs, ys)`
    """
    pyplot.scatter(xs,ys)
    pyplot.axis([0, 1, 0, 0.5])
    if fig_name:
        pyplot.savefig(fig_name)
    pyplot.show()

def plotHistogram(values, bins=None):
    """
        2013-03-08:
            Create and show a histogram from given list of values.
            `numbins` optionally sets the number of columns in the output

            http://stackoverflow.com/questions/5328556/histogram-matplotlib
    """
    histogram, bins = numpy.histogram(values, bins=bins) if bins is not None else numpy.histogram(values)
    width = 0.6*(bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    pyplot.bar(center, histogram, align='center', width=width)
    # TODO Saves in current directory only
    # pyplot.savefig('figure-name')
    pyplot.show()

def run():
    """
        make a graph with Hersh's output
        three line, best buy, best sell, quantity-weightedverage
    """
    parser = IBParser("sample.txt")
    parser.parseAll()
    plot = LineGraph()
    plot.addLine(parser.timeValues, parser.bestBids, 'b')
    plot.addLine(parser.timeValues, parser.bestAsks, 'g')
    plot.addLine(parser.timeValues, parser.priceWeightedAverage, 'r')
    plot.show()

if __name__=="__main__":
    run()
