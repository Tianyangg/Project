from Bayesian_V1 import define_variables as df_v, parameter_generation

# Encoding 1 indicator clauses
#

debug = False

indicator_clauses = [[]] # stote the indicator name
indicator_clauses_s = [[]] # store the sign of the indicator clauses
indicator_single_clauses =[[]]
def enc1_indicator_clauses(bn):

    ctr = 0 # control index in indicator_variable_n
    index = 0 # NOTE: explain this!!!!
    for i in bn.nodes:    # [A, B, C]
        result = [x[1] for x  in df_v.indicator_index if x[0] == i ]
        # step 1, the positive clauses
        for j in range(0, result[0]):
            indicator_clauses[index].append((1, df_v.indicator_variable_n[ctr])) # list of tuples(sign, name)
            #indicator_single_clauses[index].append(df_v.indicator_variable_n[ctr]) # list of names(name)
            indicator_clauses_s[index].append(1)
            ctr += 1

        index += 1
        indicator_clauses.append([])
        indicator_clauses_s.append([])

        # step 2: the i < j
        indicator_single_name = list(zip(*indicator_clauses[index - 1]))
        #print(indicator_single_name)
        #processing_clause = indicator_clauses[index - 1]
        processing_clause = indicator_single_name[1]
        #print("Processing")
        #print(processing_clause)
        # print(processing_clause, len(processing_clause))
        for u in range(0, len(processing_clause) - 1):
            ctr_2 = u + 1
            for v in range(ctr_2, len(processing_clause)):
                indicator_clauses[index].append((-1,processing_clause[u]))
                indicator_clauses_s[index].append(-1)
                indicator_clauses[index].append((-1,processing_clause[v]))
                indicator_clauses_s[index].append(-1)

                index += 1
                indicator_clauses.append([])
                indicator_clauses_s.append([])


    print(indicator_clauses)
    #print(indicator_clauses_s)
    #pretty_print_iclause()

def pretty_print_iclause():
    printing = []
    for i in indicator_clauses:
        for j in indicator_clauses_s:
            printing.append(list(zip(j, i)))
    print(printing)


parameter_clause = [] # store the generated clauses
parameter_CNF = []

def enc1_parameter_clauses():
    # example:
    # a1 /\ c1 <=> theta_c1|a1
    # (-1, a1),(-1, c1), lambda c1|a1


    for i in df_v.parameter_triple:
        #look up indicator variables
        temp = []
        temp.clear()
        for j in i[2]:
            #print(j)
            if j in df_v.indicator_tuple:
                temp.append("lambda_"+parameter_generation.tuple_to_string(j))


        # case1 without evidence:
        if not temp:
            temp.append("lambda_"+str(i[0])+str(i[1]))
            parameter_clause.append(["theta_"+str(i[0])+str(i[1]), temp])

            # =>
            clause1 = [(-1, i) for i in temp]
            clause1.append((1, "theta_"+str(i[0])+str(i[1])))
            parameter_CNF.append(clause1)
            # <=
            for k in temp:
                clause2 = [(-1, "theta_"+str(i[0])+str(i[1])), (1, k)]
                parameter_CNF.append(clause2)

        # case2 with evidence:
        else:
            namer = []
            namer.clear()
            namer = ''.join(parameter_generation.list_tuple_to_str(i[2]))
            temp.append("lambda_"+str(i[0])+str(i[1]))
            parameter_clause.append(["theta_"+str(i[0])+str(i[1])+"|"+namer, temp])

            # =>
            clause1 = [(-1, i) for i in temp]
            clause1.append((1, "theta_"+str(i[0])+str(i[1])+"|"+namer))
            parameter_CNF.append(clause1)

            # <=
            for k in temp:
                clause2 = [(-1, "theta_"+str(i[0])+str(i[1])+"|"+namer), (1, k)]
                parameter_CNF.append(clause2)


    if debug:
        print("parameter_clause")
        print(parameter_clause)
        print("parameter_CNF")
        print(parameter_CNF)

def enc1_clauses_weight(bn):
    # return the weight of certain clauses
    #
    #
    #
    # use the parameter_clause
    count = 0
    for i in df_v.parameter_triple:
        table = i[0]
        # case with evidence
        if len(i[2]) != 0:
            evidence = i[2]
            ## attention: !!!!! 这个evidence的顺序是有问题的！！！！！
            unzip = list(zip(*evidence))
            #temp = [list(t) for t in zip(*evidence)]
            temp = list(unzip[1])
            temp.insert(0, i[1])
            temp = tuple(temp)
            print("Weight"+str(parameter_clause[count]))
            print(bn.get_cpds(table).values[temp])
            count += 1
        else:
            print("Weight" + str(parameter_clause[count]))
            print(bn.get_cpds(table).values[i[1]])
            count += 1

        print("---分割线-----")

write_file = []
def write_indicator_clause():
    print("write cnf:")

    #indicator clauses
    for i in indicator_clauses:
        if i:
            list1 = [df_v.variable_dictionary[j[1]]*j[0] for j in i]
            write_file.append(list1)
    for i in parameter_CNF:
        if i:
            list1 = [df_v.variable_dictionary[j[1]] * j[0] for j in i]
            write_file.append(list1)

    print(write_file)



enc1_parameter_clauses()


