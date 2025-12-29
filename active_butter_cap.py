from math import sqrt, pow, pi, log10, ceil
from unit import *

As = 20 # attenuation en dB
freqc = 20000 #frequence de coupure
freqa = 40000 # frequence d'ttenuation
wc = 2 * pi * freqc # pulsation de coupure
wa = 2 * pi * freqa # pulsation de coupure
a = freqa/freqc# pulsation de coupure / pulsation d'attenuation

p = 1

c = 0.0000001
r = 10000  # 10k

n = ceil(As/(20*log10(a)))  # As/20log(A)

def ordre2(indice:float) -> float:
    return (pow(p,2) + indice*p + 1)
#c2 = 0.445/2R*wc
#c1 = 1/R²*c2*(wc)²

def c2(i:float, r:float, wc:float) -> float:
    return i/(2*r*wc)

def c1(c2:float, r:float, wc:float) -> float:
    return 1/(pow(r,2)*c2*pow(wc,2))



n1 = p + 1
n2 = pow(p,2) + sqrt(2*p) + 1
n3 = (p + 1)*(pow(p,2) + p + 1)
n4 = (0.765, 1.848)
n6 = (0.5176, 1.4142, 1.9318)
n7 = (0.445, 1.247, 1.8019, 1)

for i in n4:
    var_c2 = c2(i, r, wc)
    var_c1 = c1(var_c2, r, wc)
    print("c1 = ", unit(var_c1))
    print("c2 = ", unit(var_c2))





