#python version = 3.6
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import bisect

g = 9.8

class Commons:

    legends = {
        "time" : "Tempo",
        "gfx"  : "Fgx",
        "gFy"  : "Fgy",
        "gFz"  : "Fgz",
        "Bx"   : "Fmx",
        "By"   : "Fmy",
        "Bz"   : "Fmz",
        "x"    : "Fmx",
        "y"    : "Fmy",
        "z"    : "Fmz",
        "MF"   : "FmR"
    }
    dirs = ["right", "left", "top", "bottom"]

    def __plotCsv(self, csv, axis, cols, res=""):
        """
        Plots columns cols from csv file into axis and add an resultant force
        column if necessary
        """
        self.legends["r"] = res
        # read csv file
        file = "./CSV/" + csv + ".csv"
        df = pd.read_csv(file, sep=';', decimal=',', usecols=cols)
        if res:
            # add resultant force
            v = list(df)
            df = df.assign(r=lambda row : np.sqrt(row[v[1]]**2 + row[v[2]]**2 + row[v[3]]**2))
        # customizing the graph
        df.rename(columns=self.legends, inplace=True)
        df.plot(x='Tempo', ax=axis)
        for d in self.dirs:
            axis.spines[d].set_visible(False)
        axis.axis('off')
        axis.legend(loc='upper left')
        axis.set_xlim(0, np.max(np.asarray(df['Tempo'])))

    def __calculateError(self, states, pos):
        """
        Calculates the deviation of y axis error at observed times
        """
        s = 0
        stimes = states[0]
        spos = states[1]
        n = len(pos)
        for t, p in zip(self.times, pos):
            i = bisect.bisect_left(stimes, t) - 1
            if stimes[i+1] == t:
                y = spos[i+1]
            else:
                m = (spos[i]-spos[i+1])/(stimes[i]-stimes[i+1])
                y = m*(t-stimes[i]) + spos[i]
            s += (p-y)**2
        return np.sqrt(s/n)

class Ramp(Commons):

    # class variables
    DT = 0.1
    THETA = 0.148353
    MI = 0.055
    # Mi obtained by the system:
    # Sf = 6
    # Sf = g*t²*(sin(theta)-mi*cos(theta))/2
    # theta = 0.148353
    # average final time t = 3.621
    # g = 9.8

    def __init__(self, info):
        self.csv = info["csv"]
        self.fTime = info["fTime"]
        self.times = info["times"]
        self.obsTime = info["obsTime"]

    def __statesFEuler(self, theta, mi, dt):
        """
        Uses Euler algorithm and given ramp inclination (theta), kinetic
        friction coefficient (mi) and delta time (dt) to calculate space and
        speed of a sliding object
        """
        lstate = {"t" : 0, "s" : 0, "v" : 0}
        state = {"t" : 0, "s" : 0, "v" : 0}
        res = []
        for i in np.arange(0.0, self.fTime, dt):
            state["s"] = lstate["s"] + lstate["v"]*dt
            state["v"] = lstate["v"] + g*dt*(np.sin(theta)-mi*np.cos(theta))
            state["t"] = lstate["t"] + dt
            res.append(list(lstate.values()))
            lstate = state.copy()
        return np.array(res).transpose()

    def plotGraph(self):
        '''
        Plots the full simulation and data of a ramp sliding object in a
        matplotlib plot!
        '''
        f, axarr = plt.subplots(nrows=3, ncols=1, figsize=(15, 10))
        ax = axarr[0]
        # calculate space and speed
        realX = self.times
        realY = [2, 4]
        states = self.__statesFEuler(self.THETA, self.MI, self.DT)
        # plot informations
        ax.plot(states[0], states[1], label="espaço simulado")
        ax.plot(states[0], states[2], "g-", label="velocidade simulada")
        for t,i in zip(self.times, range(1,3)):
            ax.plot([t, t], [0, i*2], "r--")
        ax.scatter(realX, realY, color='red', marker="+", label="observado")
        # customize the graph
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_xlim(0, self.obsTime)
        ax.set_ylim(0, 6)
        # add legends and error
        err = self._Commons__calculateError(states, realY)
        ax.scatter(0, 0,  c = 'w', label=f"Erro: {round(err, 2)}")
        ax.set_title(self.csv, fontsize=16, color="#000c3d")
        ax.legend(loc='upper left')
        # plot csvs
        self._Commons__plotCsv(self.csv, axarr[1], [0, 1, 2, 3], "FgR")
        self._Commons__plotCsv(self.csv, axarr[2], [0, 4, 5, 6], "FmR")
        plt.tight_layout(pad=4, w_pad=0.5, h_pad=5.0)
        plt.show()

class Pendulum(Commons):

    # class variables
    THETA = np.pi/4
    LENGTH = 1.5
    DT = 0.1

    def __init__(self, info):
        self.csv = info["csv"]
        self.fTime = info["fTime"]
        self.times = info["times"]

    def __statesFEuler(self, itheta, length, dt):
        """
        Uses Euler algorithm and given initial angle (itheta), thread length
        (length) and delta time (dt) to calculate space and speed of a pendulum
        """
        lstate = {"t" : 0, "th" : itheta, "v" : 0}
        state = {"t" : 0, "th" : 0, "v" : 0}
        # gamma is the
        gamma = 0.043
        res = []
        for i in np.arange(0.0, self.fTime, dt):
            state["th"] = lstate["th"] + lstate["v"]*dt
            state["v"] = lstate["v"] - ((g*np.sin(state["th"]))/length + gamma*lstate["v"])*dt
            state["t"] = lstate["t"] + dt
            res.append(list(lstate.values()))
            lstate = state.copy()
        return np.array(res).transpose()

    def plotGraph(self):
        '''
        Plots the full simulation and data of a pendular movement in a
        matplotlib plot!
        '''
        f, axarr = plt.subplots(nrows=2, ncols=1, figsize=(15, 10))
        ax = axarr[0]
        # calculate space and speed and plot them
        states = self.__statesFEuler(self.THETA, self.LENGTH, self.DT)
        ax.plot(states[0], states[1], label="ângulo simulado")
        ax.plot(states[0], states[2], "g-", label="velocidade simulada")
        ypos = [0]*len(self.times)
        ax.scatter(self.times, ypos, color="r", marker="x", label="observado")
        # customize the graph
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_xlim(0, self.fTime)
        ax.set_ylim(-2, 2)
        # add legends and error
        err = self._Commons__calculateError(states, ypos)
        ax.scatter(0, 0,  c = 'w', label=f"Erro: {round(err, 2)}")
        ax.set_title(self.csv, fontsize=16, color="#000c3d")
        ax.legend(loc='upper right')
        # plot csv
        self._Commons__plotCsv(self.csv, axarr[1], [0, 1, 2, 3], "FmR")
        plt.tight_layout(pad=4, w_pad=0.5, h_pad=5.0)
        plt.show()

def main():
    if(len(sys.argv) == 2 and sys.argv[1][-5:] == ".json"):
        data = sys.argv[1]
    else:
        raise ValueError("You need to pass a single json file as argument!")
    # parse json file
    with open(data) as f:
        jsonData = json.loads(f.read())
    # create objects and plot their information
    for i in range(len(jsonData["Rampa"])):
        r = Ramp(jsonData["Rampa"][i])
        r.plotGraph()
    for i in range(len(jsonData["Pendulo"])):
        r = Pendulum(jsonData["Pendulo"][i])
        r.plotGraph()



if __name__ == '__main__':
    main()
