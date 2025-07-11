import numpy as np
import copy

# van der waals interaction
# van der waals interaction
def ZZ(n):
    terms = []
    for i in range(n - 1):
        for j in range(i + 1, n):
            term = f"{{1 * [862690 / (4 * (@x_{i}_@ - @x_{j}_@) ** 6)]}} * Z{i}Z{j}"
            terms.append(term)
    result = " + ".join(terms)
    return result

def Z(n):
    terms = []
    for i in range(n):
        coefs = []
        for j in range(i):
            coef = f"- 1 * [862690 / (4 * (@x_{j}_@ - @x_{i}_@) ** 6)]"
            coefs.append(coef)
        for j in range(i+1, n):
            coef = f"- 1 * [862690 / (4 * (@x_{i}_@ - @x_{j}_@) ** 6)]"
            coefs.append(coef)

        coef_str = " ".join(coefs)
        coef_str = "{" + coef_str + "}" + " * " + f"Z{i}"

        terms.append(coef_str)

        # print(coef_str)
    result = " + ".join(terms)

    return result

# local laser
def laser(n):
    terms = []
    for i in range(n):
        term = f"{{1 * [@delta@ / 2]}} * Z{i} + {{1 * [@omega@ * np.cos(@phi@) / 2]}} * X{i} + {{-1 * [@omega@ * np.sin(@phi@) / 2]}} * Y{i}"
        terms.append(term)
    result = " + ".join(terms)
    return result

def laser_bs(n):
    local_ubs = {}
    local_lbs = {}
    local_ubs["delta"] = 20
    local_lbs["delta"] = -20
    local_ubs["omega"] = 2.2
    local_lbs["omega"] = 0
    
    return local_ubs, local_lbs

def amp_adjust(sol_dic):

    keys = [key for key in sol_dic.keys() if key.startswith("omega")]
    for key in keys:
        if sol_dic[key] < 0:  # Check if the value is negative
            j = key[5:]  # Extract the index j from 'omega{j}'
            phi_key = f"phi{j}"  # Corresponding phi key

            if phi_key in sol_dic:  # Ensure phi key exists before modifying
                sol_dic[key] = -sol_dic[key]  # Make omega positive
                sol_dic[phi_key] = (sol_dic[phi_key] + np.pi) % (2 * np.pi)  # Adjust phi
                
    return sol_dic

# Create all the operator that may appear in equation 
def gen_op_list(n):
    op_list = []
    
    # Products of Z operators on pairs of qubits
    for i in range(0, n):
        for j in range(i+1, n):
            op_list.append(f'Z{i}Z{j}')
    
    # Single qubit Z, X, Y operators
    for i in range(0, n):
        op_list.append(f'Z{i}')
    for i in range(0, n):
        op_list.append(f'X{i}')
    for i in range(0, n):
        op_list.append(f'Y{i}')
    
    return op_list

def init_gen(strength=None, t_tar=None, n=None):
    def nested_init_gen(t_sim=None, global_var=None):
        global_init = [[i*(862690 * t_sim / (4 * strength * t_tar))**(1/6) for i in range(n)]]
        return global_init
    return nested_init_gen

# for mapping purpose
def sim_ham_list(N):
    id = "I" * N
    ls = []

    for i in range(N):
        id_cp = copy.deepcopy(id)
        id_x = id_cp[:i] + "X" + id_cp[i + 1:]
        ls.append(id_x)

    for i in range(N):
        id_cp = copy.deepcopy(id)
        id_y = id_cp[:i] + "Y" + id_cp[i + 1:]
        ls.append(id_y)

    for i in range(N):
        id_cp = copy.deepcopy(id)
        id_z = id_cp[:i] + "Z" + id_cp[i + 1:]
        ls.append(id_z)

    for i in range(0, N-1):
        id_cp = copy.deepcopy(id)
        id_zz = id_cp[:i] + "ZZ" + id_cp[i + 2:]
        ls.append(id_zz)
        
    return ls

def gen_rydberg1D(n):
    # Rydberg system Hamiltonian
    term1 = ZZ(n)
    term2 = Z(n)
    ham_sys = term1 + " + " + term2

    # Local laser Hamiltonian and its bound
    ham_local = laser(n)
    local_ubs, local_lbs = laser_bs(n)

    # generate the operator list
    # op_list = gen_op_list(n)

    return [ham_sys, ham_local, local_ubs, local_lbs]
