import numpy as np

# local interaction: X, Y, Z, XX, YY, ZZ
### graph representation

def interaction(edges, vertices):
    terms = []
    for edge in edges:
        term = f"{{1 * [@ax{edge[0]}x{edge[1]}@]}} * X{edge[0]}X{edge[1]} + {{1 * [@ay{edge[0]}y{edge[1]}@]}} * Y{edge[0]}Y{edge[1]} + {{1 * [@az{edge[0]}z{edge[1]}@]}} * Z{edge[0]}Z{edge[1]}"
        terms.append(term)
    for vertex in vertices:
        term = f"{{1 * [@omega{vertex}@ * np.cos(@phi{vertex}@)]}} * X{vertex} + {{1 * [@omega{vertex}@ * np.sin(@phi{vertex}@)]}} * Y{vertex} + {{1 * [@az{vertex}@]}} * Z{vertex}"
        terms.append(term)
    result = " + ".join(terms)
    return result

def local_bs(edges, vertices):
    local_ubs = {}
    local_lbs = {}
    for edge in edges:
        local_ubs[f"ax{edge[0]}x{edge[1]}"] = 1
        local_lbs[f"ax{edge[0]}x{edge[1]}"] = -1
        local_ubs[f"ay{edge[0]}y{edge[1]}"] = 1
        local_lbs[f"ay{edge[0]}y{edge[1]}"] = -1
        local_ubs[f"az{edge[0]}z{edge[1]}"] = 1
        local_lbs[f"az{edge[0]}z{edge[1]}"] = -1
    for vertex in vertices:
        local_ubs[f"omega{vertex}"] = 1
        local_lbs[f"omega{vertex}"] = -1
        local_ubs[f"az{vertex}"] = 1
        local_lbs[f"az{vertex}"] = -1
    
    return local_ubs, local_lbs

def gen_heisenberg(edges, vertices):
    # Rydberg system Hamiltonian
    ham_sys = ""

    # Local laser Hamiltonian and its bound
    ham_local = interaction(edges, vertices)
    local_ubs, local_lbs = local_bs(edges, vertices)

    return [ham_sys, ham_local, local_ubs, local_lbs]
