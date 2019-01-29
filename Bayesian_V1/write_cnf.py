#generate a CNF File
from Bayesian_V1 import define_CNF as df_c
from Bayesian_V1 import define_variables as df_v
from Bayesian_V1 import enc1_simplified_def_variables as df_v_simplified

# !! need to get the file name!!!
# take a list of lists, each element is a CNF
# generate a .cnf FILE
def write_no_weight(ll):
    f = open("temp.cnf", "w")
    print(len(ll))
    f.write("c This is the test file generate by sty"+"\n")
    f.write("p cnf "+ str(len(df_v.variable_dictionary) - 1) +" " + str(len(ll)) +"\n")
    for i in ll:
        # list1 = [1, 2, 3]
        str1 = ''.join(str(e)+' ' for e in i)
        str1 = str1.join(" 0")
        f.write(str1+"\n")
    f.close()

#write_no_weight(df_c.write_file)


def enc1_write_no_weight_simplified(ll):
    f = open("temp.cnf", "w")
    print(len(ll))
    f.write("c This is the enc1_simplified file generate by sty"+"\n")
    f.write("p cnf "+ str(max(df_v_simplified.variable_dictionary.values())) +" " + str(len(ll)) +"\n")
    for i in ll:
        # list1 = [1, 2, 3]
        str1 = ''.join(str(e)+' ' for e in i)
        str1 = str1.join(" 0")
        f.write(str1+"\n")
    f.close()