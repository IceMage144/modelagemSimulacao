import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

matplotlib.style.use('ggplot')

numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def plot1():
    legend = ['Fmx', 'Fmy', 'Fmz', 'FmR']
    times = []
    matrix = []
    mem = []
    last = 0
    fra, axarr = plt.subplots(nrows=1, ncols=1, figsize=(7.5, 10))
    f = open(sys.argv[1], mode='r')
    for line in f:
        if line[0] not in numbers:
            continue
        nums = [float(num.replace(',', '.')) for num in line.split(';')]
        matrix.append(np.array(nums[1:5]))
        times.append(nums[0])
        if nums[4] > 100:
            if nums[0] - last > 0.3:
                mem.append([round(nums[0], 2), nums[4]])
            top = len(mem) - 1
            if nums[4] > mem[top][1]:
                mem[top][0] = round(nums[0], 2)
                mem[top][1] = nums[4]
            last = nums[0]
    f.close()
    matrix = np.array(matrix)
    df = pd.DataFrame(matrix, columns=legend, index=times)
    df.plot(ax=axarr)
    axarr.legend(loc='upper left')
    siz = len(mem)
    mem = np.array(mem).transpose()
    print(repr(mem[0]))
    print("Length:", siz)
    bot = mem[0][0] - (mem[0][1] - mem[0][0])/2
    top = mem[0][siz-1] + (mem[0][siz-1] - mem[0][siz-2])/2
    print("[", round(bot, 2), ",", round(top, 2), "]")
    real = mem[0]-np.array([bot]*siz)
    print(repr(real))
    print(top-bot)
    plt.show()

def plot2():
    legend = {'time' : 'Tempo',
              'gfx'  : 'Fgx',
              'gFy'  : 'Fgy',
              'gFz'  : 'Fgz'}
    legend2 = {'time' : 'Tempo',
               'Bx'   : 'Fmx',
               'By'   : 'Fmy',
               'Bz'   : 'Fmz'}
    times = []
    matrix = []
    matrix2 = []
    fra, axarr = plt.subplots(nrows=2, ncols=1, figsize=(15, 10))
    df1 = pd.read_csv(sys.argv[1], sep=';', decimal=',', usecols=[0, 1, 2, 3])
    df1.rename(columns=legend, inplace=True)
    df1 = df1.assign(FgR=lambda row : np.sqrt(row["Fgx"]**2 + row["Fgy"]**2 + row["Fgz"]**2))
    df2 = pd.read_csv(sys.argv[1], sep=';', decimal=',', usecols=[0, 4, 5, 6])
    df2.rename(columns=legend2, inplace=True)
    df2 = df2.assign(FmR=lambda row : np.sqrt(row.Fmx**2 + row.Fmy**2 + row.Fmz**2))
    df1.plot(x='Tempo', ax=axarr[0])
    df2.plot(x='Tempo', ax=axarr[1])
    axarr[0].legend(loc='upper left')
    axarr[1].legend(loc='upper left')
    plt.show()

def main():
    try:
        if (sys.argv[2] == '1'):
            plot1()
        elif (sys.argv[2] == '2'):
            plot2()
    except IndexError:
        print("Usage: plotter <csv file path> <number of plots>")


main()
