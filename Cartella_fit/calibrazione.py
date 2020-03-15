from config import *

y, dy, x, media_camp1, dx, t, media_camp2, dt = np.loadtxt(
    "data_calibrazione/file.txt", unpack = True)

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
    return legge(x, a, b) - np.sqrt(legge_error(x, c, d, f)**2 +
                                    (legge(x, a, b)*(0.7/100))**2)

def leggesumerror_model(x, a, b, c, d,f ):
    return legge(x, a, b) + np.sqrt(legge_error(x, c, d, f)**2 +
                                    (legge(x, a, b)*(0.7/100))**2)

def legge_giusto_error(x, a, b, c, d,f):
    return  np.sqrt(legge_error(x, c, d, f)**2 + (legge(x, a, b)*(0.7/100))**2)


##ADC0
if tex:
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

if (grafici_calibrazione):
    plt.errorbar(x, y, dy, dx, marker = '.', ls = '')
    

print("\n GRAFICO ADC0:")

if(grafici_calibrazione):
    fig0 = plt.figure(0)
    gridsize = (3, 1)
    g1 = plt.subplot2grid(gridsize,(0,0),colspan = 1, rowspan = 2)
    g2 = plt.subplot2grid(gridsize,(2,0), colspan = 2, sharex=g1)
    g1.errorbar(x, y, dy, dx, ls = '', c = 'k', marker = 'o', ms=2.7 ,
                elinewidth=1.5, capsize=2)
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
print("m = %.10f +- %.10f" %(a1, da1))
print("intercetta = %.10f +- %.10f" %(a2, da2))

# Covarianza tra m0 e q0
corr_m0q0 = pcov[0][1]/(da1*da2)
corm = np.zeros((2,2))
for i in range(len(popt)):
    for j in range (len(popt)):
        corm[i][j] = pcov[i][j]/pcov[i][i]
    
print('Covarianza normalizzata ADC0:', corr_m0q0)
print('Matrice di correlazione:\n', corm)

bucket = np.linspace(0.01, max(x)+50, 1000)
ordinate = legge(bucket, *popt)
if(grafici_calibrazione):
    g1.plot(bucket, ordinate, c = 'r', lw=1.2)

if(grafici_calibrazione):
    g1.set_title("Digit vs Volt (\\texttt{ADC0})")
    #g1.set_xlabel("Letture digitali [digit]")
    g1.set_ylabel("Tensione [V]")
    g1.grid(c = "gray")
    g1.grid(b=True, which='major', c='#666666', ls='-')
    g1.grid(b=True, which='minor', c='#999999', ls='-', alpha=0.2)
    currXlim = [min(x), max(x)+50]
    g1.set_xlim(currXlim[0], currXlim[1])
    currYlim = [min(y)-0.1, max(y)+0.1]
    g1.set_ylim(currYlim[0], currYlim[1])
    g1.minorticks_on()
    g1.tick_params(direction='in', length=5, width=1., top=True, right=True)
    g1.tick_params(which='minor', direction='in', width=1., top=True, right=True)
    g1.xaxis.set_major_formatter(plt.NullFormatter())
    g1.xaxis.set_minor_formatter(plt.NullFormatter())
    fig0.tight_layout(h_pad=1)

residui =  y - legge(x, *popt)
resnorm = residui/dw

if(grafici_calibrazione):
    g2.axhline(0, c = 'k')
    g2.errorbar(x, residui*1e3, dw*1e3, c = 'k', marker = '.', ls = '',
                elinewidth=1.5, capsize=2)
    g2.set_xlabel("Letture MCU [digit]", x = 0.85)
    g2.set_ylabel("Residui [mV]")
    g2.grid(c = "gray")
    g2.grid(b=True, which='major', c='#666666', ls='-')
    g2.grid(b=True, which='minor', c='#999999', ls='-', alpha=0.2)
    g2.set_xlim(currXlim[0], currXlim[1])
    g2.minorticks_on()
    g2.tick_params(direction='in', length=5, width=1., top=True, right=True)
    g2.tick_params(which='minor', direction='in', width=1., top=True, right=True)
ndof = len(x) - len(popt)
chi = ((residui**2)/dw**2).sum()
print("chi atteso = %f" % ndof)
print("test chi = %f" %chi)
    

##PREVISIONE

value = 0.
yvalue =legge(value, *popt)
dyvalue = np.sqrt(pcov[0][0] *value**2 + pcov[1][1] + 2*pcov[0][1]*value)

print("yvalue = %f +- %f" %(yvalue, dyvalue))


if (grafici_previsione):
    prev0 = plt.figure(2)
    plt.title("Previsione \\texttt{ADC0}")
    plt.errorbar(x, y, dy, dx, marker = '.', ls = '')
    plt.plot(bucket, ordinate, c = 'r', lw=1.2)
    plt.plot(bucket, leggesumerror(bucket, *popt, pcov[0][0], pcov[1][1],
                                   pcov[0][1]), c = 'k', lw=1.2)
    plt.plot(bucket, leggedifferror(bucket, *popt, pcov[0][0], pcov[1][1],
                                    pcov[0][1]), c = 'k', lw=1.2)
    plt.plot(bucket, leggesumerror_model(bucket, *popt, pcov[0][0],
                                         pcov[1][1], pcov[0][1]), c='g', lw=1.2)
    plt.plot(bucket, leggedifferror_model(bucket, *popt, pcov[0][0],
                                          pcov[1][1], pcov[0][1]), c='g', lw=1.2)
    plt.grid(color ='gray', ls = '--', alpha = 0.7)
    plt.xlabel("Letture MCU [digit]", x = 0.85)
    plt.ylabel("Tensione [V]")
    plt.minorticks_on()
    plt.tick_params(direction='in', length=5, width=1., top=True, right=True)
    plt.tick_params(which='minor', direction='in', width=1., top=True, right=True)

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

print("\n GRAFICO ADC1:")

if(grafici_calibrazione):
    fig1 = plt.figure(1)
    gridsize = (3, 1)
    g1 = plt.subplot2grid(gridsize,(0,0), colspan = 1, rowspan = 2)
    g2 = plt.subplot2grid(gridsize,(2,0), colspan = 2, sharex=g1)
    g1.errorbar(x, y, dy, dx, ls = '', c = 'k', marker = 'o', ms=2.7 ,
                elinewidth=1.5, capsize=2)
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
print("m = %.10f +- %.10f" %(a1, da1))
print("intercetta = %.10f +- %.10f" %(a2, da2))

# Covarianza tra m1 e q1
corr_m1q1 = pcov[0][1]/(da1*da2)
corm = np.zeros((2,2))
for i in range(len(popt)):
    for j in range(len(popt)):
        corm[i][j] = pcov[i][j]/pcov[i][i]
    
print('Covarianza normalizzata ADC1:', corr_m1q1)
print('Matrice di correlazione:\n', corm)

bucket = np.linspace(0., max(x)+50, 1000)
ordinate = legge(bucket, *popt)
if(grafici_calibrazione):
    g1.plot(bucket, ordinate, c = 'r', lw=1.2)
    g1.set_title("Digit vs Volt (\\texttt{ADC1})")
    #g1.set_xlabel("digitized reading [digit]")
    g1.set_ylabel("Tensione [V]")
    g1.grid(c = "gray")
    g1.grid(b=True, which='major', c='#666666', ls='-')
    g1.grid(b=True, which='minor', c='#999999', ls='-', alpha=0.2)
    currXlim = [min(x)+1, max(x)+50]
    g1.set_xlim(currXlim[0], currXlim[1])
    currYlim = [min(y)-0.1, max(y)+0.1]
    g1.set_ylim(currYlim[0], currYlim[1])
    g1.minorticks_on()
    g1.tick_params(direction='in', length=5, width=1., top=True, right=True)
    g1.tick_params(which='minor', direction='in', width=1., top=True, right=True)
    g1.xaxis.set_major_formatter(plt.NullFormatter())
    g1.xaxis.set_minor_formatter(plt.NullFormatter())
    fig1.tight_layout(h_pad=1)


residui =  y - legge(x, *popt)
resnorm = residui/dw

if(grafici_calibrazione):
    g2.plot(bucket, bucket*0., c = 'k')
    g2.errorbar(x, residui*1e3, dw*1e3, c = 'k', marker = '.', ls = '',
                elinewidth=1.5, capsize=2)
    g2.set_xlabel("Letture MCU [digit]", x = 0.85)
    g2.set_ylabel("Residui [mV]")
    g2.grid(c = "gray")
    g2.grid(b=True, which='major', c='#666666', ls='-')
    g2.grid(b=True, which='minor', c='#999999', ls='-', alpha=0.2)
    g2.set_xlim(currXlim[0], currXlim[1])
    g2.minorticks_on()
    g2.tick_params(direction='in', length=5, width=1., top=True, right=True)
    g2.tick_params(which='minor', direction='in', width=1., top=True, right=True)
ndof = len(x) - len(popt)
chi = ((residui**2)/dw**2).sum()
print("chi atteso = %f" % ndof)
print("test chi = %f" %chi)
  
##PREVISIONE

value = 0.
yvalue =legge(value, *popt)
dyvalue = np.sqrt(pcov[0][0] *value**2 + pcov[1][1] + 2*pcov[0][1]*value)

print("yvalue = %f +- %f" %(yvalue, dyvalue))


if (grafici_previsione):
    prev1 = plt.figure(3)
    plt.errorbar(x, y, dy, dx, marker = '.', ls = '')
    plt.plot(bucket, ordinate, c = 'r', lw=1.2)
    plt.plot(bucket, leggesumerror(bucket, *popt, pcov[0][0], pcov[1][1],
                                   pcov[0][1]), c = 'k', lw=1.2)
    plt.plot(bucket, leggedifferror(bucket, *popt, pcov[0][0], pcov[1][1],
                                    pcov[0][1]), c = 'k', lw=1.2)
    plt.plot(bucket, leggesumerror_model(bucket, *popt, pcov[0][0],
                                         pcov[1][1], pcov[0][1]), c='g', lw=1.2)
    plt.plot(bucket, leggedifferror_model(bucket, *popt, pcov[0][0],
                                          pcov[1][1], pcov[0][1]), c='g', lw=1.2)
    plt.grid(color ='gray', ls = '--', alpha = 0.7)
    plt.title("Previsione \\texttt{ADC1}")
    plt.xlabel("Letture MCU [digit]", x = 0.85)
    plt.ylabel("Tensione [V]")
    plt.minorticks_on()
    plt.tick_params(direction='in', length=5, width=1., top=True, right=True)
    plt.tick_params(which='minor', direction='in', width=1., top=True, right=True)

matrixADC1 = pcov
parADC1 = popt

print("----------------------")
print("matrixADC1")
print(matrixADC1)
print("parADC1")
print(parADC1)
print("----------------------")
