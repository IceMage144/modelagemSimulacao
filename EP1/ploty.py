import matplotlib.pyplot as plt

x = y = [1,2,3,4,5]

fig, ax = plt.subplots()

ax.plot(x,y)
leg = ax.legend(['line 1'], loc="upper left")

plt.draw()

p = leg.get_frame().get_bbox().bounds
print(p)

ax.annotate('Annotation Text', (p[0] + 3 , p[1] + 3), (p[2] + 3, p[3] + 3),
            xycoords='figure pixels', zorder=9)

plt.show()
