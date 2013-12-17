import numpy
import random
import re
import sys

from matplotlib import pyplot
from scipy import stats

T = [x for x in xrange(1, 101)]
# Fraction of informed traders. 0.2..0.7 correspond to range of market shares of institutional investors
M = [float("0.%s" % x) for x in xrange(1, 10)]

# Proir distribution for an asset
# P = \{ P(V) | P(V_j) \in \{0.1..0.8\} for j = 1,2,3 and \sum_1^3 P(V_j) = 1\}
# pick 3 values, at random, in interval that add up to 1
def getP():
    n1 = random.randint(1, 8)
    print n1
    n2 = random.randint(1, 9-n1)
    print n2
    n3 = 10 - n1 - n2
    print n3
    return [float("0.%s" % x) for x in [n1, n2, n3]]
# pp = []
# def allp():
#     while (len(pp) < 36):
#         g = getP()
#         if g not in pp:
#             pp.append(g)
#     return pp
P = [[0.5, 0.4, 0.1], [0.2, 0.6, 0.2], [0.7, 0.2, 0.1], [0.6, 0.2, 0.2], [0.7, 0.1, 0.2], [0.3, 0.2, 0.5], [0.5, 0.3, 0.2], [0.2, 0.4, 0.4], [0.1, 0.6, 0.3], [0.1, 0.1, 0.8], [0.4, 0.5, 0.1], [0.8, 0.1, 0.1], [0.1, 0.7, 0.2], [0.1, 0.3, 0.6], [0.3, 0.6, 0.1], [0.6, 0.3, 0.1], [0.2, 0.7, 0.1], [0.4, 0.2, 0.4], [0.2, 0.2, 0.6], [0.1, 0.4, 0.5], [0.2, 0.5, 0.3], [0.1, 0.8, 0.1], [0.3, 0.3, 0.4], [0.4, 0.4, 0.2], [0.3, 0.1, 0.6], [0.5, 0.1, 0.4], [0.3, 0.5, 0.2], [0.4, 0.1, 0.5], [0.6, 0.1, 0.3], [0.2, 0.3, 0.5], [0.3, 0.4, 0.3], [0.2, 0.1, 0.7], [0.1, 0.2, 0.7], [0.5, 0.2, 0.3], [0.4, 0.3, 0.3], [0.1, 0.5, 0.4]]
# Risky asset thats each value V1 V2 V3 with positive probability

# Conditional signal distribution P(S|V)
# C = { P(S|V) | pij \in [0.1 .. 0.8] for i,j = 1,2,3} 
# ???
C = [float("0.%s" % x) for x in xrange(1, 9)]

# omega = M * P * C
omega = [(x,y,z) for x in M for y in P for z in C]
# Each element of omega represents a stock
# Each stock traded over T points of time
# they repeated 2000 simulaations for each parmetrization
prob_noise = 1./3.

def getPrev(i, history):
    """ Find the last action for trader i"""
    for (j, d, h) in history[::-1]:
        if i==j:
            return d
    return None

def getCrowd(history):
    numBuy = 0
    numSell = 0
    numHold = 0
    for (j, d, h) in history:
        if d == "BUY":
            numBuy += 1
        elif d == "SELL":
            numSell += 1
        else:
            numHold += 1
    if numBuy > numSell:
        return "BUY"
    elif numSell > numBuy:
        return "SELL"
    else:
        return None

def getAction(price, history):
    """ Informed traders chooses to buy / sell / hold"""
    signal = random.random()
    if signal < price:
        return "SELL"
    elif signal > price:
        return "BUY"
    else:
        return "HOLD"

def run2():
    """
    Random price, random signal. Not at all dependent on others
    """
    numtraders = 50
    results_by_mu = {}
    n = 1
    for stock in omega:
        (prop_informed, values, signal) = stock
        num_informed = int(numtraders * prop_informed)
        num_noise = numtraders - num_informed
        # Fill with triplees (trader number, decision, hereded)
        history = []
        # Each timestep
        for t in T:
            price = random.random()
            # Simulate informed
            for i in xrange(0, num_informed):
                # make a decision based on past stuff
                action = getAction(price, history)
                prev_action = getPrev(i, history)
                crowd_choice = getCrowd(history)
                # herded in prev != current and history has more buys than sells
                herded = (action != prev_action) and (crowd_choice == action)
                history.append((i, action, herded))
            # Simulate noise (should probably happen in parallel)
            for j in xrange(num_informed, numtraders):
                action = random.random()
                outcome = None
                if action < prob_noise:
                    # Buy
                    outcome = "BUY"
                elif action < (prob_noise + prob_noise):
                    # sell
                    outcome = "SELL"
                else:
                    # hold
                    outcome = "HOLD"
                history.append((j, outcome, False))
        num_informed = len([ a for (a,b,c) in history if a < num_informed ])
        num_buy = len([ a for (a,b,c) in history if b == "BUY" and c ])
        num_sell = len([ a for (a,b,c) in history if b == "SELL" and c ])
        bhi = num_buy / float(num_informed)
        shi = num_sell / float(num_informed)
        if prop_informed not in results_by_mu:
            results_by_mu[prop_informed] = [(bhi, shi)]
        else:
            results_by_mu[prop_informed].append((bhi, shi))
        print "FINISHED ROUND %s" % n
        n += 1
    with open("/tmp/herd2.csv", "w") as f:
        for (mu, vals) in results_by_mu.iteritems():
            avg_b = sum([x for (x,y) in vals]) / float(len(vals))
            avg_s = sum([y for (x,y) in vals]) / float(len(vals))
            print>>f,("%s,%s,%s" % (mu, avg_b, avg_s))

def getXYZ(fname):
    xs,ys,zs = [], [], []
    with open(fname, "r") as f:
        for line in f:
            x,y,z = [float(x) for x in line.strip().split(",")]
            xs.append(x)
            ys.append(y)
            zs.append(z)
    return xs, ys, zs

def plotScatter(x, y, fig_name=None):
    # Plot the graph
    pyplot.scatter(x,y)
    pyplot.axis([0, 1, 0, 0.5])
    if fig_name:
        pyplot.savefig(fig_name)
    pyplot.show()

if __name__ == "__main__":
    run2()
