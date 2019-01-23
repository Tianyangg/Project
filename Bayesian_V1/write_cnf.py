#generate a CNF File
from Bayesian_V1 import define_CNF as df_c
from Bayesian_V1 import define_variables as df_v

# !! need to get the file name!!!

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