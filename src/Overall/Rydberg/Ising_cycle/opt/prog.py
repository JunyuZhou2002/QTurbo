from AQS.compiler import *
from AQS.system.ising_cycle import *
from AQS.simulator.rydberg2D import *
from AQS.accuracy.Ryd2D4IsingCyc import *

##############################################################################################################

import argparse
parser = argparse.ArgumentParser(description="Parse system size and evolution time parameters.")

# Define the parameters with default values
parser.add_argument('--N', type=int, default=3, help='Specify the system size N')
parser.add_argument('--J', type=float, default=1.0, help='Specify the interaction strength J')
parser.add_argument('--h', type=float, default=1.0, help='Specify the interaction strength h')
parser.add_argument('--T', type=int, default=1, help='Specify the evolution time T')
parser.add_argument('--F', type=str, default="result_opt.csv", help='Specify the file name to put result')

# Parse the arguments
args = parser.parse_args()

# Access the parameters
N = args.N
J = args.J
h = args.h
T = args.T
output_file = args.F

##############################################################################################################

# Hamiltonian of Ising cycle
model = ising_cycle(N, J, h, T)

# Rydberg2D machine
machine = gen_rydberg2D(N)
init_fun = init_gen_cyc(J, T, N)

t_compile, t_evol, sol, res = operation(model, machine, init_fun)
sol = amp_adjust(sol)
# res_new = acc(N, sol, t_evol, T)

##############################################################################################################

import pandas as pd

info = [N, J, h, T]

def round_to_sigfigs(num, sigfigs=6, threshold=1e-6):
    if abs(num) < threshold:
        return 0.0
    return float(np.round(num, sigfigs - int(np.floor(np.log10(abs(num)))) - 1))

t_compile = round_to_sigfigs(t_compile, sigfigs=6)
t_evol = round_to_sigfigs(t_evol, sigfigs=6)
res = round_to_sigfigs(res, sigfigs=6)
sol = {key: round_to_sigfigs(value) for key, value in sol.items()}

# write down the result to csv file
result = [info, t_compile, t_evol, res, sol]
columns = ["Size N / J / h / Evol T", " Compilation Time", " Execution Time", " Error", " solution"]  
df = pd.DataFrame([result], columns=columns)

# Append to the CSV file without headers (after the first write)
df.to_csv(output_file, mode='a', header=not pd.io.common.file_exists(output_file), index=False)
