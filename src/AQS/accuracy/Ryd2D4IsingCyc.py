import numpy as np

# Function that calculate the solution accuracy by comparing the Hamiltonain
def acc(n, sol, t_evol, T):

    C_6 = 862690 
    reses = 0

    for i in range(n - 1):
        x_i_0 = sol[f"x_{i}_0"]
        x_i_1 = sol[f"x_{i}_1"]
        for j in range(i + 1, n):
            x_j_0 = sol[f"x_{j}_0"]
            x_j_1 = sol[f"x_{j}_1"]
            z_iz_j = C_6 / ( 4 * ((x_i_0 - x_j_0)**2+(x_i_1 - x_j_1)**2) ** 3 )
            if j-i == 1 or j-i == n-1:
                reses = reses + abs(z_iz_j * t_evol - 0.5 * T) 
            else:
                reses = reses + abs(z_iz_j * t_evol) 

    for i in range(n):
        z_ = 0
        x_i_0 = sol[f"x_{i}_0"]
        x_i_1 = sol[f"x_{i}_1"]
        for j in range(i):
            x_j_0 = sol[f"x_{j}_0"]
            x_j_1 = sol[f"x_{j}_1"]
            z_ = z_ - C_6 / ( 4 * ((x_j_0 - x_i_0)**2+(x_j_1 - x_i_1)**2) ** 3 )
        for j in range(i+1, n):
            x_j_0 = sol[f"x_{j}_0"]
            x_j_1 = sol[f"x_{j}_1"]
            z_ = z_ - C_6 / ( 4 * ((x_i_0 - x_j_0)**2+(x_i_1 - x_j_1)**2) ** 3 )
        d_i = sol[f"delta{i}"]
        z_ = (z_ + d_i/2) * t_evol
        reses = reses + abs(z_)
    
    for i in range(n):
        omega_i = sol[f"omega{i}"]
        phi_i = sol[f"phi{i}"]
        x_ = omega_i/2 * np.cos(phi_i) * t_evol
        y_ = - omega_i/2 * np.sin(phi_i) * t_evol
        reses = reses + abs(x_ - T) + abs(y_ - 0)

    return reses