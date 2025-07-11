import numpy as np

# van der waals interaction
def ZZ(n):
    terms = []
    for i in range(n - 1):
        for j in range(i + 1, n):
            term = f"{{1 * [862690 / (4 * ((@x_{i}_0@ - @x_{j}_0@)**2+(@x_{i}_1@ - @x_{j}_1@)**2) ** 3)]}} * Z{i}Z{j}"
            terms.append(term)
    result = " + ".join(terms)
    return result


def Z(n):
    terms = []
    for i in range(n):
        coefs = []
        for j in range(i):
            coef = f"- 1 * [862690 / (4 * ((@x_{j}_0@ - @x_{i}_0@)**2+(@x_{j}_1@ - @x_{i}_1@)**2) ** 3)]"
            coefs.append(coef)
        for j in range(i+1, n):
            coef = f"- 1 * [862690 / (4 * ((@x_{i}_0@ - @x_{j}_0@)**2+(@x_{i}_1@ - @x_{j}_1@)**2) ** 3)]"
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
    for i in range(n):
        # local_ubs[f"delta"] = 10.34/(2*np.pi)
        local_ubs[f"delta"] = 20
        # local_lbs[f"delta"] = -10.34/(2*np.pi)
        local_lbs[f"delta"] = -20
        local_ubs[f"omega"] = 1
        local_lbs[f"omega"] = 0
    
    return local_ubs, local_lbs

def amp_adjust(sol_dic):

    keys = [key for key in sol_dic.keys() if key.startswith("omega")]
    for key in keys:
        if sol_dic[key] < 0:  # Check if the value is negative
            phi_key = f"phi"  # Corresponding phi key

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

def init_gen_cyc(strength=None, t_tar=None, n=None):
    def nested_init_gen(t_sim=None, global_var=None):
        l = (862690 * t_sim / (4 * strength * t_tar)) ** (1.0 / 6) / (2 - 2 * np.cos(2 * np.pi / n)) ** 0.5
        global_init = []
        for var in global_var:
            parts = var.split('_')
            idx = int(parts[1])
            xy = int(parts[2])
            if xy ==0:
                global_init.append(l * (np.cos(idx * 2 * np.pi / n) - 1))
            else:
                global_init.append(l * np.sin(idx * 2 * np.pi / n))
        global_init = [global_init]
        return global_init
    return nested_init_gen

def init_gen_grid(strength=None, t_tar=None, n=None):
    def nested_init_gen(t_sim=None, global_var=None):
        l = (862690 * t_sim / (4 * strength * t_tar)) ** (1.0 / 6)
        global_init = []
        for var in global_var:
            parts = var.split('_')
            idx = int(parts[1])
            quotient, remainder = divmod(idx, n)
            xy = int(parts[2])
            if xy ==0:
                global_init.append(remainder * l)
            else:
                global_init.append(quotient * l)
        global_init = [global_init]
        return global_init
    return nested_init_gen

def gen_rydberg2D(n):
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
