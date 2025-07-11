# fuction to define the Hamiltonian of Heisenberg chain
def hydrogen(a, b, c, d, T):
    target = {}
    
    target['Z0'] = a*T
    target['Z1'] = b*T
    target['Z0Z1'] = c*T
    target['X0X1'] = d*T

    return target