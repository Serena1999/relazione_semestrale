import serial 
import time 

Dir = '../data_did/'
fName = 'dati_0.22_1.txt'
outFile = open(Dir + fName, "w" ) 

# apre porta seriale (occhio alla sintassi, dipende
# dal sistema operativo!)
#ard = serial.Serial('/dev/ttyACM0',19200)
ard = serial.Serial('COM11',9600)

print('Start Acquisition') # scrive sulla console (terminale)
time.sleep(2)
ard.write(b'e')
time.sleep(2)
ard.write(b'r')
time.sleep(2)
# Sintassi veloce accesso file, a fine indentazione li chiude automaticamente
with open(Dir + fName, "w",) as outFile:
    while(1):
        line = ard.readline()[:-2]
        line = line.decode()
        print("%s\n" % line)
        
    while(line != "#E"):    
        line = ard.readline()[:-2] # legge il dato e lo decodifica
        line = line.decode()
        outFile.write(line + '\n') # scrive i dati sul file
        print("%s\n" % line)

ard.close() # chiude la comunicazione seriale con Arduino
print('end') # scrive sulla console che ha finito
