from math import sqrt

n0 = (0.0,)
n1 = (1.0,)
n2 = (sqrt(2),)
n3 = (1.0, 0.0)
n4 = (0.765, 1.848)
n5 = (0.618, 1.618, 0.0)
n6 = (0.5176, 1.4142, 1.9318)
n7 = (0.445, 1.247, 1.8019, 0.0)
n8 = (0.3902, 1.1111, 1.6629, 1.9616)

active_normalised_componant: list[tuple[float, ...]] = [n0, n1, n2, n3, n4, n5, n6, n7, n8]

p_n0 = (0.0,)
p_n1 = (0.0,)
p_n2 = (0.0,)
p_n3 = (1.0, 2.0, 1.0)
p_n4 = (0.765, 1.848, 1.848, 0.765)
p_n5 = (0.618, 1.618, 2, 1.618, 0.618)
p_n6 = (0.5176, 1.4142, 1.9318, 1.9318, 1.4142, 0.5176)
p_n7 = (0.445, 1.247, 1.8019, 2, 1.8019, 1.247, 0.445)
p_n8 = (0.390, 1.111, 1.663, 1.962, 1.962, 1.663, 1.111, 0.390)

passiv_normalised_componant: list[tuple[float, ...]] = [p_n0, p_n1, p_n2, p_n3, p_n4, p_n5, p_n6, p_n7, p_n8]

def unit(u:float, sign:str = "") -> str:
    str_u = str(u)
    unit = " "
    if u > 1000000000:
        unit = " G"
        str_u = str(round(u/1000000000,4))
    elif u > 1000000:
        unit = " M"
        str_u = str(round(u/1000000,4))
    elif u > 1000:
        unit = " K"
        str_u = str(round(u/1000,4))
    elif u > 0.1:
        unit = " "
        str_u = str(round(u,4))
    elif u > 0.0001:
        unit = " m"
        str_u = str(round(u*1000,4))
    elif u>0.0000001:
        unit = " u"
        str_u = str(round(u*1000000,4))
    elif u>0.0000000001:
        unit = " n"
        str_u = str(round(u*1000000000, 4))
    else:
        unit = " p"
        str_u = str(round(u*1000000000000,4))
    return str_u + unit + sign

def product(*iterables, repeat=1):
    # product('ABCD', 'xy') → Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) → 000 001 010 011 100 101 110 111

    if repeat < 0:
        print('repeat argument cannot be negative')
    pools = [tuple(pool) for pool in iterables] * repeat

    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]

    for prod in result:
        yield tuple(prod)

def printf(*args):
    formatted_string = ""
    for arg in args:
        formatted_string += str(arg)
    print(formatted_string)