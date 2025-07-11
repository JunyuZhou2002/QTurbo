import copy

# fuction to define the Hamiltonian of Ising chain
def ising_chain(n, J, h, T, ali=None):

    if ali == None:
        ali = [i for i in range(n)]

    Ising = {}
    # Generate the 'Z{i}*Z{i+1}' terms
    for i in range(0, n-1):
        Ising[f'Z{ali[i]}Z{ali[i+1]}'] = J*T
    # Generate the 'X{i}' terms
    for i in range(0, n):
        Ising[f'X{ali[i]}'] = h*T
    return Ising

# for mappping purpose
def tar_ham_list(N):
    id = "I" * N
    ls = []

    for i in range(N):
        id_cp = copy.deepcopy(id)
        id_x = id_cp[:i] + "X" + id_cp[i + 1:]
        ls.append(id_x)

    for i in range(0, N-1):
        id_cp = copy.deepcopy(id)
        id_zz = id_cp[:i] + "ZZ" + id_cp[i + 2:]
        ls.append(id_zz)

    return ls