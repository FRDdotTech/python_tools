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
    while True:
        choice = input("Votre choix (1/2/3) : ").strip()
        if choice in ["1", "2", "3"]:
            return {"1": "L", "2": "PI", "3": "T"}[choice]
        print("Choix invalide.")

def compute_l_match(Rs, Rl, f, mode=None):
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
    Xs = Rs * Q
    Xp = Rl / Q

    w = 2 * math.pi * f

    # Cas classique : série puis parallèle
    L_series = Xs / w
    C_shunt = 1 / (w * Xp)

    result = {
        "Q": Q,
        "Rs": Rs,
        "Rl": Rl,
        "L_series_H": L_series,
        "C_shunt_F": C_shunt,
        "swapped": swapped
    }
    return result

def compute_pi_match(Rs, Rl, f, Q=None):
    """
    Réseau PI : on impose Q si fourni, sinon Q minimal.
    Formules usuelles:
      Qmin = sqrt(Rhigh/Rlow - 1)
      Q > Qmin pour un PI réalisable
    """
    Rlow = min(Rs, Rl)
    Rhigh = max(Rs, Rl)
    Qmin = math.sqrt(Rhigh / Rlow - 1)

    if Q is None:
        Q = Qmin
    elif Q < Qmin:
        raise ValueError(f"Q trop faible. Minimum requis: {Qmin:.4f}")

    w = 2 * math.pi * f

    Xs = Q * Rlow
    Xp1 = Rhigh / Q
    Xp2 = Rhigh / Q

    C_in = 1 / (w * Xp1)
    L_series = Xs / w
    C_out = 1 / (w * Xp2)

    return {
        "Q": Q,
        "Qmin": Qmin,
        "C_in_F": C_in,
        "L_series_H": L_series,
        "C_out_F": C_out
    }

def compute_t_match(Rs, Rl, f, Q=None):
    """
    Réseau T : on impose Q si fourni, sinon Q minimal.
    Formules usuelles:
      Qmin = sqrt(Rhigh/Rlow - 1)
    """
    Rlow = min(Rs, Rl)
    Rhigh = max(Rs, Rl)
    Qmin = math.sqrt(Rhigh / Rlow - 1)

    if Q is None:
        Q = Qmin
    elif Q < Qmin:
        raise ValueError(f"Q trop faible. Minimum requis: {Qmin:.4f}")

    w = 2 * math.pi * f

    Xs = Rlow * Q
    Xp = Rhigh / Q

    L1 = Xs / w
    Cshunt = 1 / (w * Xp)
    L2 = Xs / w

    return {
        "Q": Q,
        "Qmin": Qmin,
        "L1_H": L1,
        "C_shunt_F": Cshunt,
        "L2_H": L2
    }

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

    Q_user = None
    if topo in ["PI", "T"]:
        use_q = input("Voulez-vous imposer un Q ? (o/n) : ").strip().lower()
        if use_q == "o":
            Q_user = ask_float("Valeur de Q : ")

    print("\n--- Résultats ---")
    print(f"Topologie choisie : {topo}")
    print(f"Rs = {Rs} ohms, Rl = {Rl} ohms, f = {f} Hz")

    if topo == "L":
        result = compute_l_match(Rs, Rl, f)
        print(f"Q = {result['Q']:.4f}")
        print(f"L série = {format_value(result['L_series_H'], 'H')}")
        print(f"C shunt = {format_value(result['C_shunt_F'], 'F')}")
        if result["swapped"]:
            print("Note : Rs et Rl ont été inversées pour le calcul.")

    elif topo == "PI":
        result = compute_pi_match(Rs, Rl, f, Q_user)
        print(f"Q = {result['Q']:.4f}")
        print(f"Qmin = {result['Qmin']:.4f}")
        print(f"C entrée = {format_value(result['C_in_F'], 'F')}")
        print(f"L série = {format_value(result['L_series_H'], 'H')}")
        print(f"C sortie = {format_value(result['C_out_F'], 'F')}")

    elif topo == "T":
        result = compute_t_match(Rs, Rl, f, Q_user)
        print(f"Q = {result['Q']:.4f}")
        print(f"Qmin = {result['Qmin']:.4f}")
        print(f"L1 = {format_value(result['L1_H'], 'H')}")
        print(f"C shunt = {format_value(result['C_shunt_F'], 'F')}")
        print(f"L2 = {format_value(result['L2_H'], 'H')}")

if __name__ == "__main__":
    main()