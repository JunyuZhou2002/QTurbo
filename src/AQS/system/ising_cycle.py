# fuction to define the Hamiltonian of Ising cycle
def ising_cycle(n, J, h, T):

    Ising = {}

    # Generate the 'Z{i}*Z{i+1}' terms
    for i in range(0, n-1):
        Ising[f'Z{i}Z{i+1}'] = J*T
    Ising[f'Z{0}Z{n-1}'] = J*T

    # Generate the 'X{i}' terms
    for i in range(0, n):
        Ising[f'X{i}'] = h*T
        
    return Ising