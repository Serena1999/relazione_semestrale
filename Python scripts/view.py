import pylab 

Directory = '../data_did'
FileName = Directory+ 'dati_sincronizzato.txt'

x,y = pylab.loadtxt(FileName,unpack='True')

pylab.errorbar(x,y,linestyle='', marker = '.')

pylab.show()
