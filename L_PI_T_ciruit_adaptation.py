import math

def ask_float(prompt):
    while True:
        try:
            return float(input(prompt).replace(',', '.'))
        except ValueError:
            print("Entrée invalide, veuillez saisir un nombre.")

def choose_topology():
    print("\nChoisissez le type de circuit d'adaptation :")
    print("1 - L")
    print("2 - PI")
    print("3 - T")
    print("4 - LL")
    while True:
        choice = input("Votre choix (1/2/3:4) : ").strip()
        if choice in ["1", "2", "3", "4"]:
            return {"1": "L", "2": "PI", "3": "T", "4": "LL"}[choice]
        print("Choix invalide.")

def compute_l_match(Rs, Rl, f, mode="lpf"):
    """
    Adaptation en L entre Rs et Rl.
    Convention:
    - Si Rs < Rl : réseau passe-bas ou passe-haut selon mode
    - Si Rs > Rl : inversion des rôles pour garder la même logique
    """
    swapped = False
    if Rs > Rl:
        Rs, Rl = Rl, Rs
        swapped = True

    Q = math.sqrt(Rl / Rs - 1)

    w = 2 * math.pi * f

    # Cas classique : série puis parallèle
    if mode == 1:
        print("calcule pour low-pass")
        C_val = Q / (Rl*w)
        L_val =  1 / ((C_val * (w * w))*(1+1/(Q*Q)))
    else:
        print("calcule pour high-pass")
        L_val = (Q*Rs) / w
        C_val =  (1+(1/(Q*Q))) / (L_val * (w * w))

    result = {
        "Q": Q,
        "Rs": Rs,
        "Rl": Rl,
        "L_series_H": L_val,
        "C_shunt_F": C_val,
        "swapped": swapped
    }
    return result

def compute_pi_match(Rs, Rl, f, Q=None, mode=None):
    rmin, rmax = min(Rs, Rl), max(Rs, Rl)
    Qmin = math.sqrt(rmax / rmin - 1)
    if Q is None:
        Q = Qmin
    if Q < Qmin:
        print(f"Q trop faible, minimum = {Qmin:.4f}")

    # Résistance virtuelle centrale du PI
    Rv = rmax / (1 + Q * Q)

    # Deux sous-circuits L

    print("ciruit Rs -> Rv")
    result = compute_l_match(Rs, Rv, f, mode)
    print(f"Q = {result['Q']:.4f}")
    print(f"L = {format_value(result['L_series_H'], 'H')}")
    print(f"C = {format_value(result['C_shunt_F'], 'F')}")
    if result["swapped"]:
        print("Note : Rs et Rl ont été inversées pour le calcul.")

    print("ciruit Rv -> Rl")
    result = compute_l_match(Rv, Rl, f, mode)
    print(f"Q = {result['Q']:.4f}")
    print(f"L = {format_value(result['L_series_H'], 'H')}")
    print(f"C = {format_value(result['C_shunt_F'], 'F')}")
    if result["swapped"]:
        print("Note : Rs et Rl ont été inversées pour le calcul.")
    
def compute_t_match(Rs, Rl, f, Q=None, mode=None):
    """
    Réseau T : on impose Q si fourni, sinon Q minimal.
    Formules usuelles:
      Qmin = sqrt(Rhigh/Rlow - 1)
    """
    rmin, rmax = min(Rs, Rl), max(Rs, Rl)
    Qmin = math.sqrt(rmax / rmin - 1)
    if Q is None:
        Q = Qmin
    if Q < Qmin:
        print(f"Q trop faible, minimum = {Qmin:.4f}")

    # Résistance virtuelle centrale du T
    Rv = (1+ (Q*Q))*rmin

    # Deux sous-circuits L

    print("ciruit Rs -> Rv")
    result = compute_l_match(Rs, Rv, f, mode)
    print(f"Q = {result['Q']:.4f}")
    print(f"L = {format_value(result['L_series_H'], 'H')}")
    print(f"C = {format_value(result['C_shunt_F'], 'F')}")
    if result["swapped"]:
        print("Note : Rs et Rl ont été inversées pour le calcul.")

    print("ciruit Rv -> Rl")
    result = compute_l_match(Rv, Rl, f, mode)
    print(f"Q = {result['Q']:.4f}")
    print(f"L = {format_value(result['L_series_H'], 'H')}")
    print(f"C = {format_value(result['C_shunt_F'], 'F')}")
    if result["swapped"]:
        print("Note : Rs et Rl ont été inversées pour le calcul.")

def compute_ll_match(Rs, Rl, f, Q=None, mode=None):
    rmin, rmax = min(Rs, Rl), max(Rs, Rl)
    Qmin = math.sqrt(rmax / rmin - 1)
    if Q is None:
        Q = Qmin
    if Q < Qmin:
        print(f"Q trop faible, minimum = {Qmin:.4f}")

    # Résistance virtuelle centrale du PI
    Rv = math.sqrt(Rs * Rl)

    # Deux sous-circuits L

    print("ciruit Rs -> Rv")
    result = compute_l_match(Rs, Rv, f, mode)
    print(f"Q = {result['Q']:.4f}")
    print(f"L = {format_value(result['L_series_H'], 'H')}")
    print(f"C = {format_value(result['C_shunt_F'], 'F')}")
    if result["swapped"]:
        print("Note : Rs et Rl ont été inversées pour le calcul.")

    print("ciruit Rv -> Rl")
    result = compute_l_match(Rv, Rl, f, mode)
    print(f"Q = {result['Q']:.4f}")
    print(f"L = {format_value(result['L_series_H'], 'H')}")
    print(f"C = {format_value(result['C_shunt_F'], 'F')}")
    if result["swapped"]:
        print("Note : Rs et Rl ont été inversées pour le calcul.")
    

def format_value(value, unit):
    prefixes = [
        (1e-12, "p"),
        (1e-9, "n"),
        (1e-6, "µ"),
        (1e-3, "m"),
        (1, ""),
        (1e3, "k"),
        (1e6, "M")
    ]
    abs_val = abs(value)
    for scale, prefix in prefixes:
        if abs_val < scale * 1000 or scale == 1e6:
            return f"{value/scale:.4g} {prefix}{unit}"
    return f"{value:.4g} {unit}"

def main():
    print("=== Calcul d'adaptation d'impédance ===")
    topo = choose_topology()
    Rs = ask_float("Résistance/source Rs (ohms) : ")
    Rl = ask_float("Résistance/charge Rl (ohms) : ")
    f = ask_float("Fréquence (Hz) : ")
    mode = ask_float("type de cirtuit 1 : lpf - 2 : hpf")

    Q_user = None
    if topo in ["PI", "T"]:
        use_q = input("Voulez-vous imposer un Q ? (o/n) : ").strip().lower()
        if use_q == "o":
            Q_user = ask_float("Valeur de Q : ")

    print("\n--- Résultats ---")
    print(f"Topologie choisie : {topo}")
    print(f"Rs = {Rs} ohms, Rl = {Rl} ohms, f = {f} Hz")

    if topo == "L":
        result = compute_l_match(Rs, Rl, f, mode)
        print(f"Q = {result['Q']:.4f}")
        print(f"L = {format_value(result['L_series_H'], 'H')}")
        print(f"C = {format_value(result['C_shunt_F'], 'F')}")
        if result["swapped"]:
            print("Note : Rs et Rl ont été inversées pour le calcul.")

    elif topo == "PI":
        result = compute_pi_match(Rs, Rl, f, Q_user, mode)
        

    elif topo == "T":
        result = compute_t_match(Rs, Rl, f, Q_user, mode)

    elif topo == "LL":
        result = compute_ll_match(Rs, Rl, f, Q_user, mode)
        

if __name__ == "__main__":
    main()