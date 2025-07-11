# fuction to define the Hamiltonian of Kitaev
def kitaev(n, miu, t, h, T):
    target = {}
    # Generate the 'Z{i}*Z{i+1}' terms
    for i in range(0, n-1):
        target[f'Z{i}Z{i+1}'] = (miu/2)*T
    # Generate the 'X{i}' terms
    for i in range(0, n):
        target[f'X{i}'] = -t*T
    # Generate the 'Z{i}' terms
    for i in range(0, n):
        target[f'Z{i}'] = -h*T
    return target