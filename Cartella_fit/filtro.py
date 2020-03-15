#================================================================
#                       CHIAMA L'ESEGUIBILE ESTERNO
#================================================================

from load_data import *

os.mkdir(tmp_folder)
file2C = open(tmp_folder + file2CName, 'w')

file2C.write("#V    errV    stdV    I    errI    stdI\n")

for i in range(len(voltages)):
    for j in range(len(voltages[i])):
        file2C.write("%.20f    %.20f    %.20f    %.20f    %.20f    %.20f\n" \
                     %(voltages[i][j], voltageErrs[i][j], voltageStds[i][j],\
                       currents[i][j], currentErrs[i][j],  currentStds[i][j]))
    file2C.write("#================================")

file2C.close()

import subprocess

subprocess.call("filtro.exe"\
                + " -in " + tmp_folder + file2CName\
                + " -out " + tmp_folder + file2PyName\
                + " -maxRatio " + str(maxRatio)\
                + " -minV " + str(minV)\
                + " -Nskip " + str(filter_Nskip)\
                + " -outSigma " + str(outSigma))

#subprocess.call('filtro.exe -in tmp/file2C.txt -out file2P.txt -maxRatio 3 -minV 0.2')

##per sicurezza, anche se non è strettamente necessario
time.sleep(5)

voltages, voltageErrs, voltageStds, currents,\
          currentErrs, currentStds\
          = np.loadtxt(tmp_folder + file2PyName, unpack = True)

voltages_bad, voltageErrs_bad, voltageStds_bad, currents_bad,\
          currentErrs_bad, currentStds_bad\
          = np.loadtxt(tmp_folder + file2PyName + ".bad", unpack = True)

shutil.rmtree(tmp_folder) # rimuove la cartella temporanea
