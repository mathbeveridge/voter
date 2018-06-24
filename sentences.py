import itertools
import prefutils
import numpy as np


# generates a sentence of words consisting of A's and B's according to the 3-sets of [n]
# the words are in lex order, according to smallest element in the 3-set
# this tests a lemma of Ian's from 6/18


def get_type(my_array):
    if (my_array[3, 0] == 1):
        retval = 'A'
    else:
        retval = 'B'

    return retval


dim = 5

#ids = prefutils.get_id_list(dim)

ids = [ '31-30-29-27-23-28-26-22-25-15-21-19-24-14-20-13' ]
# '31-30-29-27-23-28-26-22-15-14-25-21-19-24-20-13',
#        '31-30-29-27-23-28-26-22-15-14-25-21-19-24-20-18',
#        '31-30-29-27-28-23-26-22-15-14-25-21-24-19-20-13',
#        '31-30-29-27-28-23-26-22-15-25-21-14-24-19-20-18',
#        '31-30-29-28-27-26-23-22-15-14-25-24-21-20-13-12'
#        ]



my_set = set(range(dim))

sets3 = list(itertools.combinations(my_set, 3))

print(sets3)

for id in ids:
    data = prefutils.data_from_id(id)
    data_bin = prefutils.data_to_bin_array(data, dim)

    print(id)
    print(data_bin)

    sentence = {}

    for set3 in sets3:

        comp_set3 = my_set.difference(set3)
        print(set3, comp_set3)

        mask_row_idx_list = []

        for i, d in enumerate(data_bin):
            c = [d[idx] for idx in comp_set3]
            #print('c', c)
            c_set = set(c)

            if not (len(c_set) == 1 and c_set.pop() == 0):
                #print("masking row", i)
                mask_row_idx_list.append(i)

        data_array = np.array(data_bin)

        m = np.zeros_like(data_array)

        m[mask_row_idx_list, :] = 1

        # print(data_array)

        masked_array1 = np.ma.masked_array(data_array, m)

        #print(masked_array1)
        c_array1 = np.ma.compress_rows(masked_array1)

        #print('=====',c_array1)

        m2 = np.zeros_like(c_array1)
        # print('m2', m2)

        for idx in comp_set3:
            m2[:, idx] = 1

        # print('m2', m2)

        ma2 = np.ma.masked_array(c_array1, m2)
        ca2 = np.ma.compress_cols(ma2)

        #print(ca2)

        min_val = min(set3)

        if min_val in sentence.keys():
            word = sentence[min_val]
        else:
            word = []

        word.append(get_type(ca2))

        sentence[min_val] = word

        print(word)

    print(data_array)

    print(sentence)


