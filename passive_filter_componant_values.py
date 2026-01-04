# denormalising algorithm

from common import *
from math import pi


#
# user Variables
#  
"""
0 -> low-pass
1 -> High-pass
2 -> band pass
"""
filter_type = 1
n = 6
R0 = 50
Fc = 750000
#
# user Variables
#  

Fc = float(input("enter a value for Fc \n ->"))
filter_type = int(input("\n\nchoose the filter type\n"
                    "0 -> low-pass\n"
                    "1 -> High-passn\n"
                    "2 -> band pass\n ->"))

n = int(input("enter a value for n \n ->"))

wc = 2 * pi * Fc # pulsation de coupure




C_value = []
L_value = []

if filter_type == 0:
    print()
    print("        p")
    print("C = --------")
    print("      R0*ωc")
    print()
    print("      p*R0")
    print("L = --------")
    print("       ωc")
    print()
    input("press enter to calculate...")
    for i, p in enumerate(passiv_normalised_componant[n]):
        if i % 2:
            C_value.append(unit(p/(R0*wc), "F"))
        else:
            L_value.append(unit((p*R0)/(wc), "H"))
elif filter_type == 1:
    print("\n\nfor high-pass filter transposition of p\n")
    print("-->  p = 1/p")
    print()
    print("        p")
    print("C = --------")
    print("      R0*ωc")
    print()
    print("      p*R0")
    print("L = --------")
    print("       ωc")
    print()
    input("press enter to calculate...")
    for i, p in enumerate(passiv_normalised_componant[n]):
        p = 1/p
        if i % 2:
            L_value.append(unit((p*R0)/(wc), "H"))
        else:
            C_value.append(unit(p/(R0*wc), "F"))      
else:
    a = 0

print("C_value = " ,C_value)
print("L_value = " ,L_value)