import numpy as np

# generate square position
def gen_pos(n):
    M0 = n
    q, r = np.divmod(M0, 4)
    even_odd = q % 2
    M = q*4
    pos = []
    for i in range(M):
        q_, r_ = np.divmod(i, q)
        if q_ == 0:
            x = f"{r_}*@l@"
            y = f"0*@l@"
            pos.append((x,y))
        elif q_ == 1:
            x = f"{q}*@l@"
            y = f"{r_}*@l@"
            pos.append((x,y))
        elif q_ == 2:
            x = f"{(q-r_)}*@l@"
            y = f"{q}*@l@"
            pos.append((x,y))
        elif q_ == 3:
            x = f"0*@l@"
            y = f"{(q-r_)}*@l@"
            pos.append((x,y))

    for i in range(r):
        if i == 0:
            # pos[int(q*0+np.ceil(q/2))-1] = (f"{((np.ceil(q/2)-0.5)-1)}*@l@", f"{-(np.sqrt(3)/2)}*@l@")
            pos[int(q*0+np.ceil(q/2))] = (f"{((np.ceil(q/2)-0.5)+1)}*@l@", f"{-(np.sqrt(3)/2)}*@l@")
            pos.insert(int(q*0+np.ceil(q/2)), (f"{(np.ceil(q/2)-0.5)}*@l@", f"{-(np.sqrt(3)/2)}*@l@"))
        if i == 1:
            # pos[int(q*1+np.ceil(q/2)+1)-1] = (f"{(q+np.sqrt(3)/2)}*@l@", f"{(np.ceil(q/2)-1.5)}*@l@")
            pos[int(q*1+np.ceil(q/2)+1)] = (f"{(q+np.sqrt(3)/2)}*@l@", f"{(np.ceil(q/2)+0.5)}*@l@")
            pos.insert(int(q*1+np.ceil(q/2)+1), (f"{(q+np.sqrt(3)/2)}*@l@", f"{(np.ceil(q/2)-0.5)}*@l@"))
        if i == 2:
            if even_odd == 1:
                # pos[int(q*2+np.ceil(q/2)+2)-1] = (f"{(np.ceil(q/2)+0.5)}*@l@", f"{(q+np.sqrt(3)/2)}*@l@")
                pos[int(q*2+np.ceil(q/2)+2)] = (f"{(np.ceil(q/2)-1.5)}*@l@", f"{(q+np.sqrt(3)/2)}*@l@")
                pos.insert(int(q*2+np.ceil(q/2)+2), (f"{(np.ceil(q/2)-0.5)}*@l@", f"{(q+np.sqrt(3)/2)}*@l@"))
            else:
                # pos[int(q*2+np.ceil(q/2)+2)-1] = (f"{(np.ceil(q/2)+1.5)}*@l@", f"{(q+np.sqrt(3)/2)}*@l@")
                pos[int(q*2+np.ceil(q/2)+2)] = (f"{(np.ceil(q/2)-0.5)}*@l@", f"{(q+np.sqrt(3)/2)}*@l@")
                pos.insert(int(q*2+np.ceil(q/2)+2), (f"{(np.ceil(q/2)+0.5)}*@l@", f"{(q+np.sqrt(3)/2)}*@l@"))
    return pos

# van der waals interaction
def ZZ(n, pos):
    terms = []
    for i in range(n - 1):
        for j in range(i + 1, n):
            x_i_0 = pos[i][0]
            x_i_1 = pos[i][1]
            x_j_0 = pos[j][0]
            x_j_1 = pos[j][1]
            term = f"{{1 * [862690 / (4 * ((({x_i_0}) - ({x_j_0}))**2+(({x_i_1}) - ({x_j_1}))**2) ** 3)]}} * Z{i}Z{j}"
            terms.append(term)
    result = " + ".join(terms)
    return result

def Z(n, pos):
    terms = []
    for i in range(n):
        coefs = []
        for j in range(i):
            x_i_0 = pos[i][0]
            x_i_1 = pos[i][1]
            x_j_0 = pos[j][0]
            x_j_1 = pos[j][1]
            coef = f"- 1 * [862690 / (4 * ((({x_j_0}) - ({x_i_0}))**2+(({x_j_1}) - ({x_i_1}))**2) ** 3)]"
            coefs.append(coef)
        for j in range(i+1, n):
            x_i_0 = pos[i][0]
            x_i_1 = pos[i][1]
            x_j_0 = pos[j][0]
            x_j_1 = pos[j][1]
            coef = f"- 1 * [862690 / (4 * ((({x_i_0}) - ({x_j_0}))**2+(({x_i_1}) - ({x_j_1}))**2) ** 3)]"
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
        local_ubs[f"delta"] = 20
        local_lbs[f"delta"] = -20
        local_ubs[f"omega"] = 2.5
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

def gen_rydberg2D(n):
    # Rydberg system Hamiltonian
    pos = gen_pos(n)
    term1 = ZZ(n, pos)
    term2 = Z(n, pos)
    ham_sys = term1 + " + " + term2

    # Local laser Hamiltonian and its bound
    ham_local = laser(n)
    local_ubs, local_lbs = laser_bs(n)

    # generate the operator list
    # op_list = gen_op_list(n)

    return [ham_sys, ham_local, local_ubs, local_lbs]
