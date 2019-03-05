from Bayesian_V1 import parameter_generation

indicator_variable_n = [] # the list for Variable parameter names
indicator_variable_v = [] # the cor values with same index as name
indicator_index = [('null', -100)]
indicator_tuple = set()

parameter_variable_n = []
parameter_variable_v = []
parameter_to_value = [] # this store the corresponisng
parameter_weights = [] # this stores the weights
parameter_index = [('null', -100)]
parameter_triple = []

# variable dictionary for cnf files
variable_dictionary = {
    'header': 0
}


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

def generate_variable(bn):
    for i in bn.nodes:
        card = bn.get_cardinality(i)
        indicator_index.append((i, card))  # index_variable[i] stores the cardinality of the i_^th node
        # define indicator variables
        thiscpd = bn.get_cpds(i)

        # if the cardinality = 2 (either true or false)
        if card == 2:
            indicator_variable_n.append('lambda_' + i + '0')
            #indicator_variable_n.append('lambda_' + i + '0')
            indicator_tuple.add((i, 0))
            indicator_variable_v.append(False)

            # define values in the variable dictionary
            temp_name = 'lambda_' + i + '0'

            if temp_name not in variable_dictionary:

                variable_dictionary[temp_name] = max(variable_dictionary.values()) + 1

            indicator_variable_n.append('lambda_' + i + '1')
            indicator_tuple.add((i, 1))
            indicator_variable_v.append(False)

            temp_name = 'lambda_' + i + '1'

            if temp_name not in variable_dictionary:
                variable_dictionary[temp_name] = -1 * max(variable_dictionary.values())

            thiscpd = bn.get_cpds(i)

        else:

            for j in range(0, card):  # example: get node A's cardinality = 3
                indicator_variable_n.append('lambda_' + i + str(j))
                indicator_tuple.add((i, j))
                indicator_variable_v.append(False)

                # define values in the variable dictionary
                temp_name = 'lambda_' + i + str(j)

                if temp_name not in variable_dictionary:
                    variable_dictionary[temp_name] = max(variable_dictionary.values()) + 1

            thiscpd = bn.get_cpds(i)


        # define parameter Variables

        # case1: no evidence
        if thiscpd.get_evidence() == []:  # if this var has no evidence, only do theta_xi
            # print (thiscpd)
            for j in range(0, bn.get_cardinality(i)):
                parameter_variable_n.append('theta_' + i + str(j))
                parameter_variable_v.append(False)
                parameter_to_value.append(("", -100))
                st = (i, j, [])
                parameter_triple.append(st)

                # define values in the variable dictionary
                temp_name = 'theta_' + i + str(j)

                if temp_name not in variable_dictionary:
                    variable_dictionary[temp_name] = max(variable_dictionary.values()) + 1

            parameter_index.append(('theta' + i, bn.get_cardinality(i)))
        else:
        # case2: have evidence
            # !!!!! need to know how to fetch evidence_cardinality properly
            ev_cardinality = []
            ev_cardinality.clear()
            # get cardinality
            for m in thiscpd.get_evidence():  # [A,B]
                ev_cardinality.append(bn.get_cardinality(m))

            for m in range(0, bn.get_cardinality(i)):  # i_m
                # this gives all the rows of the cpds
                tablerows = mixture(generate_evrow(thiscpd.get_evidence(), ev_cardinality))
                ctr = 0
                for j in tablerows:
                    # j is a tuple (string, integer)
                    namer = []
                    namer.clear()
                    namer = ''.join(parameter_generation.list_tuple_to_str(j))  # change the type
                    parameter_variable_n.append(
                        'theta_' + i + str(m) + '|' + namer)  # append theta_i_m|namer e.g: theta_C0|B0A0
                    parameter_to_value.append(j)
                    parameter_variable_v.append(False)
                    st = (i, m, j)
                    parameter_triple.append(st)

                    # define values in the variable dictionary
                    temp_name = 'theta_' + i + str(m) + '|' + namer

                    if temp_name not in variable_dictionary:
                        variable_dictionary[temp_name] = max(variable_dictionary.values()) + 1

