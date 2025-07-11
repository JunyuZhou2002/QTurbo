import subprocess

file_name = "../result/result_opt.csv"

# Define ranges or lists of values for N and T
N_values = [i for i in range(3, 99, 9)]
U_values = [1]
w_values = [1]
a_values = [1]
T_values = [1]   
D_values = [4]   

# Loop over all combinations of N and T
for N in N_values:
    for U in U_values:
        for w in w_values:
            for a in a_values:
                for T in T_values:
                    for D in D_values:
                        # Construct the command
                        command = ["python3", "prog.py", "--N", str(N), "--U", str(U), "--w", str(w), "--a", str(a), "--T", str(T), "--D", str(D), "--F", file_name]
                        print(f"Running experiment with N={N}, T={T}")
            
                        # Execute the command
                        subprocess.run(command)