import numpy as np
import matplotlib.pyplot as plt

#================================================================
#                VARIABILI DI CONTROLLO DELL SCRIPT
#================================================================

# LaTeX typesetting maths and descriptions
tex = True
# manually choose spacing between axis ticks
tick = True

#================================================================
#                       FUNZIONI PER LO SVILUPPO
#================================================================
def f(x):
    return x**3
def f_prim(x):
    return 3*(x**2)

#================================================================
#                       FUNZIONI PER IL FIT
#================================================================
def sck(V):
    return I0*(np.exp(V/nVt) - 1)

def errFun(V, V0):
    return sck(V) + (V - V0)/R

def deriv_errFun(V):
    return I0 / nVt * np.exp(V/nVt) + 1./R;

def curr(V):
    l = []
    b = []
    v = V;
    #l.append(0.)
    #b.append(v)
    for i in range(Nstep):
        a = deriv_errFun(v)
        v = v - errFun(v, V) /a
        b.append(v)
        l.append((V-v)/R)
    return np.array(l), np.array(b)

def ddp(I):
    return nVt*np.log((I0+I)/I0) + R*I

#================================================================
#                  GRAFICO DEL METODO DI NEWTON
#================================================================
if tex:
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

fig1 = plt.figure(1)
gridsize = (3, 1)
plt.xlabel("$x$ [arb. un]", x=0.92)
plt.ylabel("$y$ [arb. un]")
plt.grid(c = "gray")
plt.grid(b=True, which='major', c='#666666', ls='-')
plt.grid(b=True, which='minor', c='#999999', ls='-', alpha=0.2)
currXlim = [-2., 4.]
currYlim = [-1., f(3.)+1]
plt.xlim(currXlim[0], currXlim[1])
plt.ylim(currYlim[0], currYlim[1])

bucket = np.linspace(-4., 4., 1000)
plt.plot(bucket, f(bucket), c = 'k', label = '$f(x)$')

plt.errorbar(3., f(3.), marker = 'o', ls = '', c = 'r',
             label = r'$\left( x[i],\; f(x[i])\, \right)$')

plt.plot(bucket, f_prim(3.)*(bucket - 3.) + f(3.) , c = 'r',
         label = r'tangente in $\left( x[i],\; f(x[i])\, \right)$')

#print(3. - f(3.)/f_prim(3))

plt.title("Visualizzazione grafica relativa ad una singola iterazione")

plt.errorbar(0., 0., marker = 's', ls = '', c = 'k',
             label = r'$\left( v,\; f(v)\, \right)$')

plt.errorbar(2., 0., marker = 'x', ls = '', c = 'b',
             label = r'$\left( x[i+1],\; 0\, \right)$')

plt.errorbar(2., f(2.), marker ='o', ls = '', c = 'g',
             label = r'$\left( x[i+1],\; f(x[i+1])\, \right)$')

retta = []
for i in range(len(bucket)):
    retta.append(0.)
retta = np.array(retta)
plt.plot(bucket, retta, c = 'k', ls = '--', label = '$y = 0$')
plt.minorticks_on()
plt.tick_params(direction='in', length=5, width=1., top=True, right=True)
plt.tick_params(which='minor', direction='in', width=1., top=True, right=True)
legend = plt.legend(loc='upper left', shadow=True, fontsize=12)
plt.tight_layout()

#================================================================
#         GRAFICI DELLA CONVERGENZA AL MODELLO DEL DIODO
#================================================================

R = 0.0475
I0 = 3.18e-9
nVt = 0.0464

Nstep = 20

iteration = []
for i in range(Nstep):
    iteration.append(i+1)

I1 = 1.
I2 = 5.
I3 = 7.

voltage1 = ddp(I1)
l1, a1 = curr(voltage1)
voltage2 = ddp(I2)
l2, a2 = curr(voltage2)
voltage3 = ddp(I3)
l3, a3 = curr(voltage3)

fig2 = plt.figure(2)
gridsize = (1., 1./3)
plt.title("Convergenza a $I$ col metodo di Newton", size = 12)
plt.xlabel("Grado di iterazione", size = 11, x = 0.8)
plt.ylabel(r"$I$ - corrente dalla serie [A]", size = 11)

plt.errorbar(iteration, abs(l1 - I1), c = 'r', ls = '-', marker = 'o',
             label = 'valori ottenuti dalla serie (1 A)')
plt.errorbar(iteration, abs(l2 - I2), c = 'k', ls = '-', marker = 's',
             label = 'valori ottenuti dalla serie (5 A)')
plt.errorbar(iteration, abs(l3 - I3), c = 'b', ls = '-', marker = 'X',
             label = 'valori ottenuti dalla serie (7 A)')
plt.grid(c = "gray")
plt.grid(b=True, which='major', c='#666666', ls='--')
plt.grid(b=True, which='minor', c='#999999', ls='--', alpha=0.2)

plt.minorticks_on()
plt.yscale('log')
ax=plt.gca()
ax.tick_params(direction='in', length=5, width=1., top=True, right=True)
ax.tick_params(which='minor', direction='in', width=1., top=True, right=True)
if tick:
    ax.xaxis.set_major_locator(plt.MultipleLocator(2))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_locator(plt.LogLocator(numticks=16))
    ax.yaxis.set_minor_locator(plt.LogLocator(subs=np.arange(2, 10)*.1,
                                              numticks = 16))
    ax.xaxis.set_minor_formatter(plt.NullFormatter())
plt.tight_layout()
legend = plt.legend(loc='upper right', shadow=True)

fig3 = plt.figure(3)
gridsize = (1, 1./3)
plt.title("Convergenza a $v$ col metodo di Newton", size = 12)
plt.xlabel("Grado di iterazione", size = 11, x = 0.8)
plt.ylabel("$x - v$  [V]", size = 11)
voltage1 = ddp(I1)
voltage2 = ddp(I2)
voltage3 = ddp(I3)
variable1 = voltage1 - I1*R
variable2 = voltage2 - I2*R
variable3 = voltage3 - I3*R
l1, a1 = curr(voltage1)
l2, a2 = curr(voltage2)
l3, a3 = curr(voltage3)
plt.errorbar(iteration, a1 - variable1, c = 'r', ls = '-', marker = 'o',
             label = 'valori ottenuti dalla serie (5 A)')
plt.errorbar(iteration, a2 - variable2, c = 'k', ls = '-', marker = 's',
             label = 'valori ottenuti dalla serie (1 A)')
plt.errorbar(iteration, a3 - variable3, c = 'b', ls = '-', marker = 'X',
             label = 'valori ottenuti dalla serie (7 A)')
b = np.zeros(1000)
ax=plt.gca()
ax.set_yscale('log')
ax.grid(b=True, which='major', c='#666666', ls='--', alpha = 0.7)
#, linewidth = 1)#, dashes = (1, 5, 0.1, 0.5))
ax.grid(b=True, which='minor', c='#999999', ls='--', alpha=0.2)
#, linewidth = 1)#, dashes = (1, 1, 0.1, 0.1))
legend = ax.legend(loc='upper right', shadow=True)

ax.minorticks_on()
ax.tick_params(direction='in', length=5, width=1., top=True, right=True)
ax.tick_params(which='minor', direction='in', width=1., top=True, right=True)
if tick:
    ax.xaxis.set_major_locator(plt.MultipleLocator(2))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_locator(plt.LogLocator(numticks=16))
    ax.yaxis.set_minor_locator(plt.LogLocator(subs=np.arange(2, 10)*.1,
                                              numticks = 16))
    ax.xaxis.set_minor_formatter(plt.NullFormatter())
plt.tight_layout()
plt.show()
