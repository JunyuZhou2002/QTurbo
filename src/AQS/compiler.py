from AQS.parser import *
from AQS.solver import *

# the compiler
def operation(model, machine, init_fun=None, global_idx=None):

    ham_sys, ham_local, local_ubs, local_lbs = machine

    # Parsing the Hamiltonian
    if not ham_sys:
        global_var_syn = []
        machine_sys = {}
        ham_tol = ham_local
        machine_tol, var_syn, var = parsing(ham_tol)
    else:
        machine_sys, global_var_syn, global_var = parsing(ham_sys)
        ham_tol = ham_sys + " + " +  ham_local
        machine_tol, var_syn, var = parsing(ham_tol)

    machine_local, local_var_syn, local_var = parsing(ham_local)

    # generate the op_list
    connected, machine_ins_ls = gen_op_classifier(machine_tol, var_syn)
    op_list = []
    for pauli in model.keys():
        if pauli not in op_list:
            for sub_ins_ls in connected:
                if (machine_ins_ls.index(pauli)) in sub_ins_ls:
                    for i in sub_ins_ls:
                        op_list.append(machine_ins_ls[i])
                    break

    # generate the linear system
    lin_sys, b = gen_lin_sys(model, op_list, global_var_syn, machine_sys, local_var_syn, machine_local)
   
    # solve the equation
    t1 = time.time()
    x = np.linalg.lstsq(lin_sys, b, rcond=None)[0]
    # x = np.linalg.solve(lin_sys, b)
    t2 = time.time()
    time_lin_sys = t2 - t1
    res_linear = (np.dot(lin_sys, x)-(b)).reshape(-1)

    # start mixed equation analysis
    x_global = x[:len(global_var_syn)]
    x_local = x[len(global_var_syn):]

    # local variable
    local_connected = classifier(local_var_syn)
    # build and solve the local mixed equation for each component
    local_mixed_time, local_var_sol_dict, res_l = eq_builder(local_connected, local_var_syn, local_var, x_local)
    lin_sys_l = lin_sys[:, -len(local_var_syn):]
    res_b_l = np.dot(lin_sys_l, res_l)
    # calculate the evolution for local variable, if they control the evolution
    t_global, time_local_time = local_time(local_ubs, local_lbs, local_var_sol_dict)
    local_evo_dic, time_local_evo = local_evo(t_global, local_ubs, local_var_sol_dict)
    local_evo_dic = merge_dic(local_var_sol_dict, local_evo_dic, 1)

    if not ham_sys:
        t_compile = time_lin_sys + local_mixed_time + time_local_evo
        t_evol = t_global
        sol = local_evo_dic
        res = res_linear + res_b_l
        res_l1 = np.linalg.norm(res, ord=1)
        return t_compile, t_evol, sol, res_l1

    ###########################################################################
    # once we get t_global, we can have a better guess for initial value
    if init_fun == None:
        global_init = [10 for i in range(len(global_var))]
    else:
        global_init = init_fun(t_global, global_var)
    ###########################################################################

    # global variable
    global_connected = classifier(global_var_syn)
    # build and solve the global mixed equation for each component
    global_mixed_time, global_var_sol_dict, res_g = eq_builder(global_connected, global_var_syn, global_var, x_global/t_global, global_init)
    res_g = res_g * t_global
    
    if global_idx == 1:
        return global_var_sol_dict
  
    # local variable optimization
    t1 = time.time()
    lin_sys_g = lin_sys[:, :len(global_var_syn)]
    res_b_g = np.dot(lin_sys_g, res_g)
    update_l = np.linalg.lstsq(lin_sys_l, -res_b_g, rcond=None)[0]
    res_linear_new = np.dot(lin_sys_l, update_l)-(-res_b_g)
    update_l = [[x] for x in update_l]
    t2 = time.time()
    t_relax = t2-t1

    local_mixed_time_new, local_var_sol_dict_new, res_l_new = eq_builder_opt(local_connected, local_var_syn, local_var, update_l/t_global, local_ubs, local_evo_dic, init=None)
    res_l_new = res_l_new * t_global
    res_b_l_new = np.dot(lin_sys_l, res_l_new)

    t_relax = t_relax + local_mixed_time_new

    sol_local = merge_dic(local_var_sol_dict_new, local_evo_dic)
    sol = merge_dic(global_var_sol_dict, sol_local)

    res = res_linear + (res_b_l+res_b_g) + (res_linear_new-res_b_g) + res_b_l_new

    res_l1 = np.linalg.norm(res, ord=1)

    t_evol = t_global

    # result analysis
    # Compilation time
    t_compile = time_lin_sys + local_mixed_time + time_local_time + time_local_evo + global_mixed_time + t_relax
    # Evolution time
    t_evol = t_global

    return t_compile, t_evol, sol, res_l1


# for mapping purpose, the same as simuq
# ali is a map, from system to simulator, have the same size of system
def align(i, ali, N, model_ls, sys_ls):

    def is_id(h, N):
        ret = True
        for i in range(N):
            if not h[i] == "I":
                ret = False
                break
        return ret

    if i == N:
        return ali
    
    for map_i in range(N):
        available = True
        ali[i] = map_i
        for j in range(i):
            if ali[j] == map_i:
                available = False
                break
        if not available:
            continue
        for h in model_ls:
            for ins in sys_ls:
                if is_id(ins, N):
                    continue
                found = False
                ins_partial_match = True
                for k in range(i + 1):
                    if h[k] != ins[ali[k]]:
                        ins_partial_match = False
                if ins_partial_match:
                    found = True
                    break
            if not found:
                available = False
                break
        if available:
            result =  align(i + 1, ali, N, model_ls, sys_ls)
            return result
    return False


# for time dependent case
def time_dependent(models, machine, ham_sys_ind, init_fun=None):

    if ham_sys_ind == 0:
        t_compiles = 0
        t_evols = []
        sols = []
        res_l1s = 0
        for model in models:
            t_compile, t_evol, sol, res_l1 = operation(model, machine, init_fun=None)
            t_compiles = t_compiles + t_compile
            t_evols.append(t_evol)
            sols.append(sol)
            res_l1s = res_l1s + res_l1
        return t_compiles, t_evols, sols, res_l1s
    
    t0 = time.time()
    global_sol = find_global_var(models, machine, init_fun)
    t1 = time.time()
    t_compiles = t1-t0

    t_evols = []
    sols = []
    res_l1s = 0

    for model in models:
        t_compile, t_evol, sol, res_l1 = operation_with_global(model, machine, global_sol)
        t_compiles = t_compiles + t_compile
        t_evols.append(t_evol)
        sols.append(sol)
        res_l1s = res_l1s + res_l1

    return t_compiles, t_evols, sols, res_l1s


def find_global_var(models, machine, init_fun=None):

    def round_to_sigfigs(num, sigfigs=6, threshold=1e-6):
        if abs(num) < threshold:
            return 0.0
        return float(np.round(num, sigfigs - int(np.floor(np.log10(abs(num)))) - 1))

    powers = []

    for model in models:
        ham_sys, ham_local, local_ubs, local_lbs = machine
        machine_sys, global_var_syn, global_var = parsing(ham_sys)
        ham_tol = ham_sys + " + " +  ham_local
        machine_tol, var_syn, var = parsing(ham_tol)
        machine_local, local_var_syn, local_var = parsing(ham_local)

        # generate the op_list
        connected, machine_ins_ls = gen_op_classifier(machine_tol, var_syn)
        op_list = []
        for pauli in model.keys():
            if pauli not in op_list:
                for sub_ins_ls in connected:
                    if (machine_ins_ls.index(pauli)) in sub_ins_ls:
                        for i in sub_ins_ls:
                            op_list.append(machine_ins_ls[i])
                        break

        # generate the linear system
        lin_sys, b = gen_lin_sys(model, op_list, global_var_syn, machine_sys, local_var_syn, machine_local)
    
        # solve the equation
        x = np.linalg.lstsq(lin_sys, b, rcond=None)[0]

        # start mixed equation analysis
        x_global = x[:len(global_var_syn)]
        x_local = x[len(global_var_syn):]

        # local variable
        local_connected = classifier(local_var_syn)
        # build and solve the local mixed equation for each component
        local_mixed_time, local_var_sol_dict, res_l = eq_builder(local_connected, local_var_syn, local_var, x_local)
        # calculate the evolution for local variable, if they control the evolution
        t_global, time_local_time = local_time(local_ubs, local_lbs, local_var_sol_dict)
        power = [round_to_sigfigs(x, sigfigs=6) for x in x_global/t_global]
        powers.append(power)

    powers = [sum(power) for power in powers]
    idx = powers.index(min(powers))

    model = models[idx]
    global_sol = operation(model, machine, init_fun, global_idx=1)

    return global_sol


# the compiler
def operation_with_global(model, machine, global_sol):

    ham_sys, ham_local, local_ubs, local_lbs = machine
    
    machine_sys, global_var_syn, global_var = parsing(ham_sys)
    ham_tol = ham_sys + " + " +  ham_local
    machine_tol, var_syn, var = parsing(ham_tol)

    machine_local, local_var_syn, local_var = parsing(ham_local)

    # generate the op_list
    connected, machine_ins_ls = gen_op_classifier(machine_tol, var_syn)
    op_list = []
    for pauli in model.keys():
        if pauli not in op_list:
            for sub_ins_ls in connected:
                if (machine_ins_ls.index(pauli)) in sub_ins_ls:
                    for i in sub_ins_ls:
                        op_list.append(machine_ins_ls[i])
                    break

    # generate the linear system
    lin_sys, b = gen_lin_sys(model, op_list, global_var_syn, machine_sys, local_var_syn, machine_local)
   
    # solve the equation
    t1 = time.time()
    x = np.linalg.lstsq(lin_sys, b, rcond=None)[0]
    # x = np.linalg.solve(lin_sys, b)
    t2 = time.time()
    time_lin_sys = t2 - t1
    res_linear = (np.dot(lin_sys, x)-(b)).reshape(-1)

    # start mixed equation analysis
    x_global = x[:len(global_var_syn)]
    x_local = x[len(global_var_syn):]

    # calculate evolution time t using global var solutions
    global_connected = classifier(global_var_syn)
    global_mixed_time, t_global, res_g = eq_builder_with_global(global_connected, global_var_syn, global_var, x_global, global_sol)
    lin_sys_g = lin_sys[:, :len(global_var_syn)]
    lin_sys_l = lin_sys[:, -len(local_var_syn):]
    res_b_g = np.dot(lin_sys_g, res_g)
    t1 = time.time()
    update_l = np.linalg.lstsq(lin_sys_l, -res_b_g, rcond=None)[0]
    t2 = time.time()
    t_relax = t2-t1
    res_linear_new = np.dot(lin_sys_l, update_l)-(-res_b_g)
    update_l = [[x] for x in update_l]
   
    

    # local variable
    local_connected = classifier(local_var_syn)
    # build and solve the local mixed equation for each component
    local_mixed_time, local_var_sol_dict, res_l = eq_builder(local_connected, local_var_syn, local_var, (x_local+update_l)/t_global)
    res_l = res_l * t_global
    res_b_l = np.dot(lin_sys_l, res_l)

    sol = merge_dic(local_var_sol_dict, global_sol)

    # res = res_linear + (res_b_l+res_b_g)
    res = res_linear + (res_b_l+res_b_g) + (res_linear_new-res_b_g)
    res_l1 = np.linalg.norm(res, ord=1)

    # result analysis
    # Compilation time
    t_compile = time_lin_sys + global_mixed_time + local_mixed_time + t_relax
    # Evolution time
    t_evol = t_global[0]

    return t_compile, t_evol, sol, res_l1
