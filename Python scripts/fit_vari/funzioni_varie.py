import pylab

Nstep = 100


def ddp(I, nVt, I0, R):
    return nVt*pylab.log((I0+I)/I0) + R*I

def der_ddp_x(I, nVt, I0, R):
    return nVt/(I0+I) * R

def function(V, nVt, I0, R, x):
    lista = []
    a = max(x)
    minimo = 100000.
    for j in range(len(V)):
        while( a >= min(x)):
            l = (ddp(a, nVt, I0, R))- V[j])**2
            if(l<minimo):
                minimo = l
                ascissa = a  
            a = a - 1./1000
        lista.append(a)
    return numpy.array(lista)




#def corr(V, nVt, I0, R):
#    I = V/R
#    Voltage = ddp(I, nVt, I0, R)
#    for i in range(Nstep):
#        V = V - ddp(I, nVt, I0, R)/
#    return 
