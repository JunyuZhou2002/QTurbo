# fuction to define the Hamiltonian of Ising cycle next nearst neighbor model
def ising_cycle_plus(n, J, h, T):

    target = {}

    # Generate the 'Z{i}*Z{i+1}' terms
    for i in range(0, n-1):
        target[f'Z{i}Z{i+1}'] = J*T
    target[f'Z{0}Z{n-1}'] = J*T

    # Generate the 'Z{i}*Z{i+2}' terms
    for i in range(0, n-2):
        target[f'Z{i}Z{i+2}'] = (J/2**6)*T
    target[f'Z{0}Z{n-2}'] = (J/2**6)*T
    target[f'Z{1}Z{n-1}'] = (J/2**6)*T

    # Generate the 'X{i}' terms
    for i in range(0, n):
        target[f'X{i}'] = h*T
        
    return target