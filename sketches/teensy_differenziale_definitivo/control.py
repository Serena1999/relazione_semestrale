####CONTROLLO
import pylab
import numpy
from matplotlib import pyplot as plt

Dir = '../data_did/'
fName = 'dati_0.22_1.txt'
Dir2 = '../tmp/'
fName2 = 'tmp0.22_1.txt'
Dir3 = '../data_elaborati/'
fName3 ='dati_0.22_1el.txt'

with open(Dir + fName, 'r') as f, open(Dir2 + fName2, 'w') as f2:
    lines = f.readlines()
    for ln in lines:
        if len(ln) <= 14:
            f2.write(ln)
            f2.write("\n")
            
x, y = numpy.loadtxt(Dir2 + fName2, unpack = True)
plt.errorbar(x, y, linestyle = '', marker = '.')
plt.show()

t = []
v = []
for value in x:
    if(value < 4100):
        t.append(value)
        v.append(value)

x = numpy.array(t)
y = numpy.array(v)
plt.errorbar(x, y, linestyle = '', marker = '.')
plt.show()

with open(Dir3 + fName3, 'w',) as f3:
    for i in range(len(x)):
        f3.write("%f    %f\n" % (x[i], y[i]))