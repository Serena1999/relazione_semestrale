import pylab 

Directory='' 
FileName=(Directory+'dati.txt') 

x,y = pylab.loadtxt(FileName,unpack='True')

pylab.errorbar(x,y,linestyle='', marker = '.')

pylab.show()
