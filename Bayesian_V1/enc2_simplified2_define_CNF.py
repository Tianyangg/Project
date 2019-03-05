from Bayesian_V1 import enc2_simplified2 as df_v
from Bayesian_V1 import parameter_generation
from pgmpy.inference import VariableElimination
from more_itertools import locate

# Encoding 1 clause simplified

debug = False

indicator_clauses = [] # stote the indicator name
indicator_clauses_s = [[]] # store the sign of the indicator clauses
indicator_single_clauses =[[]]
parameter_triple = df_v.parameter_triple

# update: generate indicator clauses
def enc2_indicator_clauses(bn):
    ctr = 0 # control index in indicator_variable_n
    index = 0 # NOTE: explain this!!!!
    for i in bn.nodes:    # [A, B, C]
        node_cardinality = bn.get_cardinality(i)
        # case1: without evidence

        # case2: with evidence
        #print(enc1_sim2.parameter_triple)

        # get evidence cardinality
        if node_cardinality != 0:
            in_clause = []
            in_clause.clear()
            for j in range(0, node_cardinality):
                temp_name = 'lambda_' + i + str(j)
                in_clause.append((1,df_v.variable_dictionary[temp_name]))

            indicator_clauses.append(in_clause)

            #-lambda_xi v -lambda_xj when i < j
            for m in range(0, node_cardinality):
                for n in range(m + 1, node_cardinality):
                    indicator_clauses.append([(-1, df_v.variable_dictionary['lambda_' + i + str(m)]), (-1, df_v.variable_dictionary['lambda_' + i + str(n)])])


parameter_clauses = []
# generate parameter clasues
def enc2_parameter_clauses(bn):
    # Note: first make sure the weight is not 0 or 1 then consider encoding clauses

    for i in bn.nodes:    # [A, B, C]
        # get the cardinality of a node:
        node_cardinality = bn.get_cardinality(i)
        for j in range(0, node_cardinality):
            # return the index with e,g('tub', 0, _) => result: [0, 1]
            triple_index = (locate(parameter_triple, lambda x1: (x1[0] == i and x1[1] == j)))
            triple_list = [parameter_triple[i] for i in triple_index]
            #print('tr', triple_list)
            if not triple_list:     # Case1: without evidence
                temp_name = 'theta_' + i + str(j)
                if df_v.parameter_weights[temp_name] != 0 and df_v.parameter_weights[temp_name] != 1:
                    # normal encoding without simplification:
                    # IP clauses
                    cnf_clause = [
                        (-1, df_v.variable_dictionary['lambda_' + i + str(j)]),
                        (1, df_v.variable_dictionary[temp_name])
                    ]  # this stores one clause: [(-1, 1), (1, 2)] means -x1 v x

                    parameter_clauses.append(cnf_clause)

                #simplification
                if df_v.parameter_weights[temp_name] == 0:
                    #print('0')
                    # negation of all:
                    cnf_clause = [(-1, df_v.variable_dictionary['lambda_' + i + str(j)])]
                    parameter_clauses.append(cnf_clause)







            else:  # Case2: with evidence
                for x in triple_list:
                    parameter_name = parameter_generation.namer(x[2])
                    temp_name = 'theta_' + i + str(j) + '|' + str(parameter_name)

                    # parameter weight none 0 and none 1:
                    if df_v.parameter_weights[temp_name] != 0 and df_v.parameter_weights[temp_name] != 1:
                        # normal encoding without simplification:
                        # IP clauses
                        pi_temp = []
                        pi_temp.clear()

                        cnf_clause = [(-1, df_v.variable_dictionary[
                            'lambda_' + i + str(j)])]  # this stores one clause: [(-1, 1), (1, 2)] means -x1 v x2
                        pi_temp.append(df_v.variable_dictionary[
                            'lambda_' + i + str(j)])
                        cnf_clause_add = [(-1, df_v.variable_dictionary['lambda_'+ n[0] + str(n[1])]) for n in x[2]]
                        pi_temp = pi_temp + [df_v.variable_dictionary['lambda_'+ n[0] + str(n[1])] for n in x[2]]
                        cnf_clause = cnf_clause + cnf_clause_add
                        cnf_clause.append((1, df_v.variable_dictionary[temp_name]))

                        parameter_clauses.append(cnf_clause)

                    if df_v.parameter_weights[temp_name] == 0:
                        #print('0')
                        # negation of all:
                        cnf_clause = [(-1, df_v.variable_dictionary[
                            'lambda_' + i + str(j)])]  # this stores one clause: [(-1, 1), (1, 2)] means -x1 v x2
                        pi_temp.append(df_v.variable_dictionary[
                                           'lambda_' + i + str(j)])
                        cnf_clause_add = [(-1, df_v.variable_dictionary['lambda_' + n[0] + str(n[1])]) for n in x[2]]
                        cnf_clause = cnf_clause + cnf_clause_add
                        parameter_clauses.append(cnf_clause)



        # Cardinality == 2 and no evidence: skip this


        # Cardinality == 2 and with evidence: skip the indicator clauses, generate parameter clauses


def pretty_print_iclause():
    printing = []
    for i in indicator_clauses:
        for j in indicator_clauses_s:
            printing.append(list(zip(j, i)))
    #print(printing)


write_file = []
def write_clauses():
    #indicator clauses
    for i in indicator_clauses:
        if i:
            list1 = [j[1]*j[0] for j in i]
            write_file.append(list1)
    for i in parameter_clauses:
        if i:
            list1 = [j[1] * j[0] for j in i]
            write_file.append(list1)



