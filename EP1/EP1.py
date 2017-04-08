import matplotlib.cm as cm
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

class Walker:
    # Constant / static variable - MAY BE USEFUL..
    SPACE = 30

    '''
    Walker attributes:

        name = the name of the Walker
        movType = "MRU" ou "MRUV"
        times = A dict with the movements!
    '''
    def __init__(self, name, movType, times):
        self.name = name
        self.movType = movType
        self.times = times


    def getVelocity(self):
        # Calcuate the mean velocity of a given Walker in a run
        meanVel = sum((self.__calculateVelocity(run) for run in self.times))/len(self.times)
        return meanVel

    def __calculateVelocity(self, run):
        # This should not be used for a MRUV run!
        msr = [float(m) for m in run['measures'].split("|") if m != '']
        # Alternate measure
        if(run['mType'] == 'A'):
            return sum((i/t for i, t in zip(range(5, 31, 5), msr)))/len(msr)
        else:
            # Takes the mean of both time measures of the same pos
            msr = [(i+j)/2 for i, j in zip(msr[:len(msr)//2],msr[len(msr)//2:])]
            # Makes deltaS/deltaT for every t and space, then takes the mean
            #print (sum((i/t for i, t in zip(range(10, 31, 10), msr)))/len(msr))
            return sum((i/t for i, t in zip(range(10, 31, 10), msr)))/len(msr)

    def __spaceF(self, run):
        # Return a closure in the form x(t)
        simVel = Walker.SPACE/self.__finalTime(run)
        def f(t):
            return simVel*t
        return f

    def __timeList(self, run):
        # Return the list of observed times. The length may vary
        # if it's an Alternate or Normal read.
        msr = [float(m) for m in run['measures'].split("|") if m != '']
        if(run['mType'] == 'N'):
            msr = [(i+j)/2 for i, j in zip(msr[:len(msr)//2],msr[len(msr)//2:])]
        return msr

    def __spaceList(self, run):
        # Return a list of spaces (e.g. [10, 20, 30]) and a list of
        # space xticks (e.g. [t1, t2, t3]). The length changes if it's Alternate.
        if(run['mType'] == 'N'):
            spcList = list(range(10,35, 10))
            xticks = ["t"+str(i) for i in range(1,4)]
        else:
            spcList = list(range(5, 35, 5))
            xticks = ["t"+str(i) for i in range(1,7)]

        return [spcList, xticks]


    def __finalTime(self, run):
        # Semantic way of getting the final time
        msr = self.__timeList(run)
        return msr[len(msr) - 1]



    def __plotCsv(self, run, axis):
        file = "./CSV/" + run['csv'] + ".csv"
        labels = ['Tempo', 'Fx', 'Fy', 'Fz', 'Fr']
        df = pd.read_csv(file, names=labels, sep=';', decimal=',')
        df.plot(ax=axis, x = 'Tempo')
        ax = plt.gca()
        ax.set_yticklabels([])
        ax.set_xlabel("")
        plt.tick_params(axis='both', which='both', bottom='off',
                        top='off', labelbottom='off', right='off',
                        left='off', labelleft='off')
        ax.axis('off')
        plt.legend(loc='upper right')
        axis.set_xlim(0, np.max(np.asarray(df['Tempo'])))

    def __setAnnotations(self, xObs, yObs, labels, values, ax):
        for x, y, text, val in zip(xObs, yObs, labels, values):
            ax.annotate(text+f"{round(val, 2)}",
            xy=(x, y + 1), xycoords='data',
            xytext=(-15, 25), textcoords='offset points',
            arrowprops=dict(facecolor='cyan', shrink=0.05),
            horizontalalignment='right', verticalalignment='bottom')


    def __calculateError(self, xObs, yObs, xt):
        '''
        Calculates the mean error of a list of points in the form (xObs, yObs) and
        the points (xObs, xt(xObs)), where xt is a function provided by the
        caller of the method.
        '''
        error = [abs(y - xt(x)) for x, y in  zip(xObs, yObs)]
        return sum(error)/len(error)



    def plotGraph(self):
        for run in self.times:
            xt = self.__spaceF(run)
            x = np.asarray([0, self.__finalTime(run)])
            y = list(map(xt, x))
            realX = self.__timeList(run)
            realY = self.__spaceList(run)[0]
            timeNames = self.__spaceList(run)[1]
            labelDict = {tValue : tName for tValue, tName in zip(realX, timeNames)}
            xticks = [int(i) for i in np.arange(0, self.__finalTime(run), 5)]
            #xticks = sorted(xticks + list(labelDict.keys()))
            labels = [str(i) for i in xticks]
            #labels = [labelDict.get(float(t), t) for t in labels]
            f, axarr = plt.subplots(nrows=2, ncols=1, figsize=(15, 10))
            axarr[0].plot(x, y, label = "simulado")
            for i, j in zip(list(labelDict.keys()), realY):
                axarr[0].plot([i, i], [0, j], 'r--')
            axarr[0].scatter(realX, realY,color='red', marker="+", label = "observado")
            axarr[0].set_xlabel('tempo (s)')
            axarr[0].set_ylabel('espaço (m)')
            axarr[0].set_title(run["csv"])
            axarr[0].set_xticklabels(labels)
            axarr[0].set_xticks(xticks)
            axarr[0].spines['right'].set_visible(False)
            axarr[0].spines['top'].set_visible(False)
            axarr[0].set_xlim(0, self.__finalTime(run) + 1)
            axarr[0].set_ylim(0, Walker.SPACE + 1)
            axarr[0].legend(shadow=True)
            self.__setAnnotations(realX, realY, list(labelDict.values()), list(labelDict.keys()), axarr[0])


            self.__plotCsv(run, axarr[1])
            plt.autoscale(False)
            plt.show()





'''
def fileBlock(f, n):

    # A generator which returns a block of 'n' lines of
    # a given file 'f', each time it is called, using iterators

    for line in f:
        yield ''.join(chain([line], islice(f, n - 1)))
'''


def addWalker(w, listWalkers):
    newWalker = Walker(w['walker'], w['movType'], w['times'])
    listWalkers.append(newWalker)

def main():
    # Parse a json file passed as argument
    if(len(sys.argv) == 2 and sys.argv[1][-5:] == ".json"):
        data = sys.argv[1]
    else:
        raise ValueError("You need to pass a single json file as argument!")

    listWalkers = list()

    with open(data) as f:
        jsonData = json.loads(f.read())
    for j in jsonData:
        addWalker(j, listWalkers)

    for w in listWalkers:
        print(f"Mean Velocity ({w.name} - {w.movType}) = {w.getVelocity():{3}.{5}} m/s")
        w.plotGraph()


if __name__ == '__main__':
    main()
