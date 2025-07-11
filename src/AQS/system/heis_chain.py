# fuction to define the Hamiltonian of Heisenberg chain
def heis_chain(n, J, h, T):
    target = {}
    # Generate the 'X{i}*X{i+1}' terms
    for i in range(0, n-1):
        target[f'X{i}X{i+1}'] = J*T
    # Generate the 'Y{i}*Y{i+1}' terms
    for i in range(0, n-1):
        target[f'Y{i}Y{i+1}'] = J*T
    # Generate the 'Z{i}*Z{i+1}' terms
    for i in range(0, n-1):
        target[f'Z{i}Z{i+1}'] = J*T
    # Generate the 'X{i}' terms
    for i in range(0, n):
        target[f'X{i}'] = h*T
    return target