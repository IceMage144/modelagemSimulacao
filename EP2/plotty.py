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
    top = mem[0][siz-1] - (mem[0][siz-1] - mem[0][siz-2])/2
    print("[", round(bot, 2), ",", round(top, 2), "]")
    plt.show()

def plot2():
    legend = ['Fgx', 'Fgy', 'Fgz', 'FgR']
    legend2 = ['Fmx', 'Fmy', 'Fmz', 'FmR']
    times = []
    matrix = []
    matrix2 = []
    fra, axarr = plt.subplots(nrows=2, ncols=1, figsize=(15, 10))
    f = open(sys.argv[1], mode='r')
    for line in f:
        if line[0] not in numbers:
            continue
        arr = line.split(';')[:-1]
        arr = [float(num.replace(',', '.')) for num in arr]
        nums = arr[1:4] + [np.sqrt(arr[1]**2 + arr[2]**2 + arr[3]**2)]
        nums2 = arr[4:] + [np.sqrt(arr[4]**2 + arr[5]**2 + arr[6]**2)]
        matrix.append(nums)
        matrix2.append(nums2)
        times.append(arr[0])
    f.close()
    matrix = np.array(matrix)
    matrix2 = np.array(matrix2)
    df = pd.DataFrame(matrix, columns=legend, index=times)
    df2 = pd.DataFrame(matrix2, columns=legend2, index=times)
    df.plot(ax=axarr[0])
    df2.plot(ax=axarr[1])
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
        raise


main()
