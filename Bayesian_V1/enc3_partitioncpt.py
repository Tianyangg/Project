from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import ExactInference
from pgmpy.inference import VariableElimination
from Bayesian_V1 import qm


def parameter_to_number(l):
    numbers = []
    for element in l:
        temp = [element[1]]
        for i in element[2]:
            temp.append(i[1])
        numbers.append(temp)
    return numbers

def parameter_to_name(l):
    names = []
    for element in l:
        temp = [element[0]]
        for i in element[2]:
            temp.append(i[0])
        names.append(temp)
    return names

# my_max: given a list of (array of numbers)
# return the largest number in a column
# use: to decide the length of binary number to represent each variable
def my_max(l):
    mymax = []
    if l:
        mymax = l[0] #[1,2,4] e.g
        for i in l:
            for j in range(0, len(i)):
                if mymax[j] < i[j]:
                    mymax[j] = i[j]
    return mymax


# switch the direction of storting the lists
# do twice and you'll get the original one
def row_to_col(l):
    result = []
    if l:
        for j in range(0, len(l[0])):
            result.append([e[j] for e in l])
    #print(result)
    return result


def number_to_binary_list(l):
    col_list = row_to_col(l)
    maxnums = my_max(l)
    binmax = ["{0:b}".format(i) for i in maxnums]
    length_binary = [len(i) for i in binmax]
    binary_list = []
    for c in range(0, len(col_list)):
        temp = ["{0:b}".format(decimal).zfill(length_binary[c]) for decimal in col_list[c]]
        binary_list.append(temp)
    return (length_binary, row_to_col(binary_list))
    #.zfill()

# 把结果整合起来，作为输入送到  qm.qm(ones = [list])
def append_binary(bin_list):
    binaries = []
    for i in bin_list:
        temp = ''.join(i)
        binaries.append(temp)
    return binaries

def binary_to_dec(binaries):
    dec = []
    for i in binaries:
        dec.append(int(i, 2))
    return dec

def bins_to_decs(bins):
    decs = []
    for i in bins:
        decs.append([int(j, 2) for j in i])
    return decs

def call_qm(binaries):
    b = number_to_binary_list(binaries)
    sop = qm.qm(ones= binary_to_dec(append_binary(b[1])))
    length = b[0]
    # replace x with 0
    new_sop = [i.replace('X', '0') for i in sop]
    return (new_sop, length)

def split_binary(s, length):
    #print([''.join([s[sum(n[:i]): sum(n[:i + 1])] for i in range(len(n))])])\
    n = length
    res = []
    for j in range(0, len(s)):
        res.append([s[j][sum(n[:i]): sum(n[:i + 1])] for i in range(len(n))])
    return res


def partition(l):
    l.sort(key=lambda x: x[3])
    ctr = 0
    while ctr < len(l):
        list2 = [x for x in list1 if x[3] == l[counter][3]]
        ctr = ctr + len(list2)
        #print(list2)
        ### insert here for partition of one parameter value ######
        par2num = parameter_to_number(list2)
        prime_implicants = call_qm(par2num)
        #print(prime_implicants)
        temp = split_binary(prime_implicants[0], prime_implicants[1])
        decs = bins_to_decs(temp)
        print(decs)

        ###

list1 = [('var', 1, [('Ev', 1), ('Ev', 2)], 0.04),
         ('var', 2, [('Ev', 1), ('Ev', 2)], 0.4),
         ('var', 1, [('Ev', 1), ('Ev', 3)], 0.04),
         ('var', 2, [('Ev', 0), ('Ev', 2)], 0.4)]
#list1.sort(key = lambda x: x[3])
counter = 0
#while counter < len(list1):
#    list2 = [x for x in list1 if x[3] == list1[counter][3]]
#    counter = counter + len(list2)
#    print(list2)

#a = parameter_to_number(list1)
#number_to_binary_list(a)
#temp = number_to_binary_list(a)
#b = call_qm(a)
#print('b'+ str(b))
#temp = split_binary(b[0], b[1])
#print(bins_to_decs(temp))
#print(append_binary(temp))

#print (qm.qm(ones= binary_to_dec(append_binary(temp))))


partition(list1)