from Bayesian_V1 import parameter_generation
from pgmpy.inference import VariableElimination

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



def generate_vars(bn):
    for i in bn.nodes:
        card = bn.get_cardinality(i)
        indicator_index.append((i, card))  # index_variable[i] stores the cardinality of the i_^th node: e.g [('A', 2), ('B', 3)...]
        thiscpd = bn.get_cpds(i)
        # define indicator variables

        if card == 2:
            # case 1 without evidence:
            if not bn.get_cpds(i).get_evidence(): # list is empty
                # define indicator variables
                temp_name = 'lambda_' + i + '0'
                if temp_name not in variable_dictionary:
                    variable_dictionary[temp_name] = max(variable_dictionary.values()) + 1

                temp_name = 'lambda_' + i + '1'
                if temp_name not in variable_dictionary:
                    variable_dictionary[temp_name] = -1 * max(variable_dictionary.values())

                # define parameter variables:
                temp_name = 'theta_' + i + '0'
                if temp_name not in variable_dictionary:
                    variable_dictionary[temp_name] = max(variable_dictionary.values()) + 1
                if temp_name not in parameter_weights:
                    # fetch weights from bn
                    infer = VariableElimination(bn)
                    query_weight = infer.query([i], evidence={})[i]
                    temp_weight = query_weight.values[0]
                    parameter_weights[temp_name] = temp_weight

                temp_name = 'theta_' + i + '1'
                if temp_name not in variable_dictionary:
                    variable_dictionary[temp_name] = max(variable_dictionary.values()) + 1

                if temp_name not in parameter_weights:
                    temp_weight = query_weight.values[1]
                    parameter_weights[temp_name] = temp_weight



            # case 2 with evidence
            else:
                # define indicator variables of Node i

                temp_name = 'lambda_' + i + '0'

                if temp_name not in variable_dictionary:
                    variable_dictionary[temp_name] = max(variable_dictionary.values()) + 1

                temp_name = 'lambda_' + i + '1'

                if temp_name not in variable_dictionary:
                    variable_dictionary[temp_name] = -1 * max(variable_dictionary.values())

               # define parameter variables
                ev_cardinality = []
                ev_cardinality.clear()
                # get cardinality
                for m in thiscpd.get_evidence():  # [A,B]
                    ev_cardinality.append(bn.get_cardinality(m))

                for m in range(0, bn.get_cardinality(i)):  # i_m
                    # returns evidence tuples [[(A,0), (B,0)] [(A,0), (B1)]...]
                    tablerows = mixture(generate_evrow(thiscpd.get_evidence(), ev_cardinality))
                    ctr = 0
                    for j in tablerows:
                        # j is a list of tuples
                        # define the name of tuples  # define values in the variable dictionary
                        temp_name = 'theta_' + i + str(m) + '|' + parameter_generation.namer(j)  # append theta_i_m|namer e.g: theta_C0|B0A0
                        st = (i, m, j)
                        parameter_triple.append(st)
                        # fetch result from CPT
                        # fetch weights from bn
                        infer = VariableElimination(bn)
                        print(str(i) + "with evidence" + str(evidence_dic(j)))
                        query_weight = infer.query([i], evidence = evidence_dic(j))[i]
                        temp_weight = query_weight.values[m]

                        # OMIT the theta if it == 1
                        if temp_weight != 1 and temp_weight != 0:
                            if temp_name not in variable_dictionary:
                                variable_dictionary[temp_name] = max(variable_dictionary.values()) + 1
                            parameter_weights[temp_name] = temp_weight

        else:
            for j in range(0, card):  # example: get node A's cardinality = 3
                # define indicator variables:
                temp_name = 'lambda_' + i + str(j)

                if temp_name not in variable_dictionary:
                    variable_dictionary[temp_name] = max(variable_dictionary.values()) + 1

            # define parameter variables:
            ev_cardinality = []
            ev_cardinality.clear()
            # get cardinality
            for m in thiscpd.get_evidence():  # [A,B]
                ev_cardinality.append(bn.get_cardinality(m))

            for m in range(0, bn.get_cardinality(i)):  # i_m
                # returns evidence tuples [[(A,0), (B,0)] [(A,0), (B1)]...]
                tablerows = mixture(generate_evrow(thiscpd.get_evidence(), ev_cardinality))
                ctr = 0
                for j in tablerows:
                    # j is a list of tuples
                    # define the name of tuples  # define values in the variable dictionary
                    temp_name = 'theta_' + i + str(m) + '|' + parameter_generation.namer(
                        j)  # append theta_i_m|namer e.g: theta_C0|B0A0
                    st = (i, m, j)
                    parameter_triple.append(st)

                    # fetch result from CPT
                    # fetch weights from bn

                    infer = VariableElimination(bn)
                    print(str(i) + "with evidence" + str(evidence_dic(j)))
                    query_weight = infer.query([i], evidence=evidence_dic(j))[i]
                    temp_weight = query_weight.values[m]

                    # omit the clause if theta .. = 1
                    if temp_weight != 1 and temp_weight != 0:
                        if temp_name not in variable_dictionary:
                            variable_dictionary[temp_name] = max(variable_dictionary.values()) + 1
                        parameter_weights[temp_name] = temp_weight


def evidence_dic(tuples):
    ev_dic = {}
    for i in tuples:
        ev_dic[i[0]] = i[1]
    return ev_dic

def parameter_vars_withevidence():

    print("test")