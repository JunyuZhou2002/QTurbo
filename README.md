# QTurbo: A Robust and Efficient Compiler for Analog Quantum Simulation

Artifact for paper _QTurbo: A Robust and Efficient Compiler for Analog Quantum Simulation_

---

## System Requirement

**Hardware**:

* 40GB+ available hard drive
* 32GB+ RAM
* QuEra quantum device: Aquila (Access through Amazon Braket).

**Software**:

* Linux (Ubuntu 22.04 server is tested)
* Python 3.10+

## Setup

We will use Python virtual environment. To set up and activate the virtual environment under folder `src`:

```bash
python3 -m venv venv
source venv/bin/activate
```

Then, install necessary Python packages:

```bash
pip3 install -r requirements.txt
pip3 install -e .
```

You can now use your favorite frontend to execute the code (vscode, browser, etc.)

## Results

This section shows how to obtain result for each figure from the QTurbo paper.

**Figure 3**: Execute `python3 fig3.py` under folder `src`. The outputs will be placed in the folder `src/Overall/Rydberg/Hamiltonian_name (replace with the real one)/result`. The `Compilation Time` graph, `Execution Time` graph, and `Relative Error` graph are directly printed, and the reduction values can be found in `result.txt`.

**Figure 4**: Execute `python3 fig4.py` under folder `src`. The outputs will be placed in the folder `src/Overall/Heisenberg/Hamiltonian_name (replace with the real one)/result`. The `Compilation Time` graph, `Execution Time` graph, and `Relative Error` graph are directly printed, and the reduction values can be found in `result.txt`.

**Figure 5**: Execute `python3 fig5.py` under folder `src`. The outputs for Figure 5 (a) will be placed in the folder `src/Mapping&TimeDep/Mapping/Rydberg/Ising_chain/result`, and the outputs for Figure 5 (b) will be placed in the folder `src/Mapping&TimeDep/TimeDep/Rydberg/mis_chain/result`. The `Compilation Time` graph, `Execution Time` graph, and `Relative Error` graph are directly printed, and the reduction values can be found in `result.txt`.

**Figure 6 Real Experiment**: To reproduce Figure 6, you need a AWS account and use `Notebooks` feature under Amazon Braket. 
1) Execution: Please go to the folder `src/RealExp/result/Hamiltonian_name (replace with the real one)/`, you will find notebooks to be executed on hardware placed under different folder ladeled by target evolution time. For example, if you want the data point for 0.5us in Figure 6 (a), please go to the folder `src/RealExp/result/Ising_cycle/0.5`, `real_base.ipynb` will give you the data for SimuQ and `real_opt.ipynb` will give you the data for QTurbo. After the execution through Amazon Braket, please retrieve the `.json` file and named them as `BASE.json` and `OPT.json` respectively under the same folder. We placed our results for reference. 
2) Data processing: After get all the hardware data, you can process them in folder `src/RealExp/result/Hamiltonian_name (replace with the real one)/`. Run the `data_base_process.ipynb` and `data_opt_process.ipynb` seperately, and then run `data_datavisualization.ipynb`, this will directly produce the Figure 6.

**Note for real experiments**: 

1) The pulse amplitude and position data for hardware in `real_base.ipynb` and `real_opt.ipynb` are derived from the folder `src/RealExp/pulse_gen/Hamiltonian_name (replace with the real one)/`, please feel free to recompile and check them. The pulse amplitude and execution time should be the same, and we use 2D translation and rotation for the position data to fit the hardware. 
2) The `base.json`, `opt.json`, and `qutip.json` under `src/RealExp/result/Hamiltonian_name (replace with the real one)/` are simulation data using classical computer, you can directly generate them using the three notebooks under `src/RealExp/classical_sim/Hamiltonian_name (replace with the real one)/`.
3) To execute the notebooks in folder `src/RealExp/result/Hamiltonian_name (replace with the real one)/` and `src/RealExp/classical_sim/Hamiltonian_name (replace with the real one)/`, we need a new virtual environment, the `requirements.txt` can be found under `src/RealExp/`.


## Tutorial
This artifact contains the `tutorial.ipynb` notebook, which instructs users on the use of QTurbo.
