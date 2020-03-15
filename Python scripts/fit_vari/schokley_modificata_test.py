import numpy
import pylab

Nstep = 1000


def sck(V, I0, nVt):
    return I0*(pylab.exp(V/nVt) - 1)

def errFun(V, V0, I0, nVt, R):
    return sck(V, I0, nVt) + (V - V0)/R

def deriv_errFun(V, I0, nVt, R):
    return I0 / nVt * pylab.exp(V/nVt) + 1./R;
    
def curr(V, I0, nVt, R):
    v = V;
    for i in range(Nstep):
        a = deriv_errFun(v, I0, nVt, R)
        v = v - errFun(v, V, I0, nVt, R) /a 
    return (V - v)/R;

def ddp(I, nVt, I0, R):
    return nVt*pylab.log((I0+I)/I0) + R*I

xx = numpy.linspace(0., 2., 10000)
yy = numpy.logspace(-7, 1, 10000)
pylab.plot(xx, curr(xx, 1./10**8, 52./1000, 0.1), color = 'red')
pylab.plot(ddp(yy,  52./1000, 1./10**8, 0.1), yy, color = 'black')
pylab.semilogy()
pylab.show()

# -----------------------------

xx = numpy.linspace(0., 2., 100)
yy = curr(xx, 1./10**8, 52./1000, 0.1)
pylab.plot(xx, yy, color = 'black')
pylab.show()

tt = ddp(xx,  52./1000, 1./10**8, 0.1)
pylab.plot(tt, xx, color = 'black')
pylab.show()
