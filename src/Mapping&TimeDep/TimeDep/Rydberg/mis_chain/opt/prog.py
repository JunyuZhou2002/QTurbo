from AQS.compiler import *
from AQS.system.mis_chain import *
from AQS.simulator.rydberg1D import *

##############################################################################################################

import argparse
parser = argparse.ArgumentParser(description="Parse system size and evolution time parameters.")

# Define the parameters with default values
parser.add_argument('--N', type=int, default=3, help='Specify the system size N')
parser.add_argument('--U', type=float, default=1.0, help='Specify the interaction strength U')
parser.add_argument('--w', type=float, default=1.0, help='Specify the interaction strength w')
parser.add_argument('--a', type=float, default=1.0, help='Specify the interaction strength a')
parser.add_argument('--T', type=int, default=1, help='Specify the evolution time T')
parser.add_argument('--D', type=int, default=4, help='Specify the discretization number D')
parser.add_argument('--F', type=str, default="result_opt.csv", help='Specify the file name to put result')

# Parse the arguments
args = parser.parse_args()

# Access the parameters
N = args.N
U = args.U
w = args.w
a = args.a
T = args.T
D = args.D
output_file = args.F

##############################################################################################################

# Hamiltonian of MIS chain
models = mis_chain(N, U, w, a, T, D)

# Rydberg2D machine
machine = gen_rydberg1D(N)
init_fun = init_gen(a/4, T/D, N)

t_compiles, t_evols, sols, reses = time_dependent(models, machine, 1, init_fun)

##############################################################################################################

import pandas as pd

info = [N, U, w, a, T, D]

def round_to_sigfigs(num, sigfigs=6, threshold=1e-6):
    if abs(num) < threshold:
        return 0.0
    return float(np.round(num, sigfigs - int(np.floor(np.log10(abs(num)))) - 1))

t_compile = round_to_sigfigs(t_compiles, sigfigs=6)
t_evols = sum([round_to_sigfigs(t_evol, sigfigs=6) for t_evol in t_evols])
res = round_to_sigfigs(reses, sigfigs=6)
sols = [{key: round_to_sigfigs(value) for key, value in sol.items()} for sol in sols]

# write down the result to csv file
result = [info, t_compile, t_evols, res, sols]
columns = ["Size N / U / w / a / Evol T/ Dis D", " Compilation Time", " Execution Time", " Error", " solution"]  
df = pd.DataFrame([result], columns=columns)

# Append to the CSV file without headers (after the first write)
df.to_csv(output_file, mode='a', header=not pd.io.common.file_exists(output_file), index=False)
