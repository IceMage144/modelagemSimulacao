import sys
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

def main():
    # Parse a json file passed as argument
    if(len(sys.argv) == 2 and sys.argv[1][-5:] == ".json"):
        data = sys.argv[1]
    else:
        raise ValueError("You need to pass a single json file as argument!")

    #Creates a list of Walkers objects
    listWalkers = list()
    with open(data) as f:
        jsonData = json.loads(f.read())
    for j in jsonData:
        addWalker(j, listWalkers)

    # TODO: REMOVE this. This calculates the mean velocity of every walker, then plot a graph
    for w in listWalkers:
        print(f"Mean Velocity ({w.name} - {w.movType}) = {w.getVelocity():{3}.{5}} m/s")
        w.plotGraph()

def addWalker(w, listWalkers):
    newWalker = Walker(w['walker'], w['movType'], w['times'])
    listWalkers.append(newWalker)

class Walker:
    '''
    Walker represents a person's experiment, and it's read from the json.
        name = the name of the Walker
        movType = "MRU" ou "MRUV"
        times = A dict with the movements!
    '''
    SPACE = 30

    def __init__(self, name, movType, times):
        self.name = name
        self.movType = movType
        self.times = times


    def getVelocity(self):
        '''
        Returns the mean velocity of a Walker in all of his runs!
        Should only be used with MRU movements!
        '''
        if self.movType != "MRU":
            raise ValueError("getVelocity(): You can't get MRUV mean velocity!")
        meanVel = sum((self.__calculateVelocity(run) for run in self.times))/len(self.times)
        return meanVel

    def __calculateVelocity(self, run):
        '''
        Calculate the mean Velocity of a given run, should only be
        used with MRU movements.
        '''
        #TODO: Modify so that the simulated mean velocity uses the CSV final time.
        # TODO: Probably this will be removed!!
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
        '''
        Calculates a space funtion of a run. A space function f(t)
        is a function that returns the space associated with a given t.

        Note that this returns a closure.
        '''
        #TODO: Change final time to be something from the CSV
        simVel = Walker.SPACE/self.__finalTime(run)
        def f(t):
            return simVel*t
        return f

    def __timeList(self, run):
        '''
        Return the list of observed times. The length may vary
        if it's an Alternate or Normal read.
        '''
        msr = [float(m) for m in run['measures'].split("|") if m != '']
        if(run['mType'] == 'N'):
            msr = [(i+j)/2 for i, j in zip(msr[:len(msr)//2],msr[len(msr)//2:])]
        return msr

    def __spaceList(self, run):
        '''
        Return a list of spaces (e.g. [10, 20, 30]) and a list of space
        xticks (e.g. [t1, t2, t3]). The length changes if it's Alternate.
        '''
        if(run['mType'] == 'N'):
            spcList = list(range(10,35, 10))
            xticks = ["t"+str(i) for i in range(1,4)]
        else:
            spcList = list(range(5, 35, 5))
            xticks = ["t"+str(i) for i in range(1,7)]

        return [spcList, xticks]


    def __finalTime(self, run):
        fTime = run["tcsv"][1] - run["tcsv"][0]
        # Semantic way of getting the final time...
        return fTime



    def __plotCsv(self, run, axis):
        '''
        Receives a run, and plot the CSV in a given axis!
        It removes labels, set a xlim, and add legend.
        '''
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

    def __setAnnotations(self, **kwargs):
        '''
        Plot the measured time, the calculated error, and the
        mean velocity if it's MRU.
        '''
        #TODO: Should plot different things if it's MRUV, e.g.:
        #      plot the mean acceleration, and the two different errors
        # Get arguments
        xObs = kwargs['xObs']
        yObs = kwargs['yObs']
        labels = kwargs['labels']
        values = kwargs['values']
        error = kwargs['error']
        meanVel = kwargs['meanVel']
        ax = kwargs['ax']
        # Observed time annotation
        for x, y, text, val in zip(xObs, yObs, labels, values):
            ax.annotate(text+f" ({round(val, 2)})",
            xy=(x, y + 1), xycoords='data',
            xytext=(-15, 25), textcoords='offset points',
            arrowprops=dict(facecolor='cyan', shrink=0.05),
            horizontalalignment='right', verticalalignment='bottom')
        if(self.movType == "MRU"):
            #Display meanVelocity
            ax.annotate(f"Velocidade Média:{meanVel} m/s",
            xy=(0, 0), xycoords='data',
            xytext=(+197.5, +175), textcoords='offset points', fontsize=13, color = "#f45100",
            horizontalalignment='right', verticalalignment='bottom')
            # Display error
            ax.annotate("Erro: "+f"{round(error, 2)}",
            xy=(0, 0), xycoords='data', xytext=(+78, +160), textcoords='offset points',
            fontsize=13, color = "#f45100", horizontalalignment='right',
            verticalalignment='bottom')


    def __calculateError(self, xObs, yObs, xt):
        '''
        Calculates the mean error of a list of points in the form (xObs, yObs) and
        the points (xObs, xt(xObs)), where xt is a function provided by the
        caller of the method.
        '''
        # This is an abstract way of calculating the errors,
        # it can be used either with MRU or MRUV
        error = [abs(y - xt(x)) for x, y in  zip(xObs, yObs)]
        return sum(error)/len(error)



    def plotGraph(self):
        '''
        Plots the full simulation and data in a matplotlib plot!
        '''
        '''
        TODO: Adjust to plot for MRUV (or create a different PRIVATE method and call it here).
              The different function would probably use gridspec to create customized
              subplots position (http://matplotlib.org/users/gridspec.html), or try
              to plot both velocity in the same subplot, but using a secondary axis to
              show the different data (check this http://matplotlib.org/examples/api/two_scales.html).
              The plotCSV call would be almost equal, you just would have to pass the
              right axis to plot the csv.
        '''
        if self.movType == "MRU":
            for run in self.times:
                # Simulated: xt - space Function , (x, y) simulated graph
                xt = self.__spaceF(run)
                x = np.asarray([0, self.__finalTime(run)])
                y = list(map(xt, x))
                # Observed: (realX, realY) observed points in action!
                realX = self.__timeList(run)
                realY = self.__spaceList(run)[0]
                # Labels and Xticks
                timeNames = self.__spaceList(run)[1]
                xticks = [int(i) for i in np.arange(0, self.__finalTime(run), 5)]
                labels = [str(i) for i in xticks]
                # Create the plot, and do matplotlib stuff
                f, axarr = plt.subplots(nrows=2, ncols=1, figsize=(15, 10))
                axarr[0].plot(x, y, label = "simulado")
                for i, j in zip(realX, realY):
                    axarr[0].plot([i, i], [0, j], 'r--')
                axarr[0].scatter(realX, realY,color='red', marker="+", label = "observado")
                axarr[0].set_xlabel('tempo (s)', fontsize=13)
                axarr[0].set_ylabel('espaço (m)', fontsize=13)
                axarr[0].set_title(self.movType+" - "+run["csv"], fontsize=16, color="#000c3d")
                axarr[0].set_xticklabels(labels)
                axarr[0].set_xticks(xticks)
                axarr[0].spines['right'].set_visible(False)
                axarr[0].spines['top'].set_visible(False)
                axarr[0].set_xlim(0, self.__finalTime(run) + 1)
                axarr[0].set_ylim(0, Walker.SPACE + 1)
                axarr[0].legend(shadow=True)
                # Annotate our plot
                self.__setAnnotations( xObs = realX, yObs = realY, labels = timeNames,
                    values = realX, error = self.__calculateError(realX, realY, xt),
                    meanVel = round(xt(1), 3), ax = axarr[0])
                # Plot a CSV in the second axis
                self.__plotCsv(run, axarr[1])
                plt.autoscale(False)
                # Show the final plot! :)
                plt.show()



if __name__ == '__main__':
    main()
