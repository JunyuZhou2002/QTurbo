import subprocess

# Timeout settings (in seconds)
EXP_TIMEOUT = 10000000
SORT_TIMEOUT = 10  
RESULT_TIMEOUT = 10 

def run_with_timeout(cmd, cwd, timeout, description):
    """Run command with timeout and error handling"""
    try:
        print(f"Running: {description}")
        result = subprocess.run(cmd, cwd=cwd, timeout=timeout, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ SUCCESS: {description}")
        else:
            print(f"✗ FAILED: {description} (exit code: {result.returncode})")
    except subprocess.TimeoutExpired:
        print(f"⏱ TIMEOUT: {description} (exceeded {timeout}s)")
    except Exception as e:
        print(f"✗ ERROR: {description} - {e}")

# Run Ising chain model
run_with_timeout(["python3", "exp.py"], "Overall/Heisenberg/Ising_chain/base", EXP_TIMEOUT, "Ising chain base exp.py")
run_with_timeout(["python3", "exp.py"], "Overall/Heisenberg/Ising_chain/opt", EXP_TIMEOUT, "Ising chain opt exp.py")
run_with_timeout(["python3", "sort.py"], "Overall/Heisenberg/Ising_chain/result", SORT_TIMEOUT, "Ising chain sort.py")
run_with_timeout(["python3", "result.py"], "Overall/Heisenberg/Ising_chain/result", RESULT_TIMEOUT, "Ising chain result.py")

# Run Ising cycle model
run_with_timeout(["python3", "exp.py"], "Overall/Heisenberg/Ising_cycle/base", EXP_TIMEOUT, "Ising cycle base exp.py")
run_with_timeout(["python3", "exp.py"], "Overall/Heisenberg/Ising_cycle/opt", EXP_TIMEOUT, "Ising cycle opt exp.py")
run_with_timeout(["python3", "sort.py"], "Overall/Heisenberg/Ising_cycle/result", SORT_TIMEOUT, "Ising cycle sort.py")
run_with_timeout(["python3", "result.py"], "Overall/Heisenberg/Ising_cycle/result", RESULT_TIMEOUT, "Ising cycle result.py")

# Run Kitaev model
run_with_timeout(["python3", "exp.py"], "Overall/Heisenberg/Kitaev/base", EXP_TIMEOUT, "Kitaev base exp.py")
run_with_timeout(["python3", "exp.py"], "Overall/Heisenberg/Kitaev/opt", EXP_TIMEOUT, "Kitaev opt exp.py")
run_with_timeout(["python3", "sort.py"], "Overall/Heisenberg/Kitaev/result", SORT_TIMEOUT, "Kitaev sort.py")
run_with_timeout(["python3", "result.py"], "Overall/Heisenberg/Kitaev/result", RESULT_TIMEOUT, "Kitaev result.py")

# Run Heisenberg chain model
run_with_timeout(["python3", "exp.py"], "Overall/Heisenberg/heis_chain/base", EXP_TIMEOUT, "Heisenberg chain base exp.py")
run_with_timeout(["python3", "exp.py"], "Overall/Heisenberg/heis_chain/opt", EXP_TIMEOUT, "Heisenberg chain opt exp.py")
run_with_timeout(["python3", "sort.py"], "Overall/Heisenberg/heis_chain/result", SORT_TIMEOUT, "Heisenberg chain sort.py")
run_with_timeout(["python3", "result.py"], "Overall/Heisenberg/heis_chain/result", RESULT_TIMEOUT, "Heisenberg chain result.py")

