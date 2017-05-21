from numpy import sin, cos, pi
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Variáveis que descrevem o pêndulo
G = 9.80665 # Aceleração da gravidade em (m/s)^2
L = 1.0     # Comprimento do pêndulo em m

# Equação do pêndulo que dá d^theta/dt^2
def pendulumEquation (theta):
    return -(G/L) * sin (theta)

'''
Função que gera os pontos onde a massa do pêndulo estará. É chamada como
argumento para simPoints() e cada vez que é chamada, roda a próxima iteração
do loop e retorna o x e o y da massa do pêndulo no t atual.
'''
def simData():
    t_max = 30.0
    dt = 0.05
    t = 0.0
    theta = pi/3
    dydx_theta = 0

    # Algoritmo de Euler para calcular theta atual (usando equação do pêndulo)
    while t <= t_max:
        theta = theta + dydx_theta * dt
        dydx_theta = dydx_theta + pendulumEquation (theta) * dt
        t += dt
        yield t, theta

def simPoints(simData):
    t, theta = simData[0], simData[1]
    x, y = sin(theta), -cos(theta)

    time_text.set_text(time_template%(t))
    line.set_data([0, x], [0, y])

    return line, time_text

# Configurando o o plot

fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-2, 2), ylim=(-2, 2))
line, = ax.plot([], [], 'o-', ms=10)
#ax.grid() # Adiciona um grid para facilitar visualização.
time_template = 'Time = %.1f s'    # Imprime o tempo atual
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

'''
Chama o pacote de animação: (simData() é a user function) servindo como argumento
para simPoints()
'''
ani = animation.FuncAnimation(fig, simPoints, simData, blit=False,\
     interval=10, repeat=True)

# Salva a animação
#ani.save('pendulum.mp4', fps=24)

plt.show()
