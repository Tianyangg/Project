from Bayesian_V1 import parameter_generation
from Bayesian_V1 import fetch_result as fetch
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
    print('define generate_var')
    for i in bn.nodes:
        print('node'+i)
        card = bn.get_cardinality(i)
        indicator_index.append((i, card))  # index_variable[i] stores the cardinality of the i_^th node: e.g [('A', 2), ('B', 3)...]
        thiscpd = bn.get_cpds(i)
        print(thiscpd)

        #get rid of the query#
        mycpt = fetch.mytable(bn.get_cpds(i))
        print(mycpt)

        # define indicator variables

        if card == 0:
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
                    infer = VariableElimination(bn)
                    query_weight = infer.query([i], evidence={})[i]
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
                    print(thiscpd.get_evidence)
                    print(ev_cardinality)
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
                        if temp_weight == 1 or temp_weight == 0:
                            parameter_weights[temp_name] = temp_weight
                            # only add to parameter weight for future reference
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
            # case1 without evidence
            if not bn.get_cpds(i).get_evidence():

                for m in range(0, bn.get_cardinality(i)):  # i_m
                    temp_name = 'theta_' + i + str(m)
                    print(str(i) + "no evidence")

                    #infer = VariableElimination(bn)

                    #query_weight = infer.query([i], evidence={})[i]
                    #temp_weight = query_weight.values[m]

                    # the new version
                    temp_weight = mycpt[m][3]

                    # omit the clause if theta .. = 1
                    if temp_weight == 1 or temp_weight == 0:
                        parameter_weights[temp_name] = temp_weight
                        # only add to parameter weight for future reference
                    if temp_weight != 1 and temp_weight != 0:
                        if temp_name not in variable_dictionary:
                            variable_dictionary[temp_name] = max(variable_dictionary.values()) + 1
                        parameter_weights[temp_name] = temp_weight

            # case2 with evidence
            else:
            # define parameter variables:
                ev_cardinality = []
                ev_cardinality.clear()
                # get cardinality
                for m in thiscpd.get_evidence():  # [A,B]
                    ev_cardinality.append(bn.get_cardinality(m))
                for x in mycpt:
                    temp_name = 'theta_' + x[0] + str(x[1]) + '|' + tuples2str(x[2])  # append theta_i_m|namer e.g: theta_C0|B0A0
                    print('tempname', temp_name)
                    temp_weight = x[3]

                    st = (x[0], x[1], x[2])
                    parameter_triple.append(st)

                    # omit the clause if theta .. = 1
                    if temp_weight == 1 or temp_weight == 0:
                        parameter_weights[temp_name] = temp_weight
                        # only add to parameter weight for future reference
                    if temp_weight != 1 and temp_weight != 0:
                        if temp_name not in variable_dictionary:
                            variable_dictionary[temp_name] = max(variable_dictionary.values()) + 1
                        parameter_weights[temp_name] = temp_weight
'''
                for m in range(0, bn.get_cardinality(i)):  # i_m
                    # returns evidence tuples [[(A,0), (B,0)] [(A,0), (B1)]...]
                    print(thiscpd.get_evidence)
                    print(ev_cardinality)
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
                        query_weight = infer.query([i], evidence=evidence_dic(j))[i]
                        temp_weight = query_weight.values[m]


                        # omit the clause if theta .. = 1
                        if temp_weight == 1 or temp_weight == 0:
                            parameter_weights[temp_name] = temp_weight
                            # only add to parameter weight for future reference
                        if temp_weight != 1 and temp_weight != 0:
                            if temp_name not in variable_dictionary:
                                variable_dictionary[temp_name] = max(variable_dictionary.values()) + 1
                            parameter_weights[temp_name] = temp_weight
'''


def tuples2str(l):
    s = ''
    for i in l:
        s = s+str(i[0])+str(i[1])
    return s

def evidence_dic(tuples):
    ev_dic = {}
    for i in tuples:
        ev_dic[i[0]] = i[1]
    return ev_dic

list2 = [('A', 1), ('B', 3), ('C', 0)]
print(tuples2str(list2))
