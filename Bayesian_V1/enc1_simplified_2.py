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

                # define parameter variables
                for j in range(0, bn.get_cardinality(i)):
                    #parameter_variable_n.append('theta_' + i + str(j))
                    #parameter_variable_v.append(False)
                    #parameter_to_value.append(("", -100))
                    st = (i, j, [])
                    #parameter_triple.append(st)

                    # define values in the variable dictionary
                    temp_name = 'theta_' + i + str(j)

                    # add to variable dictionary
                    if temp_name not in variable_dictionary:
                        variable_dictionary[temp_name] = max(variable_dictionary.values()) + 1
                        
                        # fetch weights from bn
                        infer = VariableElimination(bn)
                        temp_weight = infer.query([i], evidence={})[i]
                        parameter_weights[temp_name] = temp_weight

                    # add the weight to parameter weight

               # parameter_index.append(('theta' + i, bn.get_cardinality(i)))




            # case 2 with evidence
            else:
                print("need to generate lambdas")
                # define indicator variables of Node i

                temp_name = 'lambda_' + i + '0'

                if temp_name not in variable_dictionary:
                    variable_dictionary[temp_name] = max(variable_dictionary.values()) + 1

                temp_name = 'lambda_' + i + '1'

                if temp_name not in variable_dictionary:
                    variable_dictionary[temp_name] = -1 * max(variable_dictionary.values())

                evidence_list = bn.get_cpds(i).get_evidence()



        thiscpd = bn.get_cpds(i)
