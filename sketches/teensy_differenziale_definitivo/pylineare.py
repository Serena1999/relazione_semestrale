# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

y, dy, x, media_camp1, dx, t, media_camp2, dt = np.loadtxt("file.txt", unpack = True)

def legge(x, a, b):
    return a*x + b

def legge_error(value, a, b, c):
    return np.sqrt(a*value**2 + b + 2*c*value)
#a = pcov[0][0] 
#b = pcov[1][1]
#c = pcov[0][1]

def leggesumerror(x, a, b, c, d, f):
    return legge(x, a, b) + legge_error(x, c, d, f)

def leggedifferror(x, a, b, c, d, f):
    return legge(x, a, b) - legge_error(x, c, d, f)

def leggedifferror_model(x, a, b, c, d, f ):
    return legge(x, a, b) - np.sqrt(legge_error(x, c, d, f)**2 + (legge(x, a, b)*(0.7/100))**2)


def leggesumerror_model(x, a, b, c, d,f ):
    return legge(x, a, b) + np.sqrt(legge_error(x, c, d, f)**2 + (legge(x, a, b)*(0.7/100))**2)



##ADC0

dx = media_camp1
dt = media_camp2

plt.errorbar(x, y, dy, dx, marker = '.', linestyle = '')
plt.show()

print("\n GRAFICO con coefficiente angolare libero:")

gridsize = (3, 1)
g1 = plt.subplot2grid(gridsize,(0,0),colspan = 1, rowspan = 2)
g2 = plt.subplot2grid(gridsize,(2,0), colspan = 2)
g1.errorbar(x, y, dy, dx, linestyle = '', color = 'black', marker = '.')
init = [-1., 10.]
popt, pcov = curve_fit(legge, x, y, init, dy, absolute_sigma = False)
a1, a2 = popt
da1, da2 = np.sqrt(pcov.diagonal())
print("m = %f +- %f" %(a1, da1))
print("intercetta = %f +- %f" %(a2, da2))
dw = np.zeros(len(y))
for i in range(50):
    for i in range(len(y)):
        dw[i] = np.sqrt(dy[i]**2 + (a1*dx[i])**2)
    popt, pcov = curve_fit(legge, x, y, init, dw, absolute_sigma = False)
    a1, a2 = popt
    da1, da2 = np.sqrt(pcov.diagonal())
print("m = %f +- %f" %(a1, da1))
print("intercetta = %f +- %f diottrie" %(a2, da2))

bucket = np.linspace(0.01, max(x)+0.01, 1000)
ordinate = legge(bucket, *popt)
g1.plot(bucket, ordinate, color = 'red')

g1.minorticks_on()
g1.set_title("Digit vs Volt")
g1.set_xlabel("1/p [1/m]")
g1.set_ylabel("1/q [1/m]")
g1.grid(color = "gray")
g1.grid(b=True, which='major', color='#666666', linestyle='-')
g1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
currXlim = [min(x)-0.01, max(x)+0.01]
g1.set_xlim(currXlim[0], currXlim[1])
currYlim = [min(y)-0.1, max(y)+0.1]
g1.set_ylim(currYlim[0], currYlim[1])


residui =  np.zeros(len(y))
for i in range(len(y)):
    residui[i] = y[i] - legge(x[i], *popt)

g2.minorticks_on()
g2.plot(bucket, bucket*0., color = 'black')
g2.errorbar(x, residui, dw, color = 'black', marker = '.', linestyle = '')
g2.set_xlabel("??")
g2.set_ylabel("??")
g2.grid(color = "gray")
g2.grid(b=True, which='major', color='#666666', linestyle='-')
g2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
g2.set_xlim(currXlim[0], currXlim[1])
ndof = len(x) - len(popt)
chi = ((residui**2)/dw**2).sum()
print("chi atteso = %f" % ndof)
print("chi test = %f" %chi)
plt.show()

##PREVISIONE

value = 0.
yvalue =legge(value, *popt)
dyvalue = np.sqrt(pcov[0][0] *value**2 + pcov[1][1] + 2*pcov[0][1]*value)

print("yvalue = %f +- %f" %(yvalue, dyvalue))


plt.errorbar(x, y, dy, dx, marker = '.', linestyle = '')
plt.plot(bucket, ordinate, color = 'red')
plt.plot(bucket, leggesumerror(bucket, *popt, pcov[0][0], pcov[1][1], pcov[0][1]), color = 'black')
plt.plot(bucket, leggedifferror(bucket, *popt, pcov[0][0], pcov[1][1], pcov[0][1]), color = 'black')
plt.show()


plt.errorbar(x, y, dy, dx, marker = '.', linestyle = '')
plt.plot(bucket, ordinate, color = 'red')
plt.plot(bucket, leggesumerror(bucket, *popt, pcov[0][0], pcov[1][1], pcov[0][1]), color = 'black')
plt.plot(bucket, leggedifferror(bucket, *popt, pcov[0][0], pcov[1][1], pcov[0][1]), color = 'black')
plt.plot(bucket, leggesumerror_model(bucket, *popt, pcov[0][0], pcov[1][1], pcov[0][1]), color = 'green')
plt.plot(bucket, leggedifferror_model(bucket, *popt, pcov[0][0], pcov[1][1], pcov[0][1]), color = 'green')
plt.show()

matrixADC0 = pcov
parADC0 = popt
print("----------------------")
print("matrixADC0")
print(matrixADC0)
print("parADC0")
print(parADC0)
print("----------------------")


###ADC1
x = t
dx = dt

plt.errorbar(x, y, dy, dx, marker = '.', linestyle = '')
plt.show()

print("\n GRAFICO con coefficiente angolare libero:")

gridsize = (3, 1)
g1 = plt.subplot2grid(gridsize,(0,0),colspan = 1, rowspan = 2)
g2 = plt.subplot2grid(gridsize,(2,0), colspan = 2)
g1.errorbar(x, y, dy, dx, linestyle = '', color = 'black', marker = '.')
init = [-1., 10.]
popt, pcov = curve_fit(legge, x, y, init, dy, absolute_sigma = False)
a1, a2 = popt
da1, da2 = np.sqrt(pcov.diagonal())
print("m = %f +- %f" %(a1, da1))
print("intercetta = %f +- %f" %(a2, da2))
dw = np.zeros(len(y))
for i in range(50):
    for i in range(len(y)):
        dw[i] = np.sqrt(dy[i]**2 + (a1*dx[i])**2)
    popt, pcov = curve_fit(legge, x, y, init, dw, absolute_sigma = False)
    a1, a2 = popt
    da1, da2 = np.sqrt(pcov.diagonal())
print("m = %f +- %f" %(a1, da1))
print("intercetta = %f +- %f diottrie" %(a2, da2))

bucket = np.linspace(0.01, max(x)+0.01, 1000)
ordinate = legge(bucket, *popt)
g1.plot(bucket, ordinate, color = 'red')

g1.minorticks_on()
g1.set_title("Digit vs Volt")
g1.set_xlabel("1/p [1/m]")
g1.set_ylabel("1/q [1/m]")
g1.grid(color = "gray")
g1.grid(b=True, which='major', color='#666666', linestyle='-')
g1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
currXlim = [min(x)-0.01, max(x)+0.01]
g1.set_xlim(currXlim[0], currXlim[1])
currYlim = [min(y)-0.1, max(y)+0.1]
g1.set_ylim(currYlim[0], currYlim[1])


residui =  np.zeros(len(y))
for i in range(len(y)):
    residui[i] = y[i] - legge(x[i], *popt)

g2.minorticks_on()
g2.plot(bucket, bucket*0., color = 'black')
g2.errorbar(x, residui, dw, color = 'black', marker = '.', linestyle = '')
g2.set_xlabel("??")
g2.set_ylabel("??")
g2.grid(color = "gray")
g2.grid(b=True, which='major', color='#666666', linestyle='-')
g2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
g2.set_xlim(currXlim[0], currXlim[1])
ndof = len(x) - len(popt)
chi = ((residui**2)/dw**2).sum()
print("chi atteso = %f" % ndof)
print("chi test = %f" %chi)
plt.show()

##PREVISIONE

value = 0.
yvalue =legge(value, *popt)
dyvalue = np.sqrt(pcov[0][0] *value**2 + pcov[1][1] + 2*pcov[0][1]*value)

print("yvalue = %f +- %f" %(yvalue, dyvalue))


plt.errorbar(x, y, dy, dx, marker = '.', linestyle = '')
plt.plot(bucket, ordinate, color = 'red')
plt.plot(bucket, leggesumerror(bucket, *popt, pcov[0][0], pcov[1][1], pcov[0][1]), color = 'black')
plt.plot(bucket, leggedifferror(bucket, *popt, pcov[0][0], pcov[1][1], pcov[0][1]), color = 'black')
plt.plot(bucket, leggesumerror_model(bucket, *popt, pcov[0][0], pcov[1][1], pcov[0][1]), color = 'green')
plt.plot(bucket, leggedifferror_model(bucket, *popt, pcov[0][0], pcov[1][1], pcov[0][1]), color = 'green')
plt.show()


matrixADC1 = pcov
parADC1 = popt

print("----------------------")
print("matrixADC1")
print(matrixADC1)
print("parADC1")
print(parADC1)
print("----------------------")
