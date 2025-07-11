# fuction to define the Hamiltonian of Ising chain
def pxp_array(n, J, h, T):

    PXP = {}
    # Generate the 'Z{i}*Z{i+1}' terms
    PXP[f'Z{0}'] = 0
    for i in range(0, n-1):
        PXP[f'Z{i}Z{i+1}'] = J*T
        PXP[f'Z{i}'] = PXP[f'Z{i}'] - J*T
        PXP[f'Z{i+1}'] = - J*T
    # Generate the 'X{i}' terms
    for i in range(0, n):
        PXP[f'X{i}'] = h*T
    return PXP