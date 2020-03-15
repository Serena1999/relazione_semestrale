###4°
import pylab
import numpy
import math
from scipy.optimize import curve_fit
from statistics import *


Nstep = 20
r = 22

def sck(V, I0, nVt):
    return I0*(pylab.exp(V/nVt) - 1)

def errFun(V, V0, I0, nVt, R):
    return sck(V, I0, nVt) + (V - V0)/R

def deriv_errFun(V, I0, nVt, R):
    return I0 / nVt * pylab.exp(V/nVt) + 1./R;
    
def curr(V, I0, nVt, R):
    v = V;
    for i in range(Nstep):
        a = deriv_errFun(v, I0, nVt, R)
        #for j in range(len(a)):
        #    if a[j] == 0:
        #        a[j] = a[j]+ 0.000001
        v = v - errFun(v, V, I0, nVt, R) /a 
    return (V - v)/R;

def ddp(I, nVt, I0, R):
    return nVt*pylab.log((I0+I)/I0) + R*I


x, y = pylab.loadtxt("../data_elaborati/dati_22el.txt", unpack = True)
pylab.errorbar(x*3.3/4095., y*3.3/(4095.*r), marker = '.', linestyle = '')
pylab.show()


print("\n GRAFICO:")

x = x*3.3/4095.
y = y*3.3/(4095.*r)

gridsize = (3, 1)
grafico1 = g1 = pylab.subplot2grid(gridsize,(0,0),colspan = 1, rowspan = 2)
grafico2 = g2 = pylab.subplot2grid(gridsize,(2,0), colspan = 2)
g1.errorbar(x, y, linestyle = '', color = 'black', marker = '.')
init = [1./10**7, 52/10**3, 0.1]
popt, pcov = curve_fit(curr, x, y, init, absolute_sigma = False)
a1, a2, a3= popt
da1, da2, da3= pylab.sqrt(pcov.diagonal())
print("I0 = %.11f +- %.11f" %(a1, da1))
print("nVt = %f +- %f" %(a2, da2))
print("Rd = %f +- %f" %(a3, da3))

bucket = numpy.linspace(1./1000000, max(x)+0.01, 1000)
ordinate = curr(bucket, *popt)
g1.plot(bucket, ordinate, color = 'red')

g1.minorticks_on()
g1.set_title("Grafico")#da cambiare
g1.set_xlabel("ddp [V]")#vedi se devi cambiare ordine di grandezza
g1.set_ylabel("I [A]")#vedi se devi cambiare ordine di grandezza
g1.grid(color = "gray")
g1.grid(b=True, which='major', color='#666666', linestyle='-')
g1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
currXlim = [min(x)-0.01, max(x)+0.01]
#g1.set_xlim(currXlim[0], currXlim[1])
currYlim = [min(y), max(y)]
#g1.set_ylim(currYlim[0], currYlim[1])


residui =  numpy.zeros(len(x))
for i in range(len(x)):
    residui[i] = y[i] - curr(x[i], *popt)

g2.minorticks_on()
g2.plot(bucket, bucket*0., color = 'black')
g2.errorbar(x, residui, color = 'black', marker = '.', linestyle = '')
g2.set_xlabel("ddp [V]")
g2.set_ylabel("Residui [A]")
g2.grid(color = "gray")
g2.grid(b=True, which='major', color='#666666', linestyle='-')
g2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
g2.set_xlim(currXlim[0], currXlim[1])
chi_aspettato = len(x) - len(popt)
#chi = ((residui**2)/dw**2).sum()
print("chi aspettato = %f" % chi_aspettato)
#print("chi calcolato = %f" %chi)
pylab.show()


print("\n GRAFICO in carta semilogaritmica:")

gridsize = (3, 1)
pylab.errorbar(x, y, linestyle = '', color = 'black', marker = '.')

bucket = numpy.linspace(0., max(x)+0.0001, 1000)
ordinate = curr(bucket, *popt)
pylab.plot(bucket, ordinate, color = 'red')

pylab.minorticks_on()
pylab.title("Grafico in scala semilogaritmica")#da cambiare
pylab.xlabel("ddp [V]")#vedi se devi cambiare ordine di grandezza
pylab.ylabel("I [A]")#vedi se devi cambiare ordine di grandezza
pylab.grid(color = "gray")
pylab.grid(b=True, which='major', color='#666666', linestyle='-')
pylab.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
currXlim = [min(x)-0.01, max(x)+0.01]
#pylab.xlim(currXlim[0], currXlim[1])
currYlim = [min(y)-0.1, max(y)+0.1]
#pylab.ylim(currYlim[0], currYlim[1])

pylab.semilogy()
pylab.show()
