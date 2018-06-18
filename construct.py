
from numpy import *

from collections import OrderedDict
from itertools import chain, combinations

import flippable

#import time

sep4 = [
    [15, 14, 13, 12, 11, 10, 7, 6],#
    [15, 14, 13, 12, 11, 10, 7, 9],#

    [15, 14, 13, 12, 11, 10, 9, 7],#
    [15, 14, 13, 12, 11, 10, 9, 8],#

    [15, 14, 13, 12, 11, 7, 10, 6],
    [15, 14, 13, 12, 11, 7, 10, 9],#


    [15, 14, 13, 11, 12, 10, 7, 6],#
    [15, 14, 13, 11, 12, 10, 7, 9],#

    [15, 14, 13, 11, 12, 10, 9, 7],#
    [15, 14, 13, 11, 12, 10, 9, 8],#

    [15, 14, 13, 11, 12, 7, 10, 9],#
    [15, 14, 13, 11, 12, 7, 10, 6],

    [15, 14, 13, 11, 7, 12, 10, 9],#
    [15, 14, 13, 11, 7, 12, 10, 6]
]

def all_subsets(ss):
    #return sum(map(lambda r: list(combinations(ss, r)), range(1, len(ss)+1)), [])
    subsets =  chain(*map(lambda x: combinations(ss, x), range(0, len(ss) + 1)))
    return subsets

def get_subsets(ss,m):
    return combinations(ss, m)


def get_as_big(num, lower_bound):
    if (num < lower_bound):
        return 0
    else:
        return 1





#def downshift(bin_array, index):
#   del bin_array[index]


def check_middle_cols(new_data, dim):

    new_data_bin_list = [decimal_to_bin_array(x, dim + 1) for x in new_data]

    myarray = array(new_data_bin_list)

    ### mask different columns and check them
    ### we already know that columns 1 and dim+1 are good
    is_good = True
    for idx in range(1, dim):
        #print('--- idx', idx)
        mask = zeros_like(myarray)
        mask[:, [idx]] = 1
        masked_array = ma.masked_array(myarray, mask)
        compressed_array = ma.compress_rowcols(masked_array, 1)

        check_data = [bin_array_to_decimal(x) for x in compressed_array]
        # remove duplicates
        check_data = list(OrderedDict((x, True) for x in check_data).keys())

        #print(check_data)
        #print(check_data in data3)
        if check_data not in start_data:
            is_good = False
            break

    return is_good


def generate(mydata, dim):
    #### mydata is the data to extend
    new_prefs = []

    #print('mydata', mydata)
    mydata_half = [mydata[i] for i in range(0, len(mydata) // 2)]

    my_cutoff = 2 ** (dim - 1)
    #print('my_cutoff=', my_cutoff)
    first = [get_as_big(x, my_cutoff) for x in mydata]

    prefix = [x for x in mydata if x < my_cutoff]

    #print('first', first)
    #print('prefix', prefix)

    mydata_half2 = [2 * x for x in mydata_half]

    print(mydata_half, mydata_half2)

    children = parent_dic[flippable.data_to_id(prefix)]
    #print('children', children)

    for child in children:
        print('handling child', child)
        mychild_bin = [x % 2 for x in child]

        #print('mychild_bin', mychild_bin)

        indices1 = [i for i, e in enumerate(mychild_bin) if e == 1]
        # indices0 = set(range(0,len(mychild_bin))) - set(indices1)

        #print('indices1', indices1)
        # print(indices0)

        new_data_top_half = [x for x in mydata_half2]

        #print('new data half', new_data_top_half)

        for i, idx in enumerate(indices1):
            #print('\t\t', i , idx)
            new_data_top_half.insert(idx, 1 + mydata_half2[i])

        #print('new half data is', new_data_top_half)

        new_top_half_as_bin = [decimal_to_bin_array(x, dim + 1) for x in new_data_top_half]

        # reversed and complement
        new_data_bottom_half = [2 ** (dim + 1) - 1 - x for x in reversed(new_data_top_half)]

        # check straight appending
        new_data = new_data_top_half + new_data_bottom_half

        if check_middle_cols(new_data, dim):
            new_prefs.append(new_data)

        # how many ways can we stitch? at least one
        # new_data_bottom_half = [7,6,5,4,3,2,1,0]
        stitch_data = [x ^ (new_data_bottom_half[0]) < 2 ** dim for x in new_data_bottom_half]
        try:
            stitch_end = stitch_data.index(False)
        except ValueError:
            stitch_end = len(stitch_data)

        #print("stitchable:", stitch_data, stitch_end)

        # xxxab need to consider all possible subsets, i think
        # for stitch_idx in range(0, stitch_end):
        #     print('>>>>>>>>>>>>>> stitching', stitch_idx, new_data_top_half[0: len(new_data_top_half) - stitch_idx])
        #     stitch_pref = new_data_top_half[0: len(new_data_top_half) - stitch_idx] \
        #                + new_data_bottom_half[0: stitch_idx] \
        #                + new_data_top_half[len(new_data_top_half) - stitch_idx: len(new_data_top_half)] \
        #                + new_data_bottom_half[stitch_idx: len(new_data_bottom_half)]
        #
        #     if check_middle_cols(stitch_pref, dim):
        #         print('>>>>>>>>', stitch_pref)
        #         new_prefs.append(stitch_pref)

        # for stitch_idx in range(0, stitch_end):
        #     stitch_sets = all_subsets(range(0, stitch_end))
        #
        #     for stitch_set in stitch_sets:
        #          if len(stitch_set) > 0:
        #             stitch_pref = interweave(new_data_top_half, new_data_bottom_half, stitch_set)
        #             if check_middle_cols(stitch_pref, dim):
        #                 print('>>>>>>>>', stitch_pref)
        #                 new_prefs.append(stitch_pref)

        print('\tstitch end=', stitch_end)

        my_len = len(new_data_top_half)

        for stitch_size in range(0, stitch_end):
            stitch_sets = get_subsets(range(my_len - stitch_end, my_len), stitch_size)

            for stitch_set in stitch_sets:
                 if len(stitch_set) > 0: #and stitch_set != (2**dim-1,) and stitch_set !=(2**dim-2, 2**dim-1):
                    stitch_pref = interweave(new_data_top_half, new_data_bottom_half, stitch_size, stitch_set)
                    if check_middle_cols(stitch_pref, dim):
                        #print('>>>>>>>>', stitch_pref)
                        new_prefs.append(stitch_pref)


    return new_prefs

# assuming list1 and list2 have the same size
def interweave_old(list1, list2, idx_list):
    #print('***** interveave:', list1, list2, idx_list)
    size = len(list1)
    weave_size = len(idx_list)
    top = list1[:size-weave_size]
    bottom = list2[weave_size:]
    weave_top = list1[size - weave_size:]
    weave_bottom = list2[:weave_size]

    #print("top:", top, weave_top)
    #print("bottom:", bottom, weave_bottom)


    for i,idx in enumerate(idx_list):
        print(i,idx)
        weave_top.insert(idx,weave_bottom[i])

    #print("\t******",  top + weave_top + bottom)

    return top + weave_top + bottom

# assuming list1 and list2 have the same size
def interweave(list1, list2, weave_size, weave_idx):
    #print('***** interveave:', list1, list2, weave_size, weave_idx)
    size = len(list1)
    top = list1[:size-weave_size]
    bottom = list2[weave_size:]
    weave_top = list1[size - weave_size:]
    weave_bottom = list2[:weave_size]

    #print("top:", top, weave_top)
    #print("bottom:", bottom, weave_bottom)


    for i,idx in enumerate(weave_idx):
        #print(i,idx)
        top.insert(idx,weave_bottom[i])

    #print("\t******",  top)

    return flippable.data_from_top_half(top)



############################
# constructs preferences of size n+1 from preferences of size n

data2 = [ [3, 2, 1, 0]]

data3 = [[7,6,5,4,3,2,1,0], [7,6,5,3,4,2,1,0]]


data4part1 = [
    [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
    [15, 14, 13, 12, 11, 7, 10, 9, 6, 5, 8, 4, 3, 2, 1, 0],
    [15, 14, 13, 12, 11, 10, 7, 9, 6, 8, 5, 4, 3, 2, 1, 0],
    [15, 14, 13, 12, 11, 7, 10, 6, 9, 5, 8, 4, 3, 2, 1, 0],
    [15, 14, 13, 11, 12, 10, 9, 8, 7, 6, 5, 3, 4, 2, 1, 0],
    [15, 14, 13, 11, 7, 12, 10, 9, 6, 5, 3, 8, 4, 2, 1, 0],
    [15, 14, 13, 11, 12, 7, 10, 9, 6, 5, 8, 3, 4, 2, 1, 0],
    [15, 14, 13, 11, 12, 10, 7, 9, 6, 8, 5, 3, 4, 2, 1, 0],
    [15, 14, 13, 11, 7, 12, 10, 6, 9, 5, 3, 8, 4, 2, 1, 0],
    [15, 14, 13, 11, 12, 7, 10, 6, 9, 5, 8, 3, 4, 2, 1, 0],
]

data4part2 = [
    [15, 14, 13, 12, 11, 10, 7, 6, 9, 8, 5, 4, 3, 2, 1, 0],
    [15, 14, 13, 12, 11, 10, 9, 7, 8, 6, 5, 4, 3, 2, 1, 0],
    [15, 14, 13, 11, 12, 10, 7, 6, 9, 8, 5, 3, 4, 2, 1, 0],
    [15, 14, 13, 11, 12, 10, 9, 7, 8, 6, 5, 3, 4, 2, 1, 0],
]

data4 = data4part1 + data4part2




dim = 4
start_data = data4



parent_dic = {}
#parent_dic[flippable.data_to_id(data2[0])] = data3
parent_dic[flippable.data_to_id(data3[0])] = data4part1
parent_dic[flippable.data_to_id(data3[1])] = data4part2

print(parent_dic)

new_prefs = []

for mydata in start_data:
    print('handling ', mydata)
    new_prefs = new_prefs + generate(mydata, dim)


#new_prefs = new_prefs + generate(data4[13], dim)

print('done')

print(len(new_prefs))

#for pref in new_prefs:
#    print(pref)


pref_list2 = [flippable.data_to_id(pref) for pref in new_prefs]

print(len(set(pref_list2)))




#print(interweave([1,2,3,4,5,6,7,8],[11,22,33,44,55,66,77,88],2, {4,5}))