# RLC calculator tool

from math import sqrt, pow, pi
from unit import *



B = 150; # beta of the transistor (usualy ~120)
h11 = 1000; # h11 value of the transistor in Ohm


G = 100; # linéar gain of the band-pass filter
F0 = 1000000; # freq of the band-pass filter in Hz
BP = 3000; # range of the filter in Hz

R = (G * h11)/B
C = 1/(BP*2*pi*R)
L = pow((1/(F0*2*pi*sqrt(C))),2)

print("R = ", unit(R))
print("L = ", unit(L))
print("C = ",unit(C))