import sys
import re

from slither import Slither

# overwritting data-dependency file with my own modifications
from slither.analyses.data_dependency.data_dependency import (
#from data_dependency import (
    is_dependent,
    is_tainted,
    get_dependencies,
    get_all_dependencies,
    pprint_dependency,
    compute_dependency
)

from slither.core.variables.local_variable import LocalVariable
from slither.core.declarations.function import Function
from slither.core.declarations.solidity_variables import SolidityVariableComposed
from slither.core.solidity_types.elementary_type import ElementaryType


# store msg.sender, msg.value, and msg.owner
HIDDEN_PARAMETERS = set([])

if len(sys.argv) != 2 and len(sys.argv) != 3:
    print("Usage: python smart_contract_repair.py file.sol or python smart_contract_repair.py file.sol contract")
    sys.exit(-1)

slither = Slither(sys.argv[1])
compute_dependency(slither)

def not_intermediate(x):
    return "REF" not in x.name and "TMP" not in x.name


def point_to_analysis(contract, function, parameter):
    
    #D = get_all_dependencies(function, only_unprotected=True)
    #D = {key.name : [x.name for x in value if not_intermediate(x)] for key, value in D.items() if not_intermediate(key)}
    #print(D)

    G = set()
    for g in contract.state_variables:

        #print('Hig\t\t', g.name)
        #print('Hiparameter\t\t', parameter.name)
        
        # useful reference: https://github.com/crytic/slither/issues/156
        if is_dependent(g, parameter, contract):
            #print('HiHi\t\t', g.name)
            if function.is_reading(g) and (not function.is_writing(g)):
                G.add(g)
    
        for node in function.nodes:
            if node.expression:
                for hp in HIDDEN_PARAMETERS:
                    if hp == g:
                        continue
                    V = set(node.variables_read)
                    #W = set()
                    W = set(node.variables_read).union(set(node.variables_written))
                    if (hp in W or is_dependent_on(W,hp,function)) and (g in V or is_dependent_on(V,g,function)):
                        #print('HiHiHi\t\t', g.name)
                        if function.is_reading(g) and (not function.is_writing(g)):
                            G.add(g)

    return G

def is_dependent_on(variables, var, function) -> bool:

    for v in variables:
        if is_dependent(v,var,function):
            return True
    return False

def is_function_setting_variable(variables, f, var) -> bool:
    """
    Return 
    """
    for v in variables:
        if f.is_writing(v) and (v != var  and not isinstance(v.type, ElementaryType)):
            #print('HiVf\t\t', f.name)
            #print('HiV\t\t', isinstance(v.type, ElementaryType))
            #print('HiVar \t\t', var.name)
            return False
        if f.is_reading(v) and (v.type != ElementaryType("bool") and v.type != ElementaryType("address") and v != var):
            #print('HiHHiif\t\t', f.name)
            #print('HiHHiif\t\t', v.name)
            #print('HiHHiif\t\t', v.type)
            return False
        
    return True

def Are_functions_setting_variable(variable, variables, functions) -> bool:
    """
    Return 
    """
    for f in functions:
        if f.is_writing(variable) and not f.is_constructor:
            #print('HiHif\t\t', f.name)
            if is_function_setting_variable(variables,f,variable):
                #print('Hif\t\t', f.name)
                return True
    return False







def repair(contract):
    
    with open(sys.argv[1], 'r') as f:
        raw_code_lines = [line for line in f.readlines()]

    for function in contract.all_functions_called:
        #print('\t', function.name, function.visibility)

        # we only care about public functions
        # public vs external vs private vs internal: https://ethereum.stackexchange.com/questions/19380/external-vs-public-best-practices 
        # Payable vs View vs Pure: https://ethereum.stackexchange.com/questions/59326/what-is-the-difference-between-payable-and-view-in-a-smart-contract-in-solidity
        if function.visibility not in ["public", "external"]:
            continue

        # getting first line of function
        f_lines = function.source_mapping["lines"]
        f_index = f_lines[0]-1

        # getting first line of function body
        f_body = -1
        for i in function.source_mapping["lines"]:
            if "{" in raw_code_lines[i-1]:
                f_body = i-1
                break

        # getting indentation level
        indent = 0
        while raw_code_lines[f_body+1][indent] == ' ':
            indent += 1
        whitespace = ' ' * indent

        # This is probably redundant
        for node in function.nodes:
            if node.expression:
                #print(node.expression)
                #print(".transfer" in str(node.expression))
                for variable in node.solidity_variables_read:
                    if variable.name in ["msg.sender", "msg.value", "msg.owner"]:
                        HIDDEN_PARAMETERS.add(variable)

        all_G = set()
        #print('\t\t', HIDDEN_PARAMETERS.union(function.parameters))
        for parameter in HIDDEN_PARAMETERS.union(function.parameters):
            #print('\t\t', parameter.name)

            # point-to/alias analysis
            G = point_to_analysis(contract, function, parameter)

            for g in G:
                all_G.add(g)

        
        expected_parameters = []
        guard_statements = []
        for g in all_G:
            # only if they have a function setter
            #for vvv in contract.variables:
            #    print('\t\t', vvv.name)
            #print('\t\t', g.name)
            if Are_functions_setting_variable(g, contract.variables, contract.functions) and g.type != ElementaryType("address"):
            #if len( contract.get_functions_writing_to_variable(g) ) != 0:
                #print('He\t\t', g.name)
                #print('\t\t', contract.variables)
                expected_parameters.append( f"{g.type} {g.name}Expected" )
                guard_statements.append( f"{whitespace}require({g.name} == {g.name}Expected);" )
        
        # adding expected value parameters
        f_sig = raw_code_lines[f_index].split(")")
        f_sig[0] += ', ' if len(expected_parameters) != 0 and len(function.parameters) != 0 else ''
        f_sig[0] += ", ".join(expected_parameters)
        raw_code_lines[f_index] = ")".join(f_sig)

        # adding guard statements
        raw_code_lines[f_body] += '\n'.join(guard_statements) 
        raw_code_lines[f_body] += '\n' if len(guard_statements) != 0 else ''

    with open(sys.argv[1][:-4] + "_repaired.sol", 'w+') as g:
        g.writelines(raw_code_lines)



def main():


    with open(sys.argv[1], 'r') as f:
        raw_code_lines = [line for line in f.readlines()]
    for contract in slither.contracts:

        #print(contract.name)

        if len(sys.argv) == 2:
            repair(contract)
            break
        else: 
            if sys.argv[2] is None or sys.argv[2] == contract.name:
            #print(contract.__dir__())
                repair(contract)
                break


if __name__ == "__main__":
    main()