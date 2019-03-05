#generate a CNF File
from Bayesian_V1 import define_CNF as df_c
from Bayesian_V1 import define_variables as df_v
from Bayesian_V1 import enc1_simplified_def_variables as df_v_simplified
from Bayesian_V1 import enc1_simplified_2 as enc1_sim2


# !! need to get the file name!!!
# take a list of lists, each element is a CNF
# generate a .cnf FILE
def write_no_weight(ll):
    f = open("temp.cnf", "w")
    #print(len(ll))
    f.write("c This is the baseline encode file generate by sty"+"\n")
    f.write("p cnf "+ str(len(df_v.variable_dictionary) - 1) +" " + str(len(ll)) +"\n")
    for i in ll:
        # list1 = [1, 2, 3]
        str1 = ''.join(str(e)+' ' for e in i)
        str1 = str1.join(" 0")
        f.write(str1+"\n")
    f.close()

#write_no_weight(df_c.write_file)

def baseline_write_no_weight_simplified(ll, var_dic, name):
    print('writing baseline to file')
    fname = '/Users/tianyangsun/Documents/Project/Github_repo/baseline_results'+name+'_baseline.cnf'
    f = open(fname, "w")
    #print(len(ll))
    f.write("c This is the baseline generate by sty"+"\n")
    f.write("p cnf "+ str(max(var_dic.values())) +" " + str(len(ll)) +"\n")
    for i in ll:
        # list1 = [1, 2, 3]
        str1 = ''.join(str(e)+' ' for e in i)
        str1 = str1.join(" 0")
        f.write(str1+"\n")
    f.close()

def enc1_write_no_weight_simplified(ll, var_dic, name):
    print('writing enc1_simplified to file')
    fname = '/Users/tianyangsun/Documents/Project/Github_repo/enc1_results' + name + '_enc1.cnf'
    f = open(fname, "w")
    #print(len(ll))
    f.write("c This is the enc1_simplified file generate by sty"+"\n")
    f.write("p cnf "+ str(max(var_dic.values())) +" " + str(len(ll)) +"\n")
    for i in ll:
        # list1 = [1, 2, 3]
        str1 = ''.join(str(e)+' ' for e in i)
        str1 = str1.join(" 0")
        f.write(str1+"\n")
    f.close()


def enc2_write_no_weight_simplified(ll, var_dic, name):
    print('writing enc2 to file')
    fname = '/Users/tianyangsun/Documents/Project/Github_repo/enc2_results' + name + '_enc2.cnf'
    f = open(fname, "w")
    f.write("c This is the enc2 file generate by sty"+"\n")
    f.write("p cnf "+ str(max(var_dic.values())) +" " + str(len(ll)) +"\n")
    for i in ll:
        # list1 = [1, 2, 3]
        str1 = ''.join(str(e)+' ' for e in i)
        str1 = str1.join(" 0")
        f.write(str1+"\n")
    f.close()


def enc3_write_no_weight_simplified(ll, var_dic, name):
    print('writing enc3 to file')
    fname = '/Users/tianyangsun/Documents/Project/Github_repo/enc3_results' + name + '_enc3.cnf'
    f = open(fname, "w")
    #print(len(ll))
    f.write("c This is the enc3 file generate by sty"+"\n")
    f.write("p cnf "+ str(max(var_dic.values())) +" " + str(len(ll)) +"\n")
    for i in ll:
        # list1 = [1, 2, 3]
        str1 = ''.join(str(e)+' ' for e in i)
        str1 = str1.join(" 0")
        f.write(str1+"\n")
    f.close()