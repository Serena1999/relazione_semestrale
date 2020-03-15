#================================================================
#                       PROCEDE COL FIT
#================================================================

from filtro import *

if tex:
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
 
print("\n GRAFICO:")
plt.figure(4)
gridsize = (3, 1)
g1 = plt.subplot2grid(gridsize,(0,0),colspan = 1, rowspan = 2)
g2 = plt.subplot2grid(gridsize,(2,0), colspan = 2)

if plot_points:
    if plot_errors:
        g1.errorbar(voltages, currents, currentErrs, voltageErrs,
                    ls = '', c = 'k', marker = '.', alpha=scatterAlpha)
    else:
        g1.errorbar(voltages, currents,
                    ls = '', c = 'k', marker = '.', alpha=scatterAlpha)
if plot_bad_points:
    if plot_errors:
        g1.errorbar(voltages_bad, currents_bad, currentErrs_bad, voltageErrs_bad,
                    ls = '', c = 'orange', marker = '.', alpha=scatterAlpha)
    else:
        g1.errorbar(voltages_bad, currents_bad,
                    ls = '', c = 'k', marker = '.', alpha=scatterAlpha)

if plot_sigma_zone:
    xx = np.linspace(min(voltages), max(voltages), 1000)
    yy, syy = order0fit(xx, voltages, currents, voltageStds)
    g1.fill_between(xx, yy + 2.0*syy, yy - 2.0*syy,
                    c = 'b', alpha = sigma_zone_alpha)
    g1.fill_between(xx, yy + syy, yy - syy,
                    c = 'b', alpha = sigma_zone_alpha)

##FIT   
if offset_fit:
    init = [4.3/10**9, 47.5/10**3, 0.046, 0.0]
else:
    init = [1./10**7, 52/10**3, 0.1]
    
popt, pcov = curve_fit(curr, voltages, currents, init,
                       currentErrs, absolute_sigma = False)
a = popt
da = np.sqrt(pcov.diagonal())
print("I0 = %g +- %g" %(a[0], da[0]))
print("nVt = %g +- %g" %(a[1], da[1]))
print("Rd = %f +- %f" %(a[2], da[2]))
if offset_fit:
    print("offset = %g +- %g" %(a[3], da[3]))

dw = np.zeros(len(currentErrs))
for i in range(iterazioni_fit):
    for j in range(len(currentErrs)):
        dw[j] = np.sqrt(currentErrs[j]**2 +
                        (curr(voltages[j] + voltageErrs[j], *popt) -
                         curr(voltages[j], *popt))**2)
    popt, pcov = curve_fit(curr, voltages, currents, init,
                           dw, absolute_sigma = False)

a = popt
da = np.sqrt(pcov.diagonal())
print("I0 = %g +- %g" %(a[0], da[0]))
print("nVt = %g +- %g" %(a[1], da[1]))
print("Rd = %f +- %f" %(a[2], da[2]))
if offset_fit:
    print("offset = %g +- %g" %(a[3], da[3]))

residui =  np.zeros(len(voltages))
for i in range(len(voltages)):
    residui[i] = currents[i] - curr(voltages[i], *popt)

ndof = len(voltages) - len(popt)
chi = ((residui/dw)**2).sum()
print("chi atteso = %f" % ndof)
print("chi calcolato = %f" %chi)

# Covarianza tra i parametri
corr_I0nVt = pcov[0][1]/(da[0]*da[1])
corr_I0Rd = pcov[0][2]/(da[0]*da[2])
corr_nVtRd = pcov[1][2]/(da[1]*da[2])
if offset_fit:
    corr_I0oft = pcov[0][3]/(da[0]*da[3])
    corr_nVtoft = pcov[1][3]/(da[1]*da[3])
    corr_Rdoft = pcov[2][3]/(da[2]*da[3])
corm = np.zeros_like(pcov)
for i in range(len(popt)):
    for j in range(len(popt)):
        corm[i][j] = pcov[i][j]/pcov[i][i]
    
print('Covarianza normalizzata I0nVt:', corr_I0nVt)
print('Covarianza normalizzata I0Rd:', corr_I0Rd)
print('Covarianza normalizzata nVtRd', corr_nVtRd)
if offset_fit:
    print('Covarianza normalizzata I0oft:', corr_I0oft)
    print('Covarianza normalizzata nVtoft:', corr_nVtoft)
    print('Covarianza normalizzata Rdoft:', corr_Rdoft)
print('Matrice di correlazione:\n', corm)

## GRAFICI
bucket = np.linspace(1e-6, max(voltages)+0.01, 1000)
ordinate = curr(bucket, *popt)
g1.plot(bucket, ordinate, c = 'r', lw = 1, zorder = 10)

g1.minorticks_on()
if tick:
    g1.yaxis.set_major_locator(plt.MultipleLocator(1))
    g1.yaxis.set_minor_locator(plt.MultipleLocator(0.2))
    g1.xaxis.set_major_locator(plt.MultipleLocator(0.1))
    g1.xaxis.set_minor_locator(plt.MultipleLocator(2e-2))
    g1.xaxis.set_major_formatter(plt.NullFormatter())
    g1.xaxis.set_minor_formatter(plt.NullFormatter())
g1.tick_params(direction='in', length=5, width=1., top=True, right=True)
g1.tick_params(which='minor', direction='in', width=1., top=True, right=True)
# g1.set_title("Corrente vs tensione")
#g1.set_xlabel("d.d.p. [V]", x=0.9)#vedi se devi cambiare ordine di grandezza
g1.set_ylabel("Intensità di Corrente $I$ [A]")#vedi se devi cambiare ordine di grandezza
g1.grid(b=True, which='major', c='#666666', ls='--', alpha = 0.7)
#g1.grid(b=True, which='minor', c='#999999', ls='--', alpha=0.2)
currXlim = [min(voltages), max(voltages)+0.01]
g1.set_xlim(currXlim[0], currXlim[1])
currYlim = [min(currents), max(currents)]
#g1.set_ylim(currYlim[0], currYlim[1])

g2.minorticks_on()
g2.tick_params(direction='in', length=5, width=1., top=True, right=True)
g2.tick_params(which='minor', direction='in', width=1., top=True, right=True)
if tick:
    g2.xaxis.set_major_locator(plt.MultipleLocator(0.1))
    g2.xaxis.set_minor_locator(plt.MultipleLocator(2e-2))
    g2.yaxis.set_major_locator(plt.MultipleLocator(2))
    g2.yaxis.set_minor_locator(plt.MultipleLocator(0.5))
    plt.tight_layout(h_pad=1)
    
g2.axhline(0, c = 'r', alpha=0.7, zorder=10)

g2.errorbar(voltages, residui / dw, c = 'k', marker = '.',
            ls = '', alpha=scatterAlpha)
#g2.set_ylim(-3, 3)

if plot_sigma_zone:
    xx = np.linspace(min([min(voltages), min(voltages_bad)]),
                     max(voltages), 1000)
    yy, syy = order0fit(xx, voltages, currents, voltageStds)
    g2.fill_between(xx, yy + 2.0*syy - curr(xx, *popt),
                    yy - 2.0*syy - curr(xx, *popt), c = 'b',
                    alpha = sigma_zone_alpha)
    g2.fill_between(xx, yy + syy - curr(xx, *popt),
                    yy - syy - curr(xx, *popt), c = 'b',
                    alpha = sigma_zone_alpha)
g2.set_xlabel("d.d.p. [V]", x=0.9)
g2.set_ylabel("Residui normalizzati")
g2.grid(b=True, which='major', c='#666666', ls='--', alpha = 0.7)
#g2.grid(b=True, which='minor', c='#999999', ls='--', alpha=0.2)
g2.set_xlim(currXlim[0], currXlim[1])


print("\n GRAFICO in scala semilogaritmica:")
plt.figure(5)
bucket = np.linspace(0.2, max(voltages)+0.0001, 1000)
ordinate = curr(bucket, *popt)

if offset_fit:
    p_offset = a[3]
else:
    p_offset = 0

if plot_points:
    if plot_errors:
        plt.errorbar(voltages, currents - p_offset, currentErrs, voltageErrs,
                       ls = '', c = 'k', marker = '.', alpha=scatterAlpha)
    else:
        plt.errorbar(voltages, currents - p_offset,
                       ls = '', c = 'k', marker = '.', alpha=scatterAlpha)
        
if plot_bad_points:
    if plot_errors:
        plt.errorbar(voltages_bad, currents_bad - p_offset, currentErrs_bad,
                       voltageErrs_bad, ls = '', c = 'orange', marker = '.',
                       alpha=scatterAlpha)
    else:
        plt.errorbar(voltages_bad, currents_bad - p_offset,
                       ls = '', c = 'r', marker = '.', alpha=scatterAlpha)

if plot_sigma_zone:
    xx = np.linspace(min(voltages), max(voltages), 1000)
    yy, syy = order0fit(xx, voltages, currents, voltageStds)
    plt.fill_between(xx, yy + 2.0*syy, yy - 2.0*syy,
                       c = 'b', alpha = sigma_zone_alpha)
    plt.fill_between(xx, yy + syy, yy - syy,
                       c = 'b', alpha = sigma_zone_alpha)

plt.plot(bucket, ordinate - p_offset, c = 'r', lw=1, zorder = 10)

ax = plt.gca()
ax.set_yscale('log')
ax.minorticks_on()
ax.tick_params(direction='in', length=5, width=1., top=True, right=True)
ax.tick_params(which='minor', direction='in', width=1., top=True, right=True)
#ax.set_title("Grafico in scala semilogaritmica")#da cambiare
ax.set_xlabel("d.d.p. [V]", x=0.9)#vedi se devi cambiare ordine di grandezza
ax.set_ylabel("Intensità di Corrente $I$ [A]")#vedi se devi cambiare ordine di grandezza
ax.grid(b=True, which='major', c='#666666', ls='--')
ax.grid(b=True, which='minor', c='#999999', ls='--', alpha=0.2)
if plot_bad_points:
    currXlim = [min([min(voltages), min(voltages_bad)]), max(voltages)+0.01]
else:
    currXlim = [0.2, max(voltages)+0.01]
ax.set_xlim(currXlim[0], currXlim[1])
currYlim = [min(currents)-0.1, max(currents)+0.1]
#plt.ylim(currYlim[0], currYlim[1])
if tick:
    ax.xaxis.set_major_locator(plt.MultipleLocator(0.1))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(2e-2))
    ax.yaxis.set_major_locator(plt.LogLocator(numticks=16))
    ax.yaxis.set_minor_locator(plt.LogLocator(subs=np.arange(2, 10)*.1,
                                              numticks = 16))
    ax.xaxis.set_minor_formatter(plt.NullFormatter())
    plt.tight_layout()
plt.show()