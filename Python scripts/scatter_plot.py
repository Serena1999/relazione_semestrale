# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 21:58:22 2020

@author: berni
"""
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.misc import derivative
import glob

# Estrazione e stampa a schermo delle medie delle misure di x
Dir= '../data_did/'
Dir_e='../teensy_differenziale_definitivo/'
ddpfiles = glob.glob(Dir+'e_8 data/avgdevs/*txt')
def digitddp():
    x=[]
    dx=[]
    for f in ddpfiles:
        #print(f)
        D = np.loadtxt(f, unpack = True, usecols=0)
        n = len(D)
        av = np.mean(D)
        dev = np.std(D, ddof=1)/np.sqrt(n)
        x.append(av)
        dx.append(dev)
        print('X = %f +- %f ' %(av, dev))
    return x, dx
''' Variables that control the script '''
DSO = False # Sampling from Digital Oscilloscope
fit = True # attempt to fit the data
log = False # log-scale axis/es
tick = True # manually choose spacing between axis ticks
tex = True # LaTeX typesetting maths and descriptions
# Extrazione dei vettori di dati grezzi
V2, dV2, V1, dV1 = np.loadtxt(Dir_e+'file.txt', unpack = True, usecols=(0,1,2,4))
if DSO:
    V1, V2 = np.genfromtxt(Dir+'e_8 data/FAT_32.csv', float, delimiter=',',
                     skip_header = 2, usecols=(0, 1), unpack = True)
# Trasformazione dei dati nelle grandezze da fittare
x = V1
dx = np.sqrt(dV1)
y = V2
dy = np.sqrt(dV2)
# Estrazione di un sottointervallo di dati
x_min = -1.
x_max = 1.e5
x1 = x[x>x_min]; sx = x1[x1<x_max];
y1 = y[x>x_min]; sy = y1[x1<x_max];
dx1 = dx[x>x_min]; sdx = dx1[x1<x_max];
dy1 = dy[x>x_min]; sdy = dy1[x1<x_max];
# Fit lineare e con intercetta nulla (slp) per la calibrazione di Teensy
def lin(x, m, q):
    return m*x + q 

def slp(x, s):
    return s*x
# derivata numerica e legge di Shockley
def f_1 (x, pars):
    return derivative(lin, x, dx = 1e-6, n = 1, args = pars);

def sck(V, I0, VT):
    return I0*(np.exp(V/(VT)) -1.)

def conv(x):
    central = lin(x, *popt)
    unc = np.sqrt(pcov[0][0]*x**2 + pcov[1][1] + 2*pcov[0][1]*x)
    print("conv(x) = %.2f +- %.2f" %(central, unc))
    return [central, unc]

def chitest(data, unc, model, ddof=0):
    """ Evaluates Chi-square goodness of fit test for a function, model, to
    a set of data """
    res = data - model
    resnorm = res/unc
    ndof = len(data) - ddof
    chisq = (resnorm**2).sum()
    sigma = (chisq - ndof)/np.sqrt(2*ndof)
    return chisq, ndof, sigma    

#sx, sdx, sy, sdy = np.loadtxt(Dir+'e_8 data/volt_cal.txt', unpack=True)
# Fit lineare di y rispetto a x
if tex:
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
init=(1e-2, 1e-2)
popt, pcov = curve_fit(lin, sx, sy, init, sdy, absolute_sigma=True)
print('Parametri del fit:\n', popt)
print('Matrice di Covarianza:\n', pcov)
m, q = popt
dm, dq = np.sqrt(pcov.diagonal())
print('Coefficiente angolare: %.5f +- %.5f' %(m, dm))
print('Intercetta: %.5f +- %.5f' %(q, dq))
# Test Chi quadro
res = sy - lin(sx, *popt)
resnorm = res/sdy
chisq, ndof, sigma = chitest(sy, sdy, lin(sx, *popt), ddof=len(popt))
print('Chi quadro/ndof = %f/%d [%+.1f]' % (chisq, ndof, sigma))
print('Chi quadro ridotto:', chisq/ndof)
# Covarianza tra m e q
corr = pcov[0][1]/(dm*dq)
corm = np.zeros((2,2))
for i in range(2):
    for j in range (2):
        corm[i][j] = pcov[i][j]/pcov[i][i]
    
print('Covarianza normalizzata:', corr)
print('Matrice di correlazione:\n', corm)

# Compatibilità errori
soglia = 4
max_iter=100
Compatibili = True
deff = sdy
if(np.mean(sdy) > soglia*(np.mean(sdx)*m)):
    Compatibili = False
if(Compatibili):
    for n in range(max_iter):
        popt, pcov = curve_fit(lin, sx, sy, init, deff, absolute_sigma=True)
        m, q = popt
        dm, dq = np.sqrt(pcov.diagonal())
        #m_1 = f_1(sx, popt)
        deff=np.sqrt(deff**2 + (m*sdx)**2)
        print(n, np.mean(deff) - soglia*m)
        if (np.mean(deff) > soglia*m):
            print(deff)
            print('Parametri ottimali:')
            print('m = %f +- %f' % (m, dm))
            print('q = %f +- %f' % (q, dq))
            # Test Chi quadro
            res = sy - lin(sx, *popt)
            resnorm = res/deff
            chisq = (resnorm**2).sum()
            ndof = len(sy) - len(init)
            chirid = chisq/ndof
            sigma = (chisq - ndof)/np.sqrt(2*ndof)
            print('Chi quadro/ndof = %f/%d [%+.1f]' % (chisq, ndof, sigma))
            print('Chi quadro ridotto:', chirid)
            # Covarianza tra q e m
            corr = pcov[0][1]/(dm*dq)
            corm = np.zeros((2,2))
            for i in range(2):
                for j in range (2):
                    corm[i][j] = pcov[i][j]/pcov[i][i]
    
            print('Covarianza normalizzata:', corr)
            print('Matrice di correlazione:\n', corm)
            break

# Plot y vs x
xx = np.linspace(min(sx)-0.3, max(sx)+0.3, 500)
fig1,(ax1, ax2) = plt.subplots(2,1, True, gridspec_kw={'wspace':0.05,
     'hspace':0.05, 'height_ratios': [3, 1]})
if log:
    xx = np.logspace(np.log10(min(sx)), np.log10(max(sx)), len(xx))
    ax1.set_yscale('log')
    ax1.set_xscale('log')
    ax1.minorticks_on()

ax1.set_ylabel('Differenza di potenziale $\Delta V$ [V]')
ax1.grid(color = 'gray', ls = '--', alpha=0.7)
ax1.errorbar(sx, sy, deff, sdx, 'ko', ms=1.2, elinewidth=1, capsize= 1,
             ls='',label='data', zorder=5)
ax1.plot(xx, lin(xx, *popt), c='gray', lw=0.8,
         label='fit $\chi^2 = %.1f/%d$' %(chisq, ndof), zorder=10)
ax1.plot(xx, lin(xx, popt[0]+np.sqrt(pcov[0][0]), popt[1]+np.sqrt(pcov[1][1])),
         'r--', lw=0.8, zorder=10, alpha =0.6)
ax1.plot(xx, lin(xx, popt[0]-np.sqrt(pcov[0][0]), popt[1]-np.sqrt(pcov[1][1])),
         'b--', lw=0.8, zorder=10, alpha =0.6)
if tick:
    ax1.yaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax1.yaxis.set_minor_locator(plt.MultipleLocator(0.1))
    # ax1.set_xlim(min(xx), max(xx))
    # ax1.set_ylim(min(lin(xx, *popt)), max(lin(xx, *popt)))
ax1.tick_params(direction='in', length=5, width=1., top=True, right=True)
ax1.tick_params(which='minor', direction='in', width=1., top=True, right=True)
legend = ax1.legend(loc ='best')

ax2.set_xlabel('Lettura digitalizzata [digit]', x=0.83)
ax2.set_ylabel('Residui')
ax2.axhline(0, c='r', zorder=10)
ax2.errorbar(sx, resnorm, None, None, 'ko', elinewidth=1, capsize=2, ms=2.5,
             ls='--', lw=1., zorder=0)
ax2.grid(color ='gray', ls = '--', alpha=0.7)
if tick:
    ax2.xaxis.set_major_locator(plt.MultipleLocator(5e2))
    ax2.xaxis.set_minor_locator(plt.MultipleLocator(1e2))
    ax2.yaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax2.yaxis.set_minor_locator(plt.MultipleLocator(0.1))
ax2.tick_params(direction='in', length=5, width=1., top=True, right=True)
ax2.tick_params(which='minor', direction='in', width=1., top=True, right=True)

# Fit y vs x con intercetta nulla 
init=(0.005)
pars, covm = curve_fit(slp, sx, sy, init, deff, absolute_sigma=False)
print('Parametri del fit:\n', pars)
print('Matrice di Covarianza:\n', covm)
s = pars
ds = np.sqrt(covm.diagonal())
print('Coefficiente angolare: %.5f +- %.5f' %(s, ds))
# Test Chi quadro senza absolute_sigma
res = sy - slp(sx, *pars)
resnorm = res/deff
chisq, ndof, sigma = chitest(sy, deff, slp(sx, *pars), ddof=1)
print('Chi quadro/ndof = %f/%d [%+.1f]' % (chisq, ndof, sigma))
print('Chi quadro ridotto:', chisq/ndof)

# Plot y vs x con intercetta nulla
fig2,(ax1, ax2) = plt.subplots(2,1, True, gridspec_kw={'wspace':0.05,
     'hspace':0.05, 'height_ratios': [3, 1]})
ax1.set_ylabel('Differenza di potenziale $\Delta V$ [V]')
ax1.grid(color = 'gray', ls = '--', alpha=0.7)
ax1.errorbar(sx, sy, deff, sdx, 'ko', ms=1.2, elinewidth=1, capsize= 1,
             ls='',label='data', zorder=5)
ax1.plot(xx, slp(xx, *pars), c='gray', lw=0.8,
         label='fit $\chi^2 = %.1f/%d$' %(chisq, ndof), zorder=10)
if tick:
    ax1.yaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax1.yaxis.set_minor_locator(plt.MultipleLocator(0.1))
    # ax1.set_xlim(min(xx), max(xx))
    # ax1.set_ylim(min(slp(xx, *pars)), max(slp(xx, *pars)))
ax1.tick_params(direction='in', length=5, width=1., top=True, right=True)
ax1.tick_params(which='minor', direction='in', width=1., top=True, right=True)
legend = ax1.legend(loc ='best')

ax2.set_xlabel('Lettura digitalizzata [digit]', x=0.83)
ax2.set_ylabel('Residui')
ax2.axhline(0, c='r', zorder=10)
ax2.errorbar(sx, resnorm, None, None, 'ko', elinewidth=1, capsize=2, ms=2.5,
             ls='--', lw=1., zorder=0)
ax2.grid(color ='gray', ls = '--', alpha=0.7)
if tick:
    ax2.xaxis.set_major_locator(plt.MultipleLocator(5e2))
    ax2.xaxis.set_minor_locator(plt.MultipleLocator(1e2))
    ax2.yaxis.set_major_locator(plt.MultipleLocator(0.5))
    ax2.yaxis.set_minor_locator(plt.MultipleLocator(0.1))
ax2.tick_params(direction='in', length=5, width=1., top=True, right=True)
ax2.tick_params(which='minor', direction='in', width=1., top=True, right=True)
plt.show()