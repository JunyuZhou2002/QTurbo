import subprocess

file_name = "../result/result_opt.csv"

# Define ranges or lists of values for N and T
N_values = [i for i in range(3, 99, 9)]
M_values = [1]
t_values = [1]
h_values = [1]
T_values = [1]   

# Loop over all combinations of N and T
for N in N_values:
    for M in M_values:
        for t in t_values:
            for h in h_values:
                for T in T_values:
                    # Construct the command
                    command = ["python3", "prog.py", "--N", str(N), "--M", str(M), "--t", str(t), "--h", str(h), "--T", str(T), "--F", file_name]
                    print(f"Running experiment with N={N}, T={T}")
        
                    # Execute the command
                    subprocess.run(command)