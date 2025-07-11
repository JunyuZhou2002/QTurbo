# fuction to define the Hamiltonian of mis chain
def mis_chain(n, U, w, a, T, D):

    target_ls = []
    Ts = T/D
    t_ls = [i*(T/D) for i in range(D)]
    
    for t in t_ls:
        target = {}

        # Generate the 'Z{i}*Z{i+1}' terms
        for i in range(0, n-1):
            target[f'Z{i}Z{i+1}'] = (a/4)*Ts

        # Generate the 'X{i}' terms
        for i in range(0, n):
            target[f'X{i}'] = (w/2)*Ts

        # Generate the 'Z{i}' terms
        for i in range(0, n):
            target[f'Z{i}'] = ((-1+2*t)*U/2-a/2)*Ts
        target['Z0'] = target['Z0'] + (a/4)*Ts
        target[f'Z{n-1}'] = target[f'Z{n-1}'] + (a/4)*Ts

        target_ls.append(target)

    return target_ls