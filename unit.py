
def unit(u:float) -> str:
    str_u = str(u)
    unit = ""
    if u > 0.1:
        pass
        str_u = str(round(u,4))
    elif u > 0.0001:
        unit = "m"
        str_u = str(round(u*1000,4))
    elif u>0.0000001:
        unit = "u"
        str_u = str(round(u*1000000,4))
    elif u>0.0000000001:
        unit = "n"
        str_u = str(round(u*1000000000, 4))
    else:
        unit = "p"
        str_u = str(round(u*1000000000000,4))
    return str_u + unit