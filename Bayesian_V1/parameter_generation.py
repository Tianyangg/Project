import itertools
import copy
# test for output of several combination of lists

list1 = [[1,2]]#, [5,6,7,8]] #, [9,10,11,12,13,14]]
list2 = [[1,2], [5,6,7]] #, [9,10,11,12,13,14]]
list3 = [[1,2], [5,6], [9,10], [3,4, 8]]
#result = []
#result.clear()

# method zipper pick one elements in each sublist and return the combination

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def zipper(l):
    result = []
    if len(l) == 1:
        # turn [1,2,3,4] into [[1][2][3][4]]
        result.extend(list(chunks(l[0], 1)))
    elif len(l) == 2:
        result.extend([[x,y] for x in l[0] for y in l[1]])
    else:

        temp = l.pop(0) # this return a list of elements

        ctr = 0 # this it genera counter
        result2 = []
        result1 = zipper(l)

        for m in range(0, len(temp)):
            copynoref = copy.deepcopy(result1)
            result2.extend(copynoref)

        for x in temp:
            for y in result1:
                result2[ctr].insert(0, x)
                #result2[ctr].append(x)
                ctr += 1
        result.clear()
        result.extend(result2.copy())
    return result

def tuple_to_string(tuple):
    temp1 = tuple[0] # that's the name::str??
    temp2 = tuple[1] # that's the number :: integer?
    return temp1+str(temp2)

def list_tuple_to_str(l):
    return [tuple_to_string(x) for x in l]

#print(tuple_to_string(("test", 123)))
