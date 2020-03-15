import serial 
import time 
import numpy

Directory = '../data_did'
FileName = Directory+ 'dati_sincronizzato.txt'
outputFile = open(FileName, "w" ) 

# apre porta seriale (occhio alla sintassi, dipende
# dal sistema operativo!)
#ard = serial.Serial('/dev/ttyACM0',19200)
ard = serial.Serial('COM3',9600)

print('Start Acquisition') # scrive sulla console (terminale)
time.sleep(2)
ard.write(b'e')
time.sleep(2)
ard.write(b'r')
time.sleep(2)

while(1):
    line = ard.readline()[:-2]
    line = line.decode()
    print("%s\n" % line)
    if(line == "#R"):
        break
    
while(1):
    line = ard.readline()[:-2] # legge il dato e lo decodifica
    line = line.decode()
    if(line == "#E"):
        break
    outputFile.write(line) # scrive i dati sul file
    outputFile.write("\n")
    print("%s\n" % line)

ard.close() # chiude la comunicazione seriale con Arduino
outputFile.close() # chiude il file dei dati 
print('end') # scrive sulla console che ha finito
