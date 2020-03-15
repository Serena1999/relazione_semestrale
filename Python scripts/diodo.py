# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 12:57:42 2019

@author: berna
"""
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
''' Variables that control the script '''
DSO = False # Sampling from Digital Oscilloscope
fit = True # attempt to fit the data
log = False # log-scale axis/es
tick = False # manually choose spacing between axis ticks
tex = True # LaTeX typesetting maths and descriptions
# Definizione componenti del circuito
R_D = 22.
dR_D = 1.
Xi = 5.00/1023
dXi = 0.25/1023

Dir_e='../data_elaborati/'
V1, V2 = np.loadtxt(Dir_e+'dati_22_1el.txt', unpack=True)
""" Extrazione delle colonne di ddp misurate in digit 
    sull'intervallo selezionato
"""
dV1 = np.full(len(V1), 1)
dV2 = np.full(len(V2), 1)
x_min = -1
x_max = 1.e9
V1l = V1[V1>x_min]; sV1 = V1l[V1l<x_max];
dV1l= dV1[V1>x_min]; sdV1 = dV1l[V1l<x_max];
V2l = V2[V1>x_min]; sV2 = V2l[V1l<x_max];
dV2l= dV1[V1>x_min]; sdV2 = dV2l[V1l<x_max];
# Definizione variabili generali grafico
x = V1*Xi
dx = dV1*Xi
sx=sV1*Xi
sdx = sdV1*Xi
y = (V2*Xi)/R_D
dy = (dV2*Xi + dx)/R_D
sy = (sV2*Xi)/R_D
dV1V2 = np.sqrt((sdV2*Xi)**2 + sdx**2)
sdy = np.sqrt(((np.sqrt((sdV2*Xi)**2 + sdx**2))*R_D)**2 + (dR_D*sy)**2)/R_D**2
sdy*=2

# Legge di Shockley
def sck(V, I0, VT):
    return I0*(np.exp(V/(VT)) -1.)

def inv(I, I0, nVT, r):
    return np.log(I/I0)*nVT + r*I

def chitest(data, unc, model, ddof=0):
    """ Evaluates Chi-square goodness of fit test for a function, model, to
    a set of data """
    res = data - model
    resnorm = res/unc
    ndof = len(data) - ddof
    chisq = (resnorm**2).sum()
    sigma = (chisq - ndof)/np.sqrt(2*ndof)
    return chisq, ndof, sigma    

# Grafico preliminare dati
if tex:
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
init=(2e-9, 0.3)
fig, ax = plt.subplots()
xx = np.linspace(min(sx), max(sx), 500)
if log:
    xx = np.logspace(np.log10(min(sx)), np.log10(max(sx)), len(xx))
    ax.set_yscale('log')
ax.errorbar(sx, sy, sdy, sdx, 'ko', ms=1.2, elinewidth=1, capsize= 1,
        ls='',label='data', zorder=5)
ax.grid(color = 'gray', ls = '--', alpha=0.7)
ax.set_xlabel('x [digit]', x=0.9)
ax.set_ylabel('y [digit]')
ax.minorticks_on()
ax.tick_params(direction='in', length=5, width=1., top=True, right=True)
ax.tick_params(which='minor', direction='in', width=1., top=True, right=True)
if fit:
    ax.plot(xx, sck(xx, *init), 'k--', lw=0.8, zorder=10, alpha =0.6,
            label='initial fit')
legend = ax.legend(loc ='best')
plt.show()

if not fit:
    exit()

# Fit per sck di I rispetto a V
pars, covm = curve_fit(sck, sx, sy, init, sdy, absolute_sigma=False)
print('Parametri del fit:\n', pars)
print('Matrice di Covarianza:\n', covm)
I0, VT = pars
dI0, dVT = np.sqrt(covm.diagonal())
print('I0: %f +- %f' %(I0*1e6, dI0*1e6))
print('VT: %f +- %f' %(VT, dVT))
# Test Chi quadro per sck
res = sy - sck(sx, *pars)
resnorm = res/sdy
chisq, ndof, sigma = chitest(sy, sdy, sck(sx, *pars), ddof=len(pars))
print('Chi quadro/ndof = %f/%d [%+.1f]' % (chisq, ndof, sigma))
print('Chi quadro ridotto:', chisq/ndof)
# Covarianza tra I0 e VT
corr = covm[0][1]/(dI0*dVT)
corm = np.zeros((2,2))
for i in range(2):
    for j in range (2):
        corm[i][j] = covm[i][j]/covm[i][i]
  
print('Covarianza normalizzata:', corr)
print('Matrice di correlazione:\n', corm)
# Compatibilità errori per sck
soglia = 4
max_iter=100
Compatibili = True
if(np.mean(sdy) > soglia*(np.mean(sdx)*np.mean(I0))):
    Compatibili = False
if(Compatibili):
    deff = sdy
    for n in range(max_iter):
        popt, pcov = curve_fit(sck, sx, sy, init, deff, absolute_sigma=False)
        I0, VT = popt
        dI0, dVT = np.sqrt(pcov.diagonal())
        deff = np.sqrt((sdx*I0)**2 + deff**2)
        print(n, np.mean(deff) - soglia*np.mean(sdx*I0))
        if (np.mean(deff) > soglia*np.mean(sdx*I0)):
            print(deff)
            print('Parametri ottimali:')
            print('I0: %.5f +- %.5f' %(I0*1e6, dI0*1e6))
            print('den: %.5f +- %.5f' %(VT, dVT))
            # Test Chi quadro
            res = sy - sck(sx, *popt)
            resnorm = res/deff
            chisq, ndof, sigma = chitest(sy, sdy, sck(sx, *pars),
                                         ddof=len(pars))
            print('Chi quadro/ndof = %f/%d [%+.1f]' % (chisq, ndof, sigma))
            print('Chi quadro ridotto:', chisq/ndof)
            # Covarianza tra I0 e VT
            corr = covm[0][1]/(dI0*dVT)
            corm = np.zeros((2,2))
            for i in range(2):
                for j in range (2):
                    corm[i][j] = covm[i][j]/covm[i][i]
                    
            print('Covarianza normalizzata:', corr)
            print('Matrice di correlazione:\n', corm)
            break
# Plot y vs x
fig1,(ax1, ax2) = plt.subplots(2,1, True, gridspec_kw={'wspace':0.05,
     'hspace':0.05, 'height_ratios': [3, 1]})
xx = np.linspace(min(sx), max(sx), 2000)
if log:
    tick=False
    xx = np.logspace(np.log10(min(x)), np.log10(max(x)), 2000)
    ax1.set_yscale('log')
    ax1.set_xscale('log')
    ax1.minorticks_on()
ax1.grid(color = 'gray', ls = '--', alpha=0.7)
ax1.errorbar(sx, sy, sdy, sdx, 'ko', ms=1.2, elinewidth=1, capsize= 1,
             ls='',label='data', zorder=5)
ax1.plot(xx, sck(xx, *pars), c='gray', lw=0.8,
         label='fit $\chi^2 = %.f/%d$' %(chisq, ndof), zorder=10)
ax1.plot(xx, sck(xx, I0+dI0, VT + dVT), 'r--', lw=0.8, zorder=10, alpha =0.6)
ax1.plot(xx, sck(xx, I0-dI0,  VT-dVT), 'b--', lw=0.8, zorder=10, alpha =0.6)
# ax1.axhline(I0, lw=1.4, ls='--', c='k', alpha=0.7, zorder=1)
ax1.set_ylabel('Intensità di Corrente $I$ [mA]')    
if tick:
    ax1.yaxis.set_major_locator(plt.MultipleLocator(0.2))
    ax1.yaxis.set_minor_locator(plt.MultipleLocator(5e-2))
    # ax1.set_xlim(min(xx), max(xx))
    # ax1.set_ylim(min(sck(xx, *pars)), max(sck(xx, *pars)))
ax1.tick_params(direction='in', length=5, width=1., top=True, right=True)
ax1.tick_params(which='minor', direction='in', width=1., top=True, right=True)
legend = ax1.legend(loc ='best')

ax2.set_xlabel('Differenza di Potenziale $\Delta V$ [mV]', x=0.8)
ax2.set_ylabel('Residui')
ax2.axhline(0, c='r', zorder=10)
ax2.errorbar(sx, resnorm, None, None, 'ko', elinewidth=1, capsize=2, ms=2.5,
             ls='--', lw=1., zorder=0)
ax2.grid(color ='gray', ls = '--', alpha=0.7)
if tick:
    ax2.xaxis.set_major_locator(plt.MultipleLocator(50.))
    ax2.xaxis.set_minor_locator(plt.MultipleLocator(10))
    ax2.yaxis.set_major_locator(plt.MultipleLocator(5))
    ax2.yaxis.set_minor_locator(plt.MultipleLocator(1))
ax2.tick_params(direction='in', length=5, width=1., top=True, right=True)
ax2.tick_params(which='minor', direction='in', width=1., top=True, right=True)

# Fit sinusoide con rimozione degli outliers
TT=np.array([])
VV=np.array([])
dTT=np.array([])
dVV=np.array([])

outT=np.array([])
outV=np.array([])
doutT=np.array([])
doutV=np.array([])
'Contatori in e out liers'
j=0
k=0
#tengo solo i dati che si discostano dal modello per meno
# di 2-3 deviazioni standard
soglia = 2.3
for i in range (len(sy)):
    if (np.abs(sy[i] - sck(sx, *pars)[i])< soglia*sdy[i]): 
        TT=np.insert(TT, j, sx[i])
        dTT=np.insert(dTT, j, sdx[i])
        VV=np.insert(VV, j, sy[i])
        dVV=np.insert(dVV, j, sdy[i])
        j+=1
    else:
        outT=np.insert(outT, k, sx[i])
        doutT=np.insert(doutT, k, sdx[i])
        outV=np.insert(outV, k, sy[i])
        doutV=np.insert(doutV, k, sdy[i])
        k+=1

init= (1.e-7, 2*26)
pars, covm = curve_fit(sck, TT, VV, init, dVV, absolute_sigma = False)
print('Parametri del fit:\n', pars)
print('Matrice di Covarianza:\n', covm)
I0, VT = pars
dI0, dVT = np.sqrt(covm.diagonal())
print('I0: %f +- %.5f' %(I0*1e6, dI0*1e6))
print('VT: %.5f +- %.5f' %(VT, dVT))
# Test Chi quadro per sck
normin = (VV-sck(TT, *pars))/dVV
normout = (outV-sck(outT, *pars))/doutV
chisqin, ndof, sigmain = chitest(VV, dVV, sck(TT, *pars), ddof=len(pars))
print('Chi quadro ridotto:', chisq/ndof)
print('Chi quadro/ndof = %f/%d [%+.1f]' % (chisqin, ndof, sigmain))
# Covarianza tra I0 e VT
corr = covm[0][1]/(dI0*dVT)
corm = np.zeros((2,2))
for i in range(2):
    for j in range (2):
        corm[i][j] = covm[i][j]/covm[i][i]
        
print('Covarianza normalizzata:', corr)
print('Matrice di correlazione:\n', corm)
# Plot DV vs t con outliers
fig2,(ax1, ax2) = plt.subplots(2,1, True, gridspec_kw={'wspace':0.05,
     'hspace':0.05, 'height_ratios': [3, 1]})
if(log):
    ax1.set_yscale('log')
    ax1.minorticks_on()
ax1.errorbar(TT, VV, dVV, dTT, 'ko',  ms=1.5, elinewidth=1.,
             capsize=1.5, ls='', label='data')
ax1.errorbar(outT, outV, doutV, doutT, 'gx',  ms=3, elinewidth=1.,
             capsize=1.5, ls='', label='outliers')
ax1.set_ylabel('Intensità di Corrente $I$ [mA]')    
ax1.grid(which = 'major', color = 'gray', ls = '--', alpha=0.7)
ax1.plot(xx, sck(xx, *pars), c='gray', ls='-',
         label='fit $\chi^2 = %.f/%d$' %(chisqin, ndof), zorder=10, alpha=0.7)
if tick:
    ax1.yaxis.set_major_locator(plt.MultipleLocator(0.2))
    ax1.yaxis.set_minor_locator(plt.MultipleLocator(5e-2))

ax1.tick_params(direction='in', length=5, width=1., top=True, right=True)
ax1.tick_params(which='minor', direction='in', width=1., top=True, right=True)
legend = ax1.legend(loc ='best')

ax2.set_xlabel('Differenza di Potenziale $\Delta V$ [mV]', x=0.8)
ax2.set_ylabel('Residui')
ax2.axhline(0, c='r', alpha=0.7, zorder=10)
ax2.errorbar(TT, normin, None, None, 'ko', elinewidth = 0.5, capsize=0.5,
             ms=1., ls='--', lw=1., zorder=5)
ax2.errorbar(outT, normout, None, None, 'gx', elinewidth = 0.7, capsize=0.7,
             ms=3., ls='--', zorder=5)
ax2.grid(color ='gray', ls = '--', alpha=0.7)
ax2.ticklabel_format(axis='both', style='sci', scilimits=None,
                     useMathText=True)
if tick:
    ax2.xaxis.set_major_locator(plt.MultipleLocator(50))
    ax2.xaxis.set_minor_locator(plt.MultipleLocator(10))
    ax2.yaxis.set_major_locator(plt.MultipleLocator(2))
    ax2.yaxis.set_minor_locator(plt.MultipleLocator(0.5))
    ax2.set_ylim(min(normin)-np.std(normin), max(normin)+np.std(normin))
ax2.tick_params(direction='in', length=5, width=1., top=True, right=True)
ax2.tick_params(which='minor', direction='in', width=1., top=True, right=True)
plt.show()
