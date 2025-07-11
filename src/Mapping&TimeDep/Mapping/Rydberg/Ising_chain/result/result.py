import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import FuncFormatter, PercentFormatter
import matplotlib.ticker as ticker

def to_percentage(y, position):
    return f'{y * 100:.0f}%'

formatter = FuncFormatter(to_percentage)

# Load data from CSV
df_base = pd.read_csv('result_base.csv')
df_opt = pd.read_csv('result_opt.csv')

N_values = [i for i in range(3, 99, 9)]
x_T = [1]   

base_color = "#d04a3f" 
opt_color = "#0033FF"

# Compilation time analysis
# vary size N
array_base = df_base[" Compilation Time"].to_numpy()
array_opt = df_opt[" Compilation Time"].to_numpy()

plt.figure(figsize=(6, 3.5))
plt.plot(N_values, array_opt, marker='x', markersize=12, markeredgewidth=2, linewidth=2, label='Opt', color=opt_color)
plt.plot(N_values, array_base, marker='o', markerfacecolor='none', markersize=12, markeredgewidth=2, linewidth=2, label='SimuQ', color=base_color)

plt.yscale('log')
plt.grid(True, linestyle='--', linewidth=1.0)
plt.xticks(fontsize=25)
custom_ticks = [10**-2, 10**0, 10**2]
plt.yticks(custom_ticks, [r'$10^{-2}$', r'$10^{0}$', r'$10^{2}$'], fontsize=25)
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(30))  
plt.savefig("Compile Time.png", format='png', dpi=300, bbox_inches='tight')

del_ls = []
for i in range(len(array_base)):
    if np.isnan(array_base[i]):
        del_ls.append(i)
array_base = np.delete(array_base, del_ls)
array_opt = np.delete(array_opt, del_ls)

result_value_1 = (sum(array_base)-sum(array_opt[:len(array_base)]))/sum(array_opt[:len(array_base)])


# Evolution time analysis
# vary size N
array_base = df_base[" Execution Time"].to_numpy()
array_opt = df_opt[" Execution Time"].to_numpy()

plt.figure(figsize=(6, 3.5))
plt.plot(N_values, array_opt, marker='x', markersize=12, markeredgewidth=2, linewidth=2, label='Opt', color=opt_color)
plt.plot(N_values, array_base, marker='o', markerfacecolor='none', markersize=12, markeredgewidth=2, linewidth=2, label='SimuQ', color=base_color)

# Labels and legend
plt.grid(True, linestyle='--', linewidth=1.0)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(30))  
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(0.9))  
plt.savefig("Evolution Time.png", format='png', dpi=300, bbox_inches='tight')

del_ls = []
for i in range(len(array_base)):
    if np.isnan(array_base[i]):
        del_ls.append(i)
array_base = np.delete(array_base, del_ls)
array_opt = np.delete(array_opt, del_ls)

result_value_2 = (sum(array_base)-sum(array_opt))/sum(array_base)*100

# Error analysis
# vary size N
array_base = df_base[" Error"].to_numpy()
array_opt = df_opt[" Error"].to_numpy()

for i in range(len(N_values[:len(array_base)])):
    array_base[i] = array_base[i]/(2 * N_values[i]-1)
for i in range(len(N_values[:len(array_opt)])):
    array_opt[i] = array_opt[i]/(2 * N_values[i]-1)

plt.figure(figsize=(6, 3.5))
plt.plot(N_values, array_opt*100, marker='x', markersize=12, markeredgewidth=2, linewidth=2, label='Opt', color=opt_color)
plt.plot(N_values, array_base*100, marker='o', markerfacecolor='none', markersize=12, markeredgewidth=2, linewidth=2, label='SimuQ', color=base_color)

# Labels and legend
plt.grid(True, linestyle='--', linewidth=1.0)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(decimals=1))
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(30))  
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(0.2)) 
plt.savefig("Error.png", format='png', dpi=300, bbox_inches='tight')

del_ls = []
for i in range(len(array_base)):
    if np.isnan(array_base[i]):
        del_ls.append(i)
array_base = np.delete(array_base, del_ls)
array_opt = np.delete(array_opt, del_ls)

result_value_3 = (sum(array_base)-sum(array_opt))/sum(array_base)*100

with open('result.txt', 'w') as f:
    f.write("Compilation Time Reduction:\n")
    f.write(f"{result_value_1:.6g} times faster\n")
    f.write("Execution Time Reduction:\n")
    f.write(f"{result_value_2:.6g}%\n")
    f.write("Error Reduction:\n")
    f.write(f"{result_value_3:.6g}%\n")



