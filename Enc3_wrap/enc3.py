from Bayesian_V1 import parameter_generation
from pgmpy.inference import VariableElimination
from Bayesian_V1 import enc3_partitioncpt as par
from Bayesian_V1 import fetch_result as fetch

indicator_index = []

# variable dictionary for cnf files
variable_dictionary = {
    'header': 0
}

parameter_weights = {
    'parameter_header': 0
}

parameter_triple = []
# this gives  the combinations of letters and numbers
def mixture(list):
    result = []
    result.clear()
    result = parameter_generation.zipper(list)
    return result

#Generate evidences table[A, B] with [2,2]
#Output [[A0,A1][B0,B1]]
def generate_evrow(evidence, evidence_card):
    list = []
    list.clear()
    ctr = 0
    for ev in evidence:
        list1 = []
        index = 0
        for i in range (0, evidence_card[ctr]):
            list1.append((ev, index))
            #list1.append(str(ev)+str(index))
            index += 1
        list.append(list1)
        ctr += 1
    return list

# these gives the same encoding for indicator variables:
def enc3_indicator_encoding(bn):
    clauses = []
    for i in bn.nodes:
        #print('node: '+i)
        card = bn.get_cardinality(i)
        indicator_index.append((i, card))  # index_variable[i] stores the cardinality of the i_^th node: e.g [('A', 2), ('B', 3)...]
        thiscpd = bn.get_cpds(i)
        #print(thiscpd)
        # define indicator variable

        for j in range(0, card):  # example: get node A's cardinality = 3
            # define indicator variables:
            temp_name = 'lambda_' + i + str(j)

            if temp_name not in variable_dictionary:
                variable_dictionary[temp_name] = max(variable_dictionary.values()) + 1

    for i in bn.nodes:  # [A, B, C]
        # get the cardinality of a node:
        node_cardinality = bn.get_cardinality(i)
        # case1: without evidence

        # case2: with evidence
        # print(enc1_sim2.parameter_triple)

        # get evidence cardinality
        if node_cardinality != 0:
            in_clause = []
            in_clause.clear()
            for j in range(0, node_cardinality):
                temp_name = 'lambda_' + i + str(j)
                in_clause.append((1, variable_dictionary[temp_name]))

            clauses.append(in_clause)

            # -lambda_xi v -lambda_xj when i < j
            for m in range(0, node_cardinality):
                for n in range(m + 1, node_cardinality):
                    clauses.append([(-1, variable_dictionary['lambda_' + i + str(m)]),
                                    (-1, variable_dictionary['lambda_' + i + str(n)])])
    return clauses

# define the method for prime encoding
# parameter: bayesian network
# get the node and it's CPT's value then store the parameter value into following form:
# [('C', 1, [('B', 1), ('A', 2)], 0.04),
#         ('C', 2, [('B', 1), ('A', 2)], 0.4),
# call the partition and do the encode
def prime_encode(l):
    ctr = 0
    clauses = []
    while ctr < len(l):
        prime_group = [x for x in l if x[3] == l[ctr][3]]
        ctr = ctr + len(prime_group)

        ## get the value
        if prime_group != []:
            par_value = prime_group[0][3]
            if par_value == 0:
                # set it to false
                # do not generate parameter variable
                terms = []
                for i in prime_group:
                    term = []
                    if i[1] != -1:
                        indicator_name = 'lambda_'+i[0]+str(i[1])

                        if indicator_name in variable_dictionary:
                            term.append((-1, variable_dictionary[indicator_name]))
                        else:
                            # append
                            indicator_value = max(variable_dictionary.values()) + 1
                            term.append((-1, indicator_value))
                            # add to dictionary
                            variable_dictionary[indicator_name] = indicator_value

                    for j in i[2]:
                        if j[1] != -1:
                            indicator_name = 'lambda_' + j[0] + str(j[1])
                            if indicator_name in variable_dictionary:
                                term.append((-1, variable_dictionary[indicator_name]))
                            else:
                                # append
                                indicator_value = max(variable_dictionary.values()) + 1
                                term.append((-1, indicator_value))
                                # add to dictionary
                                variable_dictionary[indicator_name] = indicator_value

                    terms.append(term)
                    clauses = clauses + terms
            else:
                if par_value != 1:
                # encode the clause and the parameter variable
                    terms = []
                    for i in prime_group:
                        # ADD HERE the if next line
                        term = []
                        if i[1] != -1:
                            indicator_name = 'lambda_' + i[0] + str(i[1])
                            #term = []
                            if indicator_name in variable_dictionary:
                                term.append((-1, variable_dictionary[indicator_name]))
                            else:
                                # append
                                indicator_value = max(variable_dictionary.values()) + 1
                                term.append((-1, indicator_value))
                                # add to dictionary
                                variable_dictionary[indicator_name] = indicator_value
                        for j in i[2]:
                            # ADD HERE THE IF NEXT LINE
                            if j[1] != -1:
                                indicator_name = 'lambda_' + j[0] + str(j[1])
                                if indicator_name in variable_dictionary:
                                    term.append((-1, variable_dictionary[indicator_name]))
                                else:
                                    # append
                                    indicator_value = max(variable_dictionary.values()) + 1
                                    term.append((-1, indicator_value))
                                    # add to dictionary
                                    variable_dictionary[indicator_name] = indicator_value

                        terms.append(term)

                    # generate a parameter value
                    parameter_name = 'theta_'+str(len(parameter_weights))
                    # add to weight dict
                    if parameter_name not in parameter_weights:
                        parameter_weights[parameter_name] = par_value
                    # add to variable or fetch it
                    if parameter_name in variable_dictionary:
                        t = (1, variable_dictionary[parameter_name])
                    else:
                        # append
                        parameter_value = max(variable_dictionary.values()) + 1
                        t = (1, parameter_value)
                        # add to dictionary
                        variable_dictionary[parameter_name] = parameter_value

                    # append the parameter at the end of each term
                    for cl in terms:
                        cl.append(t)
                        clauses.append(cl)

        else:
            print('error when encoding prime')

    return clauses


def generate_original_cpts(bn):
    clauses = []
    for i in bn.nodes:
        card = bn.get_cardinality(i)
        indicator_index.append((i, card))  # index_variable[i] stores the cardinality of the i_^th node: e.g [('A', 2), ('B', 3)...]
        #thiscpd = bn.get_cpds(i)

        # define indicator variables

        # the cpt before partition
        old_cpt = fetch.mytable(bn.get_cpds(i))

        ## now we have the old_cpt of node i
        #print('old', old_cpt)
        #HERE
        prime_list = par.old2prime(old_cpt)

        clauses = clauses + prime_encode(prime_list)

        '''
        old_cpt = []
        if bn.get_cpds(i).get_evidence():
            # generate evidence:
            ev_cardinality = []
            ev_cardinality.clear()
            # get cardinality
            for m in thiscpd.get_evidence():  # [A,B]
                ev_cardinality.append(bn.get_cardinality(m))

            for m in range(0, bn.get_cardinality(i)):  # i_m
                tablerows = mixture(generate_evrow(thiscpd.get_evidence(), ev_cardinality))
                for j in tablerows:
                    # j is a list of tuples
                    # define the name of tuples  # define values in the variable dictionary
                    infer = VariableElimination(bn)
                    query_weight = infer.query([i], evidence=evidence_dic(j))[i]
                    temp_weight = query_weight.values[m]

                    old_cpt.append((i, m, j, temp_weight))
        else:
            for m in range(0, bn.get_cardinality(i)):  # i_m
                infer = VariableElimination(bn)
                query_weight = infer.query([i], evidence={})[i]
                temp_weight = query_weight.values[m]
                old_cpt.append((i, m, [], temp_weight))
                
        '''
    return clauses



def write_clauses(bn):
    write_file = []
    clauses = enc3_indicator_encoding(bn)
    clauses = clauses + generate_original_cpts(bn)
    print("write cnf:")
    #indicator clauses
    for i in clauses:
        if i:
            list1 = [j[1]*j[0] for j in i]
            write_file.append(list1)
    return write_file


def evidence_dic(tuples):
    ev_dic = {}
    for i in tuples:
        ev_dic[i[0]] = i[1]
    return ev_dic

def parameter_vars_withevidence():

    print("test")