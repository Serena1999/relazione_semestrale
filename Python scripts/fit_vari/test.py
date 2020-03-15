# -*- coding: utf-8 -*-
# questo script e' (una bozza di) quello che credo potrebbe essere definitivo.
# qui dentro inseriamo i vari progressi fatti negli altri script (eventualmente
# li richiamiamo)

# SCOPO:
#   - leggere file di dati e corregere le righe sbagliate,
#     i dati corretti sono messi in una cartella temporanea
#   - convertire i dati nelle unità  desiderate
#   - analisi varie (ancora tutto da fare)


# INDICE:
#   - CONFIGURAZIONI: contiene i parametri di configurazione
#   - FUNZIONI: contiene le definizioni di funzioni varie
#   - OPERAZIONI: contiene il corpo dello script!!!


import pylab #PER COMPATIBILITA'!!!!
import numpy as np
numpy = np # così è più facile fare copia e incolla dia vari scripts #PER COMPATIBILITA'!!!!
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm
import os # operazioni su file
import shutil # operazioni su file
from statistics import * # questo penso che non serva ma da chiedere a Serena

#================================================================
#                          CONFIGURAZIONI
#================================================================
# Variables that control the script
fit = True # attempt to fit the data
log = True # semilog-scale y axis
tick = False # manually choose spacing between axis ticks
tex = False # LaTeX typesetting maths and descriptions

Nstep = 20
# i dati filtrati sono messi in questa cartella temporanea
tmp_folder = "tmp/"

# file di dati (da modificare)
data_folder = "data/"
data_files = [
    "dati_220k.txt",
    "dati_22k.txt",
    "dati_2.2k.txt",
    "dati_220.txt",
    "dati_22.txt",
    "dati_2.2.txt",
    "dati_0.22.txt"
    ]
Nruns = len(data_files) # numero di files (runs)

# valori resistenze (da modificare)
Rs = np.array([
    200e3,
    22e3,
    2.2e3,
    220.,
    22.,
    2.2,
    0.22
    ])
dRs = np.array([
    10e3,
    1e3,
    0.1e3,
    10.,
    1.,
    0.1,
    0.01
    ])


# calibrazione ADC
# NOTA: valori di test

#================================================================
#                             FUNZIONI
#================================================================
# TODO: non trovo lo script per le calibrazioni
# In ../../sketches/teensy_definitivo/pylineare.py oppure ../scatter_plot.py
# ricavano il fattore da fit lineari e hanno funzioni di conversione digit->V 

# ADC02Voltage prende le letture (in ADC) e le converte in Volt
# secondo la calibrazione eseguita
# parametri:
#   - ADCvalue è la lettura da convertire
#   - ADCstd (opzionale) è la deviazione standard (campione) della lettura
# return
#   - il valore centrale (Volt)
#   - errore (Volt)
#TODO: sostituire con la vera funzione di calibrazione
# costante di calibrazione temporanea per non stare a cambiare i valori 4 volte
cal_factor = 3.3 / 4095.# OCCHIO ALLE PRECEDENZE!!!
def ADC02Voltage(ADCvalue, ADCstd = 0.):
    return ADCvalue*cal_factor, np.sqrt(ADCstd**2 + 1) * cal_factor

def ADC12Voltage(ADCvalue, ADCstd = 0.):
    return ADCvalue*cal_factor, np.sqrt(ADCstd**2 + 1) * cal_factor

# V2I prende le tensioni e le converte in corrente sapendo la resistenza
# parametri
#   - V tensione (Volt)
#   - R reistenza (Ohm)
#   - dV errore su V (Volt)
#   - dR errore su R (Ohm)
# return
#   - corrente (Ampere)
#   - errore su corrente (Ampere)
def V2I(V, R, dV = 0., dR = 0.):
    return V / R, np.sqrt((dV / R)**2 + (dR * V / R**2)**2)

# gaussian ritorna il valore della gaussiana centrata in mx e sigma = sx
# serve per il metodo di filtraggio dati
# parametri
#   - x
#   - mx centro x
#   - sx sigma x
# return
#   - valore
def gaussian(x, mx, sx):
    return 1. / np.sqrt(2. * np.pi * sx**2) * pylab.exp(-0.5 * (x - mx)**2 / sx**2)

# esegue un fit di ordine 0 dei dati e restituisce media e varianza campione
# in pratica fa una media pesata secondo la gaussiana, si assume che
# var(x) * df/dx << var(y), questa ipotesi non è verificata nei nostri dati
# ma al massimo ci introduce un fattore di scalatura
#
# parametri
#   - x valore di valutazione
#   - xx ascisse dati
#   - yy ordinate dati
#   - dxx sigmax dei dati
# return
#   - media nell'intorno
#   - deviazione standard campione nell'intorno
def order0fit(x, xx, yy, dxx):
    try:
        my = np.zeros(len(x))
        sy = np.zeros(len(x))
        for i in range(len(x)):
            my[i], sy[i] = order0fit_impl(x[i], xx, yy, dxx)
        return my, sy
    except:
        return order0fit_impl(x, xx, yy, dxx)

# implementazione
def order0fit_impl(x, xx, yy, dxx):
    w = gaussian(x, xx, dxx)
    sum_w = sum(w)
    w = w / sum_w

    my = sum(w * yy)
    var_y = sum((yy - my)**2 * w)
    return my, np.sqrt(var_y)

#================================================================
#                            OPERAZIONI
#================================================================

#================================
#     operazioni preliminari
#================================
print("\npreparazione...")

# operazioni con cartelle temporanee
try:
    shutil.rmtree(tmp_folder)#rimuove la cartella tmp eventualmente rimasta
except OSError as e:
    pass;#  NOP

try:
    os.remove(".gitignore") # rimuovi il vecchio gitignore
except OSError as e:
    pass;#  NOP

# il file gitignore serve a dire a github di non caricare online
# la cartella temporanea
gitignoreF = open(".gitignore", 'w')
gitignoreF.write(tmp_folder);
gitignoreF.close();

os.mkdir(tmp_folder)

#================================
#        correzione dati
#================================
print("\nlettura file originali...")

# legge i dati e mette nella cartella temporanea quelli corretti (control.py)
for fName in data_files:
    name = data_folder + fName
    print(name)
    with open(name, 'r') as data_file, open(tmp_folder+fName, 'w') as tmp_file:
        lines = data_file.readlines()
        for ln in lines:
            if len(ln) <= 14:
                tmp_file.write(ln)
                #tmp_file.write('\n')

#================================
#         lettura dati
#================================
print("\nlettura file temporanei...")

# leggi dati ADC0 e ADC1 dalla cartella temporanea

# vettori di vettori delle letture acquisite
ADC0datas = []
ADC1datas = []

# vettori di vettori degli errori delle letture acquisite
ADC0stds = []
ADC1stds = []

for _name in data_files:
    name = tmp_folder + _name
    print(name)
    _x, _y = np.loadtxt(name, unpack = True)
    ADC0datas.append(_x);
    ADC1datas.append(_y);

    # grossolani, eventualmente da modificare/togliere
    ADC0stds.append(_x * 0. + 4.);
    ADC1stds.append(_y * 0. + 4.);

# converte le liste? in array numpy per comodità
ADC0datas = np.array(ADC0datas)
ADC1datas = np.array(ADC1datas)
ADC0stds = np.array(ADC0stds)
ADC1stds = np.array(ADC1stds)

# elimina i dati senza senso
print("\nelimina dati errati...")
for i in range(Nruns):
    j = 0
    while(j < len(ADC0datas[i])):
        if ((ADC0datas[i][j] > 4095) or (ADC0datas[i][j] < -4095) or
            (ADC1datas[i][j] > 4095) or (ADC1datas[i][j] < -4095)):
            ADC0datas[i] = np.delete(ADC0datas[i], j)
            ADC1datas[i] = np.delete(ADC1datas[i], j)
            ADC0stds[i] = np.delete(ADC0stds[i], j)
            ADC1stds[i] = np.delete(ADC1stds[i], j)
        else:
            j = j + 1;

# questo è quello che c'era prima, in teoria basta un solo indice, così siamo
# sicuri di non saltare nessun dato
#for i in range(Nruns):
#    j = 0
#    k = 0
#    while(k < len(ADC0datas[i])):
#        # se un numero \`e maggiore di 4095, allora elimina la coppia
#        if ((ADC0datas[i][j] > 4095) or (ADC0datas[i][j] < -4095) or
#            (ADC1datas[i][j] > 4095) or (ADC1datas[i][j] < -4095)):
#            ADC0datas[i] = np.delete(ADC0datas[i], j)
#            ADC1datas[i] = np.delete(ADC1datas[i], j)
#            ADC0stds[i] = np.delete(ADC0stds[i], j)
#            ADC1stds[i] = np.delete(ADC1stds[i], j)
#            j = j - 1
#        j = j +1
#        k = k + 1

#================================
#          conversioni
#================================
print("\nconversioni...")

# valori convertiti da ADC in Volt
voltages0s = []
voltages1s = []
voltages0stds = []# errori
voltages1stds = []
for i in range(Nruns):
    _vs, _stds = ADC02Voltage(ADC0datas[i], ADC0stds[i])
    voltages0s.append(_vs)
    voltages0stds.append(_stds)
    _vs, _stds = ADC12Voltage(ADC1datas[i], ADC1stds[i])
    voltages1s.append(_vs)
    voltages1stds.append(_stds)

voltages0s = np.array(voltages0s)
voltages1s = np.array(voltages1s)
voltages0stds = np.array(voltages0stds)
voltages1stds = np.array(voltages1stds)

# valori convertiti da Volt in valori utilizzabili nei dati
voltages = voltages0s
voltageStds = voltages0stds
currents = []
currentStds = []
for i in range(Nruns):
    _I, _dI = V2I(voltages1s[i], Rs[i], voltages1stds[i], dRs[i])
    currents.append(_I)
    currentStds.append(_dI)
    
currents = np.array(currents)
currentStds = np.array(currentStds)

# NOTA: da qui in poi sono solo test a caso, il programma dovrà  continuare..
# Imposto una soglia di deviazioni std dalla media oltre cui escludo i dati
for c in currents:
    print(len(c))

fig, ax = plt.subplots()
Nskip = 150
thr = 1.1
for i in range(Nruns):
    mean, std = norm.fit(currents[i][0::Nskip])
    if abs((currents[i][0::Nskip] - mean)/currentStds[i][0::Nskip]).any() < thr:
    #disegna un punto ogni Nskip, solo per vedere come sono fatti i dati
        ax.errorbar(voltages[i][0::Nskip], currents[i][0::Nskip],
                     currentStds[i][0::Nskip], voltageStds[i][0::Nskip],
                     '.', ls='', elinewidth=1, capsize= 1)
        ls = np.linspace(min(voltages[i]), max(voltages[i]), 100)
        py, spy = order0fit(ls, voltages[i], currents[i], voltageStds[i])
        #ax.plot(ls, py) # test
        #ax.plot(ls, py + spy)
        #ax.plot(ls, py - spy)
if log:
    ax.semilogy()
    tick = False
if tex:
    import matplotlib as mpl
    mpl.rcParams['text.usetex'] = True
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}'] #\text command
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

ax.grid(color ='gray', ls = '--', alpha=0.7)
ax.tick_params(direction='in', length=5, width=1., top=True, right=True)
ax.tick_params(which='minor', direction='in', width=1., top=True, right=True)
ax.set_ylabel('Intensit\`a di Corrente $I$ [A]')    
ax.set_xlabel('Differenza di Potenziale $\Delta V$ [V]', x=0.8)
plt.minorticks_on()
if tick:
    ax.yaxis.set_major_locator(plt.MultipleLocator(1e-1))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(2e-2))
    ax.xaxis.set_major_locator(plt.MultipleLocator(1e-2))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(2e-3))
plt.show()

# Fit con Gaussiana: restituisce mu e sigma di best fit per un insieme di dati
mean, std = norm.fit(currents[0])
#================================
#             END
#================================

shutil.rmtree(tmp_folder) # rimuove la cartella temporanea
