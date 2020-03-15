import matplotlib.pyplot as plt
import numpy as np

''' Variables that control the script '''
log = True # log-scale axis/es
tick = True # manually choose spacing between axis ticks
tex = True # LaTeX typesetting maths and descriptions

v, dv, sv, i, di, si = np.loadtxt("file2C.txt", unpack=True)

N = len(v) - 114484# disegna solo l'ultima serie
K = 10#ogni 10 punti

if tex:
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    
fig, ax = plt.subplots()
ax.errorbar(v[N::K], i[N::K], si[N::K], sv[N::K], ls='', marker='.',
            c = 'k', elinewidth = 1, capsize = 1.5, label = 'data')

x, my, sy, smy = np.loadtxt('b.txt', unpack=True)
ax.plot(x, my, lw=1.2, label = r'$\mu_y$', zorder = 10)
ax.fill_between(x, my+smy, my-smy, facecolor='r', alpha=0.5,
                label = r'Var$(\mu_y)$', zorder= 1)

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
    ax.set_ylim(2e-2, 10)
    ax.set_xlim(0.7, 1.05)
    ax.xaxis.set_major_locator(plt.MultipleLocator(5e-2))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1e-2))
plt.tight_layout()
plt.show()