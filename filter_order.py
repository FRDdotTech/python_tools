from math import log10, ceil



Fa1 = 0
Fc1 = 0



#
# user Variables
# 
"""
0 -> low-pass
1 -> High-pass
2 -> band pass
"""
filter_type = 1
Fa = 250000
Fc = 750000
Ga = -50
Gc = -3
#
# user Variables
# 
filter_type = int(input("\n\nchoose the filter type\n"
                    "0 -> low-pass\n"
                    "1 -> High-passn\n"
                    "2 -> band pass\n ->"))

Fa = float(input("enter a value for Fa \n ->"))
Fc = float(input("enter a value for Fc \n ->"))
Gc = float(input("enter a value for Gc (for butterworth -3 dB) \n ->"))
Ga = float(input("enter a value for Ga (As)\n ->"))

As = abs(Ga)  # gain after attenuation freq


if filter_type == 0:
    a = Fa/Fc
elif filter_type == 1:
    a = Fc/Fa
else:
    a = 0



n = As/(20*log10(a))
ceil_n = ceil(n)
print()
print("          AS")
print("n = -------------")
print("     20*log10(A)")
print()

print("n = ", n)
print("usable value is ->", ceil_n)