import prefutils
from scipy.optimize import linprog
import math
import numpy


def represent(id):
    data = prefutils.data_from_id(id)
    bin_array = prefutils.data_to_bin_array(data, dim)


    #print(bin_array)

    constraints = []

    for i in range(2**dim - 1):
        constraints.append([y-x for x,y in zip(bin_array[i],bin_array[i+1])])
        #constraints.append(data[i]- data[i+1])

    #print(constraints)

    b = [-1] * (2**dim -1)

    c = [1] * dim


    res = linprog(c, constraints, b) #, options={"disp": True})

    #print(res)

    if res['success']:
        return res['x']
    else:
        return []


#####

dim = 6

id_list = prefutils.get_id_list(dim)

count = 0

for id in id_list:
    rep = represent(id)

    #print(id, type(rep), rep)
    if len(rep) == 0:
        count = count + 1
        print(count, id, rep)

print(count)
