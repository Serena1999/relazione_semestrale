#CONFIGURAZIONI
#print(pylab.sqrt(costanti.Nstep))
#import librerie #non capisco perchè non funziona senza
from lib import *

grafici_calibrazione = True

grafici_previsione = False

Nstep = 20

# i dati filtrati sono messi in questa cartella temporanea
tmp_folder = "tmp/"

# parametri per il filtro
# se non vi piace odificate questi nomi
file2CName = "file2C.txt"
file2PyName = "file2Py.txt"
maxRatio = 3.0
minV = 0.2
filter_Nskip = 1000 #per le prove è utile velocizzare saltando dei dati (mettere a 1 per il run completo)
outSigma = 2.0 #numero di sigma per eliminare gli outliers

# abilita il disegno dei punti
plot_points = True

# disegna i punti scartati in rosso
plot_bad_points = False

# abilita l'offset sulla funzione di fit
offset_fit = True

# abilita le barre di errore sui grafici
plot_errors = True

# alpha per scatterplot (opacità)
scatterAlpha = 0.01

# abilita bande dei dati
plot_sigma_zone = False
sigma_zone_alpha = 0.25

# numero di iterazioni di curve_fit
iterazioni_fit = 3

# LaTeX typesetting maths and descriptions
tex = False

# manually choose spacing between axis ticks
tick = True 

# file di dati (da modificare)#!!
data_folder = "data/"
data_files = [
    # "dati_220k.txt",
    "dati_22k.txt",
    "dati_2.2k.txt",
    "dati_220.txt",
    "dati_22.txt",
    "data_diddati_2.2.txt",
    "dati_0.22.txt"
    ]
Nruns = len(data_files) # numero di files (runs)

# valori resistenze (da modificare)
Rs = np.array([
    # 216.8e3,#!! (se possiamo rimisurarle un attimo a lab  con l'attrezzo
    21.74e3,#!!  apposta meglio, atrimenti va bene comunque)
    2.2021e3,
    216.22,
    21.86,
    2.212,
    0.226
    ])
dRs = np.array([
    # 2.6e3,#!!
    0.26e3,#!!
    0.4,
    0.07,
    0.01,
    0.008,
    0.008
    ])
