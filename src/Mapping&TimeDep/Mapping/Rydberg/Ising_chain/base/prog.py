import time
import argparse
import pandas as pd
from simuq.systems.benchmark.ising_chain import GenQS
from simuq.solver import *
from simuq.aais.rydberg1d import generate_qmachine

parser = argparse.ArgumentParser(description="Parse system size and evolution time parameters.")

# Define the parameters with default values
parser.add_argument('--N', type=int, default=3, help='Specify the system size N')
parser.add_argument('--J', type=float, default=1.0, help='Specify the interaction strength J')
parser.add_argument('--h', type=float, default=1.0, help='Specify the interaction strength h')
parser.add_argument('--T', type=int, default=1, help='Specify the evolution time T')
parser.add_argument('--F', type=str, default="result_base.csv", help='Specify the file name to put result')

# Parse the arguments
args = parser.parse_args()

# Access the parameters
N = args.N
J = args.J
h = args.h
T = args.T
output_file = args.F

# generate Ising chain 
qs = GenQS(N, T, J, h)

# generate a Rydberg machine
mach = generate_qmachine(N)
mach.instantiate()
mach.extend_instruction_sites()


t0 = time.time()
result = align(0, [0] * qs.num_sites, qs, mach, solver="least_squares", solver_args={"tol": 10, "time_penalty": 0}, verbose = 0)
t1 = time.time()
t_compile = t1-t0

if result == False:
    info_ = [N, J, h, T]
    # write down the result to csv file
    result = [info_, "None", "None", "None", "None", "None"]
    columns = ["Size N / J / h / Evol T", " Compilation Time", " Alignment", " Execution Time", " Error", " solution"]  
    df = pd.DataFrame([result], columns=columns)

    # Append to the CSV file without headers (after the first write)
    df.to_csv(output_file, mode='a', header=not pd.io.common.file_exists(output_file), index=False)

else:
    _, info, ali = result

    info_syn = info[:4]
    info_syn.append(['t_exe: ', info[1][1]*(1+N*2)])

    info_ = [N, J, h, T]

    # write down the result to csv file
    result = [info_, info_syn[0][1], ali, info_syn[2][1][0], info_syn[1][1], info_syn[3][1]]
    columns = ["Size N / J / h / Evol T", " Compilation Time", " Alignment", " Execution Time", " Error", " solution"]  
    df = pd.DataFrame([result], columns=columns)

    # Append to the CSV file without headers (after the first write)
    df.to_csv(output_file, mode='a', header=not pd.io.common.file_exists(output_file), index=False)
