from funzioni import *

#================================
#     operazioni preliminari
#================================
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

#================================
#          conversioni
#================================
print("\nconversioni...")

# valori convertiti da ADC in Volt
voltages0s = []
voltages1s = []
voltages0errs = []# errori
voltages1errs = []
voltages0stds = []# dev standard
voltages1stds = []
for i in range(Nruns):
    _vs, _errs, _stds = ADC02Voltage(ADC0datas[i], ADC0stds[i])
    voltages0s.append(_vs)
    voltages0errs.append(_errs)
    voltages0stds.append(_stds)
    _vs, _errs, _stds = ADC12Voltage(ADC1datas[i], ADC1stds[i])
    voltages1s.append(_vs)
    voltages1errs.append(_errs)
    voltages1stds.append(_stds)

voltages0s = np.array(voltages0s)
voltages1s = np.array(voltages1s)
voltages0errs = np.array(voltages0errs)
voltages1errs = np.array(voltages1errs)
voltages0stds = np.array(voltages0stds)
voltages1stds = np.array(voltages1stds)

# valori convertiti da Volt in valori utilizzabili nei dati
voltages = voltages0s
voltageErrs = voltages0errs
voltageStds = voltages0stds
currents = []
currentErrs = []
currentStds = []
for i in range(Nruns):
    _I, _dI, _stdI = V2I(voltages1s[i], Rs[i], voltages1errs[i],
                         voltages1stds[i], dRs[i])
    currents.append(_I)
    currentErrs.append(_dI)
    currentStds.append(_stdI)
    
currents = np.array(currents)
currentErrs = np.array(currentErrs)
currentStds = np.array(currentStds)

shutil.rmtree(tmp_folder) # rimuove la cartella temporanea
