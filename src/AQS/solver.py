import time
import numpy as np
import networkx as nx # type: ignore
from scipy.optimize import least_squares # type: ignore


# linear system generation
# the column is indexed by the order of global/local_var_syn
def gen_lin_sys(H_tar, op_list, global_var_syn, machine_sys, local_var_syn, machine_local):

    # Register the linear system, #row = #HamTerm, #column = #(global+local) variable 
    lin_sys = np.zeros((len(op_list),len(global_var_syn)+len(local_var_syn)))
    b = np.zeros((len(op_list),1))

    # calculate the vector b in Ax=b
    for i in range(len(op_list)):
        if op_list[i] in H_tar:
            b[i] = H_tar[op_list[i]]

    # calculate the matrix A in Ax=b
    for i in range(len(op_list)):
        op = op_list[i]

        # search in system Hamiltonian
        if op in machine_sys:
            var_dep = machine_sys[op]
            if len(var_dep) == 1:
                lin_sys[i, var_dep[0][0]] = var_dep[0][1]
            else:
                for item in var_dep:
                    lin_sys[i, item[0]] = item[1]
        
        # search in local laser   
        if op in machine_local:
            var_dep = machine_local[op]
            if len(var_dep) == 1:
                lin_sys[i, var_dep[0][0]+len(global_var_syn)] = var_dep[0][1]
            else:
                for item in var_dep:
                    lin_sys[i, item[0]+len(global_var_syn)] = item[1]

    return lin_sys, b


# variable dependency analysis
# This function returning the connected components, each components has the form:
# [array1 for dependent syn_variables, array2 for dependent ori_variables]
def classifier(var_syn):

    # Define the graph using edges
    edges = []
    for i, term_dep in enumerate(var_syn):
        for j in term_dep[1]:
            edges.append((i, len(var_syn) + j))

    G = nx.Graph()
    G.add_edges_from(edges)

    # Find connected components
    connected_compo = list(nx.connected_components(G))

    connected = []
    for i, compo in enumerate(connected_compo):
        compo_list = np.array(list(compo))
        compo_list_sort1 = compo_list[compo_list < len(var_syn)]
        compo_list_sort2 = compo_list[compo_list >= len(var_syn)] - len(var_syn)
        connected.append([compo_list_sort1, compo_list_sort2])

    return connected

def gen_op_classifier(machine_ins, var_syn):

    # Define the graph using edges
    edges = []
    idx = 0
    for _, dep_ls in machine_ins.items():
        for sub_ls in dep_ls:
            edges.append((idx, len(machine_ins) + sub_ls[0]))
        idx = idx + 1

    for i, term_dep in enumerate(var_syn):
        for j in term_dep[1]:
            edges.append((len(machine_ins) + i, len(machine_ins) + len(var_syn) + j))

    G = nx.Graph()
    G.add_edges_from(edges)

    # Find connected components
    connected_compo = list(nx.connected_components(G))

    connected = []
    for i, compo in enumerate(connected_compo):
        compo_list = np.array(list(compo))
        compo_list_sort = compo_list[compo_list < len(machine_ins)]
        connected.append(compo_list_sort.tolist())

    machine_ins_ls = [key for key in machine_ins]

    return connected, machine_ins_ls

##################################################################################
# in the second round of optimization, I want to only optimized for the amplitude variables
# and only merge the amplitude variables
##################################################################################
# local mixed equation system builder, the solution is value of  Amp*Time
def eq_builder(connected, var_syn, var, x, init=None):
    
    compile_time = 0
    var_sol_dict = {string: 0 for string in var}
    error = np.zeros(len(var_syn))

    init_flag = 1
    if init is None:
        init_flag = 0

    # f_soles = []

    for i, component in enumerate(connected):
    
        # component[0] is an array describe which term in the var_syn we are consider
        # component[1] is an array describe which term in the var we are consider
        var_str = ''
        for j in range(len(component[1])):
            if j == 0:
                var_str = var_str + var[component[1][j]]
            else:
                var_str = var_str + ', ' + var[component[1][j]]
        
        eqs = []

        for k in range(len(component[0])):
            eqs.append(eval("lambda " + var_str + ": " + var_syn[component[0][k]][0] + " - " + str(x[component[0][k]][0])))
            # print("lambda " + var_str + ": " + var_syn[component[0][k]][0] + " - " + str(x[component[0][k]][0]))

        def mixed_eq(vars, equations):
            return [eq(*vars) for eq in equations]
        
        if init_flag == 0:
            init_ = [0.3 for d in range(len(component[1]))]
        else:
            init_ = init[i]

        time1 = time.time()
        result = least_squares(mixed_eq, init_, args=[eqs])
        time2 = time.time()
        # print(result.x)

        compile_time = compile_time + (time2 - time1)
        for j in range(len(component[1])):
            var_sol_dict[var[component[1][j]]] = result.x[j]

        f_sol = mixed_eq(result.x, eqs)
        # f_soles.append(f_sol)

        for i, k in enumerate(component[0]):
            error[k] = f_sol[i]

    return compile_time, var_sol_dict, error

def eq_builder_opt(connected, var_syn, var, x, local_ubs, local_evo_dic, init=None):
    
    compile_time = 0
    var_sol_dict = {string: 0 for string in var}
    error = np.zeros(len(var_syn))

    local_evo_dic_new = {key: value for key, value in local_evo_dic.items() if key not in local_ubs}

    init_flag = 1
    if init is None:
        init_flag = 0

    # f_soles = []

    for i, component in enumerate(connected):
    
        # component[0] is an array describe which term in the var_syn we are consider
        # component[1] is an array describe which term in the var we are consider
        var_str = ''
        var_count = 0
        for j in range(len(component[1])):

            if len(var_str)==0:
                if var[component[1][j]] in local_ubs:
                    var_str = var_str + var[component[1][j]]
                    var_count = var_count + 1
            else:
                if var[component[1][j]] in local_ubs:
                    var_str = var_str + ', ' + var[component[1][j]]
                    var_count = var_count + 1
        
        eqs = []

        for k in range(len(component[0])):
            for key, value in local_evo_dic_new.items():
                var_syn[component[0][k]][0] = var_syn[component[0][k]][0].replace(key, str(value))
            eqs.append(eval("lambda " + var_str + ": " + var_syn[component[0][k]][0] + " - " + str(x[component[0][k]][0])))
            # print("lambda " + var_str + ": " + var_syn[component[0][k]][0] + " - " + str(x[component[0][k]][0]))

        def mixed_eq(vars, equations):
            return [eq(*vars) for eq in equations]
        
        if init_flag == 0:
            init_ = [0.3 for d in range(var_count)]
        else:
            init_ = init[i]

        time1 = time.time()
        result = least_squares(mixed_eq, init_, args=[eqs])
        time2 = time.time()

        compile_time = compile_time + (time2 - time1)
        count = 0
        for j in range(len(component[1])):
            if var[component[1][j]] in local_ubs:
                var_sol_dict[var[component[1][j]]] = result.x[count]
                count = count + 1

        f_sol = mixed_eq(result.x, eqs)
        # f_soles.append(f_sol)

        for i, k in enumerate(component[0]):
            error[k] = f_sol[i]

    return compile_time, var_sol_dict, error

def eq_builder_with_global(connected, var_syn, var, x, global_sol):
    
    compile_time = 0
    error = np.zeros(len(var_syn))

    for i, component in enumerate(connected):
    
        # component[0] is an array describe which term in the var_syn we are consider
        # component[1] is an array describe which term in the var we are consider
        var_str = 't'
        eqs = []

        for k in range(len(component[0])):
            for key, value in global_sol.items():
                var_syn[component[0][k]][0] = var_syn[component[0][k]][0].replace(key, str(value))
            eqs.append(eval("lambda " + var_str + ": " + var_syn[component[0][k]][0] + " * t " + " - " + str(x[component[0][k]][0])))
            # print("lambda " + var_str + ": " + var_syn[component[0][k]][0] + " * t " + " - " + str(x[component[0][k]][0]))

        def mixed_eq(vars, equations):
            return [eq(*vars) for eq in equations]
        
        init = 1
        time1 = time.time()
        result = least_squares(mixed_eq, init, args=[eqs])
        time2 = time.time()
        t_global  =result.x

        compile_time = compile_time + (time2 - time1)
        f_sol = mixed_eq(result.x, eqs)
        # f_soles.append(f_sol)

        for i, k in enumerate(component[0]):
            error[k] = f_sol[i]

    return compile_time, t_global, error


# Calculate the evolution time for each instruction 
# using the upper/lower bound of the control amplitude
def local_time(local_ubs, local_lbs, local_var_sol_dict):

    local_evo_dic = {}
    time_local_evo = 0

    for control in local_var_sol_dict:
        if control in local_ubs:
            t1 = time.time()
            if local_var_sol_dict[control]>=0 and local_ubs[control] > 0:
                local_evo_dic[control] = local_var_sol_dict[control]/local_ubs[control]
            elif local_var_sol_dict[control]<0 and local_lbs[control] < 0:
                local_evo_dic[control] = local_var_sol_dict[control]/local_lbs[control]
            else: 
                print("Caution: the evolution time does not exist for local instruction!")
            t2 = time.time()
            time_local_evo = time_local_evo + (t2 - t1)

    t_global = max(local_evo_dic.values())

    return t_global, time_local_evo


# Calculate the global evolution time for all local instruction
def local_evo(t_evol, local_ubs, local_var_sol_dict):

    local_evo_dic_post = {}
    time_local_evo_post = 0

    for control in local_var_sol_dict:
        if control in local_ubs:
            t1 = time.time()
            local_evo_dic_post[control] = local_var_sol_dict[control]/t_evol
            t2 = time.time()
            time_local_evo_post = time_local_evo_post + (t2 - t1)

    return local_evo_dic_post, time_local_evo_post


# This function help merge the solution dictionary
def merge_dic(dict1, dict2, flag=None):

    if flag==1 :
        for key, value in dict1.items():
            dict2.setdefault(key, value)
        merged_dict = dict2
        return merged_dict
    merged_dict = {}
    for key in set(dict1.keys()).union(dict2.keys()):
        merged_dict[key] = dict1.get(key, 0) + dict2.get(key, 0)
    merged_dict = {key: merged_dict[key] for key in sorted(merged_dict)}

    return merged_dict
