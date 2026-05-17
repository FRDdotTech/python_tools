"""
Calcule SCOAP pour un schéma logique et propose les parties A, B et C.
Partie A: CC0, CC1 et CO pour chaque ligne.
Partie B: score de testabilité pour chaque faute stuck-at.
Partie C: génération d'un vecteur de test pour une faute spécifiée.
"""

from common import *

AND = 0
OR = 1
NAND = 2
NOR = 3
XOR = 4
NOT = 5
PIN = 6

gate_array = ["and", "or", "nand", "nor", "xor", "not", ""]

class Gate:
    def __init__(self, node_name: str, gate_type: int, A: bool | Gate = False, B: bool | Gate = False) -> None:
        self.node_name = node_name
        self.gate_type = gate_type
        self.A = A
        self.B = B
        self.COout: list[int] = []

    def is_input(self) -> bool:
        return self.gate_type == PIN

    def out(self, inputs: dict[str, bool] | None = None, fault: tuple[str, bool] | None = None, cache: dict[str, bool] | None = None) -> bool:
        if cache is None:
            cache = {}
        if self.node_name in cache:
            return cache[self.node_name]

        if fault is not None and self.node_name == fault[0]:
            value = fault[1]
        elif self.gate_type == PIN:
            value = bool(inputs[self.node_name]) if inputs and self.node_name in inputs else bool(self.A)
        elif self.gate_type == AND:
            value = self.A.out(inputs=inputs, fault=fault, cache=cache) and self.B.out(inputs=inputs, fault=fault, cache=cache)
        elif self.gate_type == OR:
            value = self.A.out(inputs=inputs, fault=fault, cache=cache) or self.B.out(inputs=inputs, fault=fault, cache=cache)
        elif self.gate_type == NAND:
            value = not (self.A.out(inputs=inputs, fault=fault, cache=cache) and self.B.out(inputs=inputs, fault=fault, cache=cache))
        elif self.gate_type == NOR:
            value = not (self.A.out(inputs=inputs, fault=fault, cache=cache) or self.B.out(inputs=inputs, fault=fault, cache=cache))
        elif self.gate_type == XOR:
            value = self.A.out(inputs=inputs, fault=fault, cache=cache) ^ self.B.out(inputs=inputs, fault=fault, cache=cache)
        elif self.gate_type == NOT:
            value = not self.A.out(inputs=inputs, fault=fault, cache=cache)
        else:
            print("Unsupported gate type")

        cache[self.node_name] = value
        return value

    def CC0(self) -> int:
        if self.gate_type == PIN:
            return 1
        if self.gate_type == AND:
            return min(self.A.CC0(), self.B.CC0()) + 1
        if self.gate_type == OR:
            return self.A.CC0() + self.B.CC0() + 1
        if self.gate_type == NAND:
            return self.A.CC1() + self.B.CC1() + 1
        if self.gate_type == NOR:
            return min(self.A.CC1(), self.B.CC1()) + 1
        if self.gate_type == XOR:
            return min(self.A.CC0() + self.B.CC0(), self.A.CC1() + self.B.CC1()) + 1
        if self.gate_type == NOT:
            return self.A.CC1() + 1
        print("Unsupported gate type")

    def CC1(self) -> int:
        if self.gate_type == PIN:
            return 1
        if self.gate_type == AND:
            return self.A.CC1() + self.B.CC1() + 1
        if self.gate_type == OR:
            return min(self.A.CC1(), self.B.CC1()) + 1
        if self.gate_type == NAND:
            return min(self.A.CC0(), self.B.CC0()) + 1
        if self.gate_type == NOR:
            return self.A.CC0() + self.B.CC0() + 1
        if self.gate_type == XOR:
            return min(self.A.CC1() + self.B.CC0(), self.A.CC0() + self.B.CC1()) + 1
        if self.gate_type == NOT:
            return self.A.CC0() + 1
        print("Unsupported gate type")

    def CO(self) -> int:
        if not self.COout:
            printf("CO called on node ", self.node_name, " with no observability value")
        cost = min(self.COout)
        if self.gate_type == PIN:
            return cost
        if self.gate_type == AND or self.gate_type == NAND:
            self.A.COout.append(cost + self.B.CC1() + 1)
            self.B.COout.append(cost + self.A.CC1() + 1)
        elif self.gate_type == OR or self.gate_type == NOR:
            self.A.COout.append(cost + self.B.CC0() + 1)
            self.B.COout.append(cost + self.A.CC0() + 1)
        elif self.gate_type == XOR:
            self.A.COout.append(cost + min(self.B.CC0(), self.B.CC1()) + 1)
            self.B.COout.append(cost + min(self.A.CC0(), self.A.CC1()) + 1)
        elif self.gate_type == NOT:
            self.A.COout.append(cost + 1)
        else:
            print("Unsupported gate type")
        return cost

    def reset_coout(self) -> None:
        self.COout = []
        if isinstance(self.A, Gate):
            self.A.reset_coout()
        if isinstance(self.B, Gate):
            self.B.reset_coout()

    def row(self, co_value: int | str) -> str:
        return self.node_name + str(self.CC0()) + str(self.CC1()) + str(co_value)


class Circuit:
    def __init__(self) -> None:
        self.gates: dict[str, Gate] = {}
        self.inputs: list[str] = []
        self.outputs: list[str] = []

    def add_pin(self, name: str) -> None:
        if name not in self.gates:
            self.gates[name] = Gate(name, PIN)
        if name not in self.inputs:
            self.inputs.append(name)

    def add_gate(self, name: str, gate_type: int, input_a: str, input_b: str | None = None) -> None:
        if gate_type == NOT:
            if input_a not in self.gates:
                print("input error")
            self.gates[name] = Gate(name, gate_type, self.gates[input_a])
        else:
            if input_a not in self.gates or input_b not in self.gates:
                print("input error")
            self.gates[name] = Gate(name, gate_type, self.gates[input_a], self.gates[input_b])

    def set_outputs(self, outputs: list[str]) -> None:
        for output in outputs:
            if output not in self.gates:
                print("output error")
        self.outputs = outputs

    def compute_cc_values(self) -> tuple[dict[str, int], dict[str, int]]:
        return ({name: gate.CC0() for name, gate in self.gates.items()}, {name: gate.CC1() for name, gate in self.gates.items()})

    def topological_order(self) -> list[str]:
        visited: set[str] = set()
        order: list[str] = []

        def dfs(node_name: str) -> None:
            if node_name in visited:
                return
            visited.add(node_name)
            gate = self.gates[node_name]
            if isinstance(gate.A, Gate):
                dfs(gate.A.node_name)
            if isinstance(gate.B, Gate):
                dfs(gate.B.node_name)
            order.append(node_name)

        for name in self.gates:
            dfs(name)
        return order

    def compute_co_values(self) -> dict[str, int]:
        for gate in self.gates.values():
            gate.reset_coout()
        for output in self.outputs:
            self.gates[output].COout.append(0)
        order = self.topological_order()
        for name in reversed(order):
            gate = self.gates[name]
            if gate.COout:
                gate.CO()
        return {name: min(gate.COout) if gate.COout else float('inf') for name, gate in self.gates.items()}

    def evaluate(self, node_name: str, inputs: dict[str, bool], fault: tuple[str, bool] | None = None) -> bool:
        if node_name not in self.gates:
                print("node not found")
        return self.gates[node_name].out(inputs=inputs, fault=fault, cache={})

    def evaluate_all(self, inputs: dict[str, bool], fault: tuple[str, bool] | None = None) -> dict[str, bool]:
        values: dict[str, bool] = {}
        for name, gate in self.gates.items():
            values[name] = gate.out(inputs=inputs, fault=fault, cache=values)
        return values


    def find_test_vector(self, fault_node: str, stuck_at: bool, max_inputs: int = 16) -> tuple[dict[str, bool], dict[str, bool], dict[str, bool]] | None:
        if len(self.inputs) > max_inputs:
            return None
        if fault_node not in self.gates:
                print("fault node not found")
        fault_value = bool(stuck_at)
        target_value = not fault_value
        for bits in product([False, True], repeat=len(self.inputs)):
            assignment = dict(zip(self.inputs, bits))
            good = self.evaluate_all(assignment, fault=None)
            if good[fault_node] != target_value:
                continue
            faulty = self.evaluate_all(assignment, fault=(fault_node, fault_value))
            if any(good[out] != faulty[out] for out in self.outputs):
                return assignment, good, faulty
        return None

    def faultability_table(self) -> list[tuple[str, int, int, int, int]]:
        cc0, cc1 = self.compute_cc_values()
        co = self.compute_co_values()
        return [(name, cc0[name], cc1[name], co[name], cc0[name] + co[name]) for name in self.gates]

    def all_faults(self) -> list[tuple[str, bool]]:
        return [(name, False) for name in self.gates] + [(name, True) for name in self.gates]


def read_nodes(prompt: str) -> list[str]:
    values: list[str] = []
    index = 0
    while True:
        index += 1
        line = input("\ny" + str(index) + " : ").strip().lower()
        if line == "":
            break
        values.append("y"+ str(index) +"::" + line)
    return values

def read_list(prompt: str) -> list[str]:
    print(prompt)
    values: list[str] = []
    while True:
        line = input().strip()
        if not line:
            break
        values.append(line)
    return values


def parse_gate_definition(line: str, circuit: Circuit) -> None:
    name = line.split("::")[0]
    line = line.split("::")[1]
    if "_" in line:
        tokens = line.strip().split("_")
    elif "," in line:
        tokens = line.strip().split(",")
    if len(tokens) < 3:
        print("invalid gate definition")
    tokens.insert(0, name)
    op = tokens[1].lower()
    if op == "not":
        if len(tokens) != 3:
            print("invalid gate definition")
        circuit.add_gate(name, NOT, tokens[2])
    else:
        if len(tokens) != 4:
            print("invalid gate definition")
        input_a = tokens[2]
        input_b = tokens[3]
        if op in ["and", "a"]:
            circuit.add_gate(name, AND, input_a, input_b)
        elif op in ["or", "o"]:
            circuit.add_gate(name, OR, input_a, input_b)
        elif op in ["nand", "na"]:
            circuit.add_gate(name, NAND, input_a, input_b)
        elif op == "nor":
            circuit.add_gate(name, NOR, input_a, input_b)
        elif op == "xor":
            circuit.add_gate(name, XOR, input_a, input_b)
        else:
            print("invalid gate definition")


def print_scoap(circuit: Circuit) -> None:
    co = circuit.compute_co_values()
    printf(" node", "  CC0", "  CC1", "  CO")
    for name in circuit.gates:
        gate = circuit.gates[name]
        printf( "   ",name, "    ", str(gate.CC0()), "    ", str(gate.CC1()), "    ", str(co[name]))




def main() -> None:
    circuit = Circuit()
    inputs = read_list("Entrez les noms des entrées, \nune par ligne \nVide pour terminer :")
    for input_name in inputs:
        circuit.add_pin(input_name)

    print("Entrez ensuite les définitions de portes \n(exemples : x_and_a_b, y_or_a_b, z_not_x). \nVide pour terminer :")
    gate_defs = read_nodes("")
    for line in gate_defs:
        parse_gate_definition(line, circuit)

    outputs = read_list("Entrez les noms des sorties,\nune par ligne \n[par défaut 's' si existant] \n \nVide pour terminer :")
    if not outputs:
        if "s" in circuit.gates:
            outputs = ["s"]
        else:
            print("Aucune sortie définie. \n Utilisez 's' ou spécifiez une sortie.")
            outputs = read_list("Entrez les noms des sorties, \nune par ligne \nVide pour terminer :")
    if not outputs:
        print("Aucune sortie disponible, arrêt.")
        return
    circuit.set_outputs(outputs)

    print("\nPartie A : SCOAP (CC0, CC1, CO)")
    print_scoap(circuit)

    print("simulation")
    while True:
        for i in circuit.inputs:
            state = input("input " + i + " = ")
            if state in ["0", "1"]:
                circuit.gates[i].A = int(state)
            else :
                break
        for i in circuit.outputs:
            print(i + " = " + str(circuit.gates[i].out()))

        if input("fault test ? "):
            result_list:list[list[str]] = [[],[],[],[],[],[],[]]
            print("Entrez les fautes sous la forme 'node/0' ou 'node/1'. Une ligne vide termine.")
            print(circuit.gates.keys())
            faults: list[tuple[str, bool]] = []
            while True:
                line = input().strip()
                if not line:
                    break
                if "/" in line:
                    name, value = line.split("/", 1)
                elif "," in line:
                    name, value = line.split(",", 1)
                value = value.strip()
                if value not in {"0", "1"}:
                    print("Valeur de faute invalide, utilisez 0 ou 1.")
                    continue
                faults.append((name.strip(), value == "1"))

            if not faults:
                print("Aucune faute saisie.")
                continue

            for fault_node, stuck_at in faults:
                print(fault_node + " S@" + str(int(stuck_at)))
                if fault_node not in circuit.gates:
                    print("Noeud non défini")
                    continue
                context_gt = circuit.gates[fault_node].gate_type
                context_a = circuit.gates[fault_node].A
                context_b = circuit.gates[fault_node].B
                circuit.gates[fault_node].gate_type = PIN
                circuit.gates[fault_node].A = stuck_at
                print(context_gt)
                for j, output in enumerate(circuit.outputs):
                    result_list[j].append(str(int(circuit.gates[output].out())))
                    print(output + " = " + str(int(circuit.gates[output].out())))
                circuit.gates[fault_node].gate_type = context_gt
                circuit.gates[fault_node].A = context_a
                circuit.gates[fault_node].B = context_b
            print("\nvector results : ")
            for j, output in enumerate(circuit.outputs):
                print_out = ""
                for element in result_list[j]:
                    print_out += element
                print(output + " = " + print_out)

        
        if input("exit ?") == "1":
                return

main()