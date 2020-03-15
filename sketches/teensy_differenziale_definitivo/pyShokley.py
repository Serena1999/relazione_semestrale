
####PER ORA FA SCHIFO---FORSE RISOLVO TRA UN ATTIMO

import pylab
import numpy
import math
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from statistics import *


#restituisce la ddp ai capi del diodo
def legge(x, I0, a, Rd, c):
    return a*numpy.log((x-c+I0)/I0)+(x-c)*Rd

x, y = numpy.loadtxt("../data_elaborati/dati_0.22_1el.txt", unpack = True)
t = []
v = []
for i in range(len(x)):
    if(y[i]>0):
       t.append(x[i])
       v.append(y[i])
       
t = numpy.array(t)
v = numpy.array(v)

x = t
y = v

##DA CANCELLARE:
#x, y = pylab.loadtxt("dati.txt", unpack = True)
##
#ERRORI A CASO
dx = 1.+numpy.zeros(len(x))
dy = 1.+numpy.zeros(len(y))
#dx = numpy.zeros(len(x))
#dy = numpy.zeros(len(x))


dx = dx*3.3/4095.*0
dy = dy*3.3/(4095.*0.22)*0


plt.errorbar(x*3.3/4095., y*3.3/(4095.*0.22), dy, dx, marker = '.', linestyle = '')
#plt.errorbar(x, y, dy, dx, marker = '.', linestyle = '')
plt.show()


print("\n GRAFICO:")

x = x*3.3/4095.
y = y*3.3/(4095.*0.22)

gridsize = (3, 1)
grafico1 = g1 = plt.subplot2grid(gridsize,(0,0),colspan = 1, rowspan = 2)
grafico2 = g2 = plt.subplot2grid(gridsize,(2,0), colspan = 2)
g1.errorbar(x, y, dy, dx, linestyle = '', color = 'black', marker = '.')
init = [1./10**8, 52/10**3, 1., 0.]
popt, pcov = curve_fit(legge, y, x, init, dx, absolute_sigma = False)
a1, a2, a3, a4 = popt
da1, da2, da3, da4 = numpy.sqrt(pcov.diagonal())
print("I0 = %f +- %f" %(a1, da1))
print("a = %f +- %f" %(a2, da2))
print("Rd = %f +- %f" %(a3, da3))
print("c = %f +- %f" %(a4, da4))
dw = numpy.zeros(len(y))
for i in range(50):
    for i in range(len(y)):
        dw[i] = numpy.sqrt(((a2*dy[i]/(y[i]+a1))+a3*dy[i])**2 + (dx[i])**2)
    popt, pcov = curve_fit(legge, y, x, init, dw, absolute_sigma = False)
    a1, a2, a3, a4 = popt
    da1, da2, da3, da4 = numpy.sqrt(pcov.diagonal())
print("I0 = %f +- %f" %(a1, da1))
print("a = %f +- %f" %(a2, da2))
print("Rd = %f +- %f" %(a3, da3))
print("c = %f +- %f" %(a4, da4))

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
plt.show()


print("\n GRAFICO in carta semilogaritmica:")

gridsize = (3, 1)
plt.errorbar(x, y, dy, dx, linestyle = '', color = 'black', marker = '.')

bucket = numpy.logspace(0.01, max(y)+0.01, 1000)
ascisse = legge(bucket, *popt)
#plt.plot(ascisse, bucket, color = 'red')

plt.minorticks_on()
plt.title("Grafico in scala semilogaritmica")#da cambiare
plt.xlabel("ddp [V]")#vedi se devi cambiare ordine di grandezza
plt.ylabel("I [A]")#vedi se devi cambiare ordine di grandezza
plt.grid(color = "gray")
plt.grid(b=True, which='major', color='#666666', linestyle='-')
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
currXlim = [min(x)-0.01, max(x)+0.01]
#plt.xlim(currXlim[0], currXlim[1])
currYlim = [min(y)-0.1, max(y)+0.1]
#plt.ylim(currYlim[0], currYlim[1])

plt.semilogy()
plt.show()