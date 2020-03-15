from config import *
from calibrazione import matrixADC1, matrixADC0, parADC1, parADC0, legge, legge_giusto_error


def ADC02Voltage(ADCvalue, ADCstd):
    """ ADC02Voltage prende le letture (in ADC) e le converte in Volt
        secondo la calibrazione eseguita
        parametri:
          - ADCvalue è la lettura da convertire
          - ADCstd (opzionale) è la deviazione standard (campione) della lettura
        return:
          - il valore centrale (Volt)
          - errore (Volt)
          - deviazione standard """
    return legge(ADCvalue, *parADC0),\
           np.sqrt((legge_giusto_error(ADCvalue, *parADC0, matrixADC0[0][0],\
                    matrixADC0[1][1], matrixADC0[0][1]))**2  \
                    +(ADCstd*parADC0[0])**2),\
                    ADCstd * parADC0[0]

def ADC12Voltage(ADCvalue, ADCstd):##cambiare nome?
    """ Analogo di ADC02Voltage per il secondo ADC (1) """
    return legge(ADCvalue, *parADC1),\
           np.sqrt((legge_giusto_error(ADCvalue, *parADC1, matrixADC1[0][0],\
                    matrixADC1[1][1], matrixADC1[0][1]))**2\
                    +(ADCstd*parADC1[1])**2),\
                    ADCstd * parADC1[0]

def V2I(V, R, dV, stdV, dR):
    """
    V2I prende le tensioni e le converte in corrente sapendo la resistenza
    parametri:
     - V tensione (Volt)
     - R reistenza (Ohm)
     - dV errore su V (Volt)
     - stdV deviazione standard su V
     - dR errore su R (Ohm)
    return:
     - corrente (Ampere)
     - errore su corrente (Ampere)
     - deviazione standard su corrente """
    return V / R, np.sqrt((dV / R)**2 + (dR * V / R**2)**2), stdV / R

def gaussian(x, mx, sx):
    """ gaussian ritorna il valore della gaussiana centrata in mx e sigma = sx
        serve per il metodo di filtraggio dati
        parametri:
          - x
          - mx centro x
          - sx sigma x
        return:
            - valore """
    return 1. / np.sqrt(2. * np.pi * sx**2) * np.exp(-0.5 * (x - mx)**2 / sx**2)


def order0fit(x, xx, yy, dxx):
    """ esegue un fit di ordine 0 dei dati e restituisce media e varianza
        campione. In pratica fa una media pesata secondo la gaussiana, si
        assume che var(x) * df/dx << var(y): questa ipotesi non è verificata
        nei nostri dati, ma al massimo introduce un errore di scala.
        parametri:
          - x valore di valutazione
          - xx ascisse dati
          - yy ordinate dati
          - dxx sigmax dei dati
        return:
          - media nell'intorno
          - varianza campione nell'intorno """
    try:
        my = np.zeros(len(x))
        sy = np.zeros_like(my)
        for i in range(len(x)):
            my[i], sy[i] = order0fit_impl(x[i], xx, yy, dxx)
        return my, sy
    except:
        return order0fit_impl(x, xx, yy, dxx)

def order0fit_impl(x, xx, yy, dxx):
    """ Implementazione del fit descritto in order0fit """
    w = gaussian(x, xx, dxx)
    sum_w = sum(w)
    w = w / sum_w

    my = sum(w * yy)
    var_y = sum((yy - my)**2 * w)
    return my, np.sqrt(var_y)

def filtro(x, y, dx, dy, n_sigma):
    """ Funzione di filtraggio dati. Se un punto dista più di n_sigma
        deviazioni standard dalla media (fittate da order0fit) viene
        eliminato dagli array di dati, questi vengono restituiti accorciati.
        parametri:
          - x, y, dx, dy: array di dati grezzi e loro incertezze associate
          - n_sigma soglia arbitraria oltre cui un y viene eliminato
        return:
          -x, y, dx, dy array di dati filtrati e loro incertezze associate """
    i = 0
    while(i<len(x)):
        print(i)
        media, dev = order0fit_impl(x[i], x, y, dx)
        if( abs(y[i] - media) > n_sigma*dev):
            x = numpy.delete(x, i)
            y = numpy.delete(y, i)
            dx = numpy.delete(dx, i)
            dy = numpy.delete(dy, i)
        else:
            i = i + 1
    return x, y, dx, dy



#================================================================
#                       FUNZIONI PER IL FIT
#================================================================

def sck(V, I0, nVt):
    return I0*(np.exp(V/nVt) - 1)



def errFun(V, V0, I0, nVt, R):
    return sck(V, I0, nVt) + (V - V0)/R



def deriv_errFun(V, I0, nVt, R):
    return I0 / nVt * np.exp(V/nVt) + 1./R;


if offset_fit:
    def curr(V, I0, nVt, R, offset):
        v = V;
        for i in range(Nstep):
            a = deriv_errFun(v, I0, nVt, R)
            v = v - errFun(v, V, I0, nVt, R) /a 
        return (V - v)/R + offset;
else:
    def curr(V, I0, nVt, R):
        v = V;
        for i in range(Nstep):
            a = deriv_errFun(v, I0, nVt, R)
            v = v - errFun(v, V, I0, nVt, R) /a 
        return (V - v)/R;


def ddp(I, nVt, I0, R):
    return nVt*np.log((I0+I)/I0) + R*I
