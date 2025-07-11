import time
import argparse
import pandas as pd
from simuq.systems.benchmark.mis_chain import GenQS
from simuq.solver import solve_aligned, generate_as
from simuq.aais.rydberg1d import generate_qmachine

parser = argparse.ArgumentParser(description="Parse system size and evolution time parameters.")

# Define the parameters with default values
parser.add_argument('--N', type=int, default=3, help='Specify the system size N')
parser.add_argument('--U', type=float, default=1.0, help='Specify the interaction strength U')
parser.add_argument('--w', type=float, default=1.0, help='Specify the interaction strength w')
parser.add_argument('--a', type=float, default=1.0, help='Specify the interaction strength a')
parser.add_argument('--T', type=int, default=1, help='Specify the evolution time T')
parser.add_argument('--D', type=int, default=4, help='Specify the discretization number D')
parser.add_argument('--F', type=str, default="result_base.csv", help='Specify the file name to put result')

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

# generate Ising chain 
qs = GenQS(N, U, w, a, T, D)

# generate a Rydberg machine
mach = generate_qmachine(N)
mach.instantiate()
mach.extend_instruction_sites()

# create a default layout
ali = [i for i in range(N)]

result = solve_aligned(
    ali, qs, mach, solver="least_squares", solver_args={"tol": 10, "time_penalty": 0}, verbose=0
)

if result == False:
    info_ = [N, U, w, a, T, D]
    # write down the result to csv file
    result = [info_, "None", "None", "None", "None"]
    columns = ["Size N / U / w / a / Evol T/ Dis D", " Compilation Time", " Execution Time", " Error", " solution"]  
    df = pd.DataFrame([result], columns=columns)

    # Append to the CSV file without headers (after the first write)
    df.to_csv(output_file, mode='a', header=not pd.io.common.file_exists(output_file), index=False)

else:
    _, info, ali = result

    info_syn = info[:4]
    info_syn.append(['t_exe: ', info[1][1]*(1+N*2)])

    info_ = [N, U, w, a, T, D]

    # write down the result to csv file
    result = [info_, info_syn[0][1], sum(info_syn[2][1]), info_syn[1][1], info_syn[3][1]]
    columns = ["Size N / U / w / a / Evol T/ Dis D", " Compilation Time", " Execution Time", " Error", " solution"]  
    df = pd.DataFrame([result], columns=columns)

    # Append to the CSV file without headers (after the first write)
    df.to_csv(output_file, mode='a', header=not pd.io.common.file_exists(output_file), index=False)
