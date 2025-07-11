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

# Run mapping experiment
run_with_timeout(["python3", "exp.py"], "Mapping&TimeDep/Mapping/Rydberg/Ising_chain/base", EXP_TIMEOUT, "mapping base exp.py")
run_with_timeout(["python3", "exp.py"], "Mapping&TimeDep/Mapping/Rydberg/Ising_chain/opt", EXP_TIMEOUT, "mapping opt exp.py")
run_with_timeout(["python3", "sort.py"], "Mapping&TimeDep/Mapping/Rydberg/Ising_chain/result", SORT_TIMEOUT, "mapping sort.py")
run_with_timeout(["python3", "result.py"], "Mapping&TimeDep/Mapping/Rydberg/Ising_chain/result", RESULT_TIMEOUT, "mapping result.py")

# Run time dependent simulation experiment
run_with_timeout(["python3", "exp.py"], "Mapping&TimeDep/TimeDep/Rydberg/mis_chain/base", EXP_TIMEOUT, "time dependent experiment base exp.py")
run_with_timeout(["python3", "exp.py"], "Mapping&TimeDep/TimeDep/Rydberg/mis_chain/opt", EXP_TIMEOUT, "time dependent experiment opt exp.py")
run_with_timeout(["python3", "sort.py"], "Mapping&TimeDep/TimeDep/Rydberg/mis_chain/result", SORT_TIMEOUT, "time dependent experiment sort.py")
run_with_timeout(["python3", "result.py"], "Mapping&TimeDep/TimeDep/Rydberg/mis_chain/result", RESULT_TIMEOUT, "time dependent experiment result.py")
