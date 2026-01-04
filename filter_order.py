from math import log10, ceil

Fa = 250000
Fc = 750000

Ga = -50
Gc = -3

Fa1 = 0
Fc1 = 0

As = abs(Ga)  # gain after attenuation freq


"""
0 -> low-pass
1 -> High-pass
2 -> band pass
"""

filter_type = 1

if filter_type == 0:
    a = Fa/Fc
elif filter_type == 1:
    a = Fc/Fa
else:
    a = 0



n = As/(20*log10(a))
ceil_n = ceil(n)

print("n = ", n)
print("usable value is ->", ceil_n)