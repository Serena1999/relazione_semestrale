import matplotlib.pyplot as plt
import numpy as np

''' Variables that control the script '''
log = True # log-scale axis/es
tick = True # manually choose spacing between axis ticks
tex = True # LaTeX typesetting maths and descriptions

if tex:
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    
#0.22k
x, my, sy, smy = np.loadtxt("b.txt", unpack=True)
fig, ax = plt.subplots()
ax.plot(x, my, color='r', label = r'$\mu_y \; (A)$')
ax.fill_between(x, my+smy, my-smy, facecolor='r', alpha=0.5, 
                label = r'Var$(\mu_y) \; (A)$')

# 2.2k
x, my, sy, smy = np.loadtxt("a.txt", unpack=True)
ax.plot(x, my, color='b', label = r'$\mu_y \; (B)$')
ax.fill_between(x, my+smy, my-smy, facecolor='b', alpha=0.5,
                label = r'Var$(\mu_y) \; (B)$')

if log:
    ax.set_yscale('log')
ax.minorticks_on()
ax.set_ylabel('$y$ [arb. un]')
ax.set_xlabel('$x$ [arb. un.]', x=0.9)
ax.grid(color = 'gray', ls = '--', alpha=0.7)
ax.grid(which='minor', c='gray', ls='--', alpha=0.2)
ax.tick_params(direction='in', length=5, width=1., top=True, right=True)
ax.tick_params(which='minor', direction='in', width=1., top=True, right=True)
legend = ax.legend(loc ='best')
if tick:
    ax.set_ylim(2e-5, 3e-3)
    ax.set_xlim(0.4, 0.65)
    ax.xaxis.set_major_locator(plt.MultipleLocator(5e-2))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1e-2))
plt.tight_layout()
plt.show()