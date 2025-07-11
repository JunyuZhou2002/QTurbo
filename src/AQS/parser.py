import re
import copy


# Hamiltonian parsing
# Hamiltonain form: {} * Z1Z2 + {} * X1 + ...
def parse_ham(ham):
    # Regex to match "(any string) * something"
    matches = re.findall(r'\{(.*?)\} \* (.+?)(?: \+|$)', ham)

    coefs = [match[0] for match in matches]
    pauli = [match[1] for match in matches]
    
    return coefs, pauli


# Coefficient parsing
# Coefficient form: 1 * [SynVar1] - 2 * [SynVar2] + 3 * [SynVar3] 
# Return: list [SynVar1, SynVar2, SynVar3] of synthesized variables(also called terms) 
def parse_coef(expression):
    
    matches = re.findall(r'([+-]?\s*\d+)\s*\*\s*\[(.+?)\]', expression)

    coef_sign = [float(match[0].replace(" ", "")) for match in matches]
    terms = [match[1] for match in matches]
    
    return coef_sign, terms 


# Check dependency between coefficients with synthesized variables
def HamTerm_SynVar(coef, pauli):
    
    # Dictionary to store pauli operaters with their dependency on the terms
    op_dic = {}
    # Empty list and dictionary to store the synthesized variables
    term_list = []
    term_dic = {}
    
    for i, pauli_ in enumerate(pauli):

        coef_ = coef[i]
        coef_sign, terms = parse_coef(coef_)

        if pauli_ not in op_dic:
            op_dic[pauli_] = []
        # else:
        #     print(f"'{pauli_}' already exists, double check the Hamiltonian.")

        for j, term_ in enumerate(terms):
            if term_ not in term_dic:
                term_dic[term_] = len(term_list)
                term_list.append([term_])
                op_dic[pauli_].append([term_dic[term_], coef_sign[j]])
            else:
                op_dic[pauli_].append([term_dic[term_], coef_sign[j]])

    return op_dic, term_list, term_dic 


# variable parsing
# Form: "@x1@ + 1/@b@"
# Return [x1, b]
def parse_var(term):
    vars = re.findall(r'@(\w+)@', term)
    return vars

# Check dependency between synthesized variables and original variables
def SynVar_OriVar(term_list):

    # Empty list and dictionary to store the variables
    var_dic = {}
    var_list = []
    term_list_copy = copy.deepcopy(term_list)
    
    for i, term_ in enumerate(term_list_copy):

        term_list_copy[i].append([])
        term_ = term_[0]

        vars = parse_var(term_)
        term_list_copy[i][0] = re.sub(r'@', '',term_list_copy[i][0])

        for var_ in vars:
            if var_ not in var_dic:
                var_dic[var_] = len(var_list)
                var_list.append(var_)
                term_list_copy[i][1].append(var_dic[var_])
            else: 
                term_list_copy[i][1].append(var_dic[var_])  

    return term_list_copy, var_dic, var_list

# Parsing function
def parsing(ham):

    coefs, pauli = parse_ham(ham)
    op_dic, term_list, _ = HamTerm_SynVar(coefs, pauli)
    term_list_copy, _, var_list = SynVar_OriVar(term_list)
    
    return op_dic, term_list_copy, var_list
