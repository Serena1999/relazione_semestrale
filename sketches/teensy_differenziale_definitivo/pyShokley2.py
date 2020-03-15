
####PROVA STUPIDA---FORSE RISOLVO TRA UN ATTIMO

import pylab
import numpy
import math
from scipy.optimize import curve_fit
from statistics import *


#restituisce la ddp ai capi del diodo
def legge(x, I0, a, Rd, c, b):
    return a*pylab.log((x/I0)+b)+(x-c)*Rd
#b = c/I0 + 1.
#x, y = pylab.loadtxt("dati_convertiti.txt", unpack = True)

##DA CANCELLARE:
x, y = pylab.loadtxt("dati.txt", unpack = True)
##
#ERRORI A CASO
dx = 1.+numpy.zeros(len(x))
dy = 1.+numpy.zeros(len(y))
#dx = numpy.zeros(len(x))
#dy = numpy.zeros(len(x))


dx = dx*3.3/4095.
dy = dy*3.3/(4095.*10000)

pylab.errorbar(x*3.3/4095., y*3.3/(4095.*10000), dy, dx, marker = '.', linestyle = '')
#pylab.errorbar(x, y, dy, dx, marker = '.', linestyle = '')
pylab.show()


print("\n GRAFICO:")

x = x*3.3/4095.
y = y*3.3/(4095.*10000)

gridsize = (3, 1)
grafico1 = g1 = pylab.subplot2grid(gridsize,(0,0),colspan = 1, rowspan = 2)
grafico2 = g2 = pylab.subplot2grid(gridsize,(2,0), colspan = 2)
g1.errorbar(x, y, dy, dx, linestyle = '', color = 'black', marker = '.')
init = [1./10**8, 52/10**3, 1., 0., 1.]
#init = [1./10**8, 52/10**3, 1., 0., - min(y) + 1.]
popt, pcov = curve_fit(legge, y, x, init, dx, absolute_sigma = False)
a1, a2, a3, a4, a5 = popt
da1, da2, da3, da4, da5 = pylab.sqrt(pcov.diagonal())
print("I0 = %f +- %f" %(a1, da1))
print("a = %f +- %f" %(a2, da2))
print("Rd = %f +- %f" %(a3, da3))
print("c = %f +- %f" %(a4, da4))
print("b = %f +- %f" %(a5, da5))
dw = numpy.zeros(len(y))
for i in range(50):
    for i in range(len(y)):
        dw[i] = pylab.sqrt(((a2*dy[i]*(a1/(y[i]+a1 + a5*a1)))+a3*dy[i])**2 + (dx[i])**2)
    popt, pcov = curve_fit(legge, y, x, init, dw, absolute_sigma = False)
    a1, a2, a3, a4, a5 = popt
    da1, da2, da3, da4, da5 = pylab.sqrt(pcov.diagonal())
print("I0 = %f +- %f" %(a1, da1))
print("a = %f +- %f" %(a2, da2))
print("Rd = %f +- %f" %(a3, da3))
print("c = %f +- %f" %(a4, da4))
print("b = %f +- %f" %(a5, da5))
bucket = numpy.linspace(1./1000000, max(y)+0.01, 1000)
ascisse = legge(bucket, *popt)
g1.plot(ascisse, bucket, color = 'red')

g1.minorticks_on()
g1.set_title("Grafico")#da cambiare
g1.set_xlabel("ddp [V]")#vedi se devi cambiare ordine di grandezza
g1.set_ylabel("I [A]")#vedi se devi cambiare ordine di grandezza
g1.grid(color = "gray")
g1.grid(b=True, which='major', color='#666666', linestyle='-')
g1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
currXlim = [min(x)-0.01, max(x)+0.01]
g1.set_xlim(currXlim[0], currXlim[1])
currYlim = [min(y), max(y)]
g1.set_ylim(currYlim[0], currYlim[1])


residui =  numpy.zeros(len(x))
for i in range(len(x)):
    residui[i] = x[i] - legge(y[i], *popt)

g2.minorticks_on()
g2.plot(bucket, bucket*0., color = 'black')
g2.errorbar(y, residui, dw, color = 'black', marker = '.', linestyle = '')
g2.set_xlabel("ddp [V]")
g2.set_ylabel("Residui [A]")
g2.grid(color = "gray")
g2.grid(b=True, which='major', color='#666666', linestyle='-')
g2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
g2.set_xlim(currXlim[0], currXlim[1])
chi_aspettato = len(x) - len(popt)
chi = ((residui**2)/dw**2).sum()
print("chi aspettato = %f" % chi_aspettato)
print("chi calcolato = %f" %chi)
pylab.show()


print("\n GRAFICO in carta semilogaritmica:")

gridsize = (3, 1)
pylab.errorbar(x, y, dy, dx, linestyle = '', color = 'black', marker = '.')

bucket = numpy.logspace(0.01, max(y)+0.01, 1000)
ascisse = legge(bucket, *popt)
pylab.plot(ascisse, bucket, color = 'red')

pylab.minorticks_on()
pylab.title("Grafico in scala semilogaritmica")#da cambiare
pylab.xlabel("ddp [V]")#vedi se devi cambiare ordine di grandezza
pylab.ylabel("I [A]")#vedi se devi cambiare ordine di grandezza
pylab.grid(color = "gray")
pylab.grid(b=True, which='major', color='#666666', linestyle='-')
pylab.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
currXlim = [min(x)-0.01, max(x)+0.01]
pylab.xlim(currXlim[0], currXlim[1])
currYlim = [min(y)-0.1, max(y)+0.1]
pylab.ylim(currYlim[0], currYlim[1])

pylab.semilogy()
pylab.show()
