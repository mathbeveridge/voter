import os as os
import itertools

# one of the first python scripts that I wrote.
# it contains helper code to convert one CSP into another via
# the flip operation

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def bytes_xor(a, b) :
    return bytes(x ^ y for x, y in zip(a, b))



def get_binary(num):
    #print(num)

    if num == 0:
        return []
    elif num % 2 == 0:
        return [2 * x for x in get_binary(num//2)]
    else:
        temp_list = [2 * x for x in get_binary(num//2)]
        temp_list.append(1)
        return temp_list

# def from_binary(bin_list):
#     mylist = reversed(bin_list)
#     mylist2 = [ x * 2**i for i,x in enumerate(mylist)]
#     return sum(mylist2)

def subsets(s):
    for cardinality in range(len(s) + 1):
        yield from itertools.combinations(s, cardinality)


def is_power2_or_zero(num):
    return ((num & (num - 1)) == 0)


def get_primitive_pairs(data):
    primitive_pairs = []

    for pair in pairwise(data):
        if (pair[0] + pair[1] == pair[0] ^ pair[1]):
            primitive_pairs.append(pair)
            #print('\t', '{0:04b}'.format(pair[0]), '{0:04b}'.format(pair[1]))

    return primitive_pairs


def get_lex_primitive_pairs(data):
    primitive_pairs = get_primitive_pairs(data)

    pair_list = []

    for pair in primitive_pairs:
        if not is_power2_or_zero(pair[0]) or not is_power2_or_zero(pair[1]):
            pair_list.append(pair)

    return pair_list


def get_comp_subsets(pair, dim):
    comp = 2 ** dim - 1 - (pair[0] + pair[1])
    #print('\t comp=', comp)
    # print('\t', pair)
    # print('\t\t', get_binary(bin_comp))
    binary_comp = get_binary(comp)

    return list_of_subsets(binary_comp)

def get_flippable_pairs(data, dim):
    primitive_pairs = get_primitive_pairs(data)

    flippable_pairs = []

    for pair in primitive_pairs:
        # pairs of singletons are not flippable since they must be in lexicographical order
        # so skip the pair if both are powers of 2
        if not is_power2_or_zero(pair[0]) or not is_power2_or_zero(pair[1]) :

            #print('flippable', pair)
            comp_subsets = get_comp_subsets(pair, dim)

            is_flippable = True

            for s in comp_subsets:
                t = sum(s)
                # print('\t', data.index(pair[0] + t), data.index(pair[1] + t))
                if abs(data.index(pair[0] + t) - data.index(pair[1] + t)) > 1:
                    is_flippable = False
                    break

            if is_flippable:
                #print("\t adding flippable:", pair)
                flippable_pairs.append(pair)
        #else:
        #    print("\t skipping pair", pair)

    return flippable_pairs


# this is a variation of the previous method
def get_largest_gap(data, dim):
    primitive_pairs = get_primitive_pairs(data)

    gap = 0

    for pair in primitive_pairs:
        # pairs of singletons are not flippable since they must be in lexicographical order
        # so skip the pair if both are powers of 2
        if not is_power2_or_zero(pair[0]) or not is_power2_or_zero(pair[1]) :

            if pair[0] < pair[1]:
                #print('flippable', pair)
                comp_subsets = get_comp_subsets(pair, dim)

                is_flippable = True

                for s in comp_subsets:
                    t = sum(s)
                    # print('\t', data.index(pair[0] + t), data.index(pair[1] + t))
                    temp_gap = abs(data.index(pair[0] + t) - data.index(pair[1] + t))
                    gap = max(gap,temp_gap)
                    if temp_gap > 7:
                        print("#####", temp_gap, pair, pair[0]+t, pair[1]+t, data_to_id(data))

    return gap


# swap all occurrences of flippable A and B
def flip(data, pair, dim):
    comp_subsets = get_comp_subsets(pair, dim)

    new_data = list(data)

    for s in comp_subsets:
        t = sum(s)
        p0, p1 = data.index(t + pair[0]), data.index(t + pair[1])
        new_data[p1], new_data[p0] = data[p0], data[p1]

    return new_data




##########

def list_of_subsets(arr):
    """returns a list of all subsets of a list"""

    combs = []
    for i in range(0, len(arr) + 1):
        listing = [list(x) for x in itertools.combinations(arr, i)]
        combs.extend(listing)
    return combs

def data_to_str(data):
    return '-'.join(str(x) for x in data)

def data_from_str(data_str):
    return [ int(x) for x in data_str.split('-')]


# only use first half for the id to make it smaller
def data_to_id(data):
    half = len(data)//2
    return '-'.join(str(x) for x in data[:half])

# recover full id from the first half
def data_from_id(data_str):
    list1 = [ int(x) for x in data_str.split('-')]
    return data_from_top_half(list1)
#    d = 2 * len(list1)-1
#    list2 = [d - x for x in reversed(list1)]
#    return list1 + list2

# recover full id from the first half
def data_from_top_half(list1):
    d = 2 * len(list1)-1
    list2 = [d - x for x in reversed(list1)]
    return list1 + list2

######


#dim = 4
#filenames = [ "/bean/mac/research/tran/n4sep/s3v1s4v1.csv",
#              "/bean/mac/research/tran/n4sep/s3v1s4v2.csv" ]
#out_file_name = "/bean/mac/research/tran/n4sep-coef/n4edges.csv"

# this is the file system version of gensep and gensepbatch
def run():

    dim = 6
    dirname = "/bean/mac/research/tran/n5sep/"
    filenames = os.listdir(dirname)
    filenames = [dirname + fn for fn in filenames]

    out_file_name = "/bean/mac/research/tran/n5sep-coef/n5edges.csv"

    edges = set()

    for filename in filenames:

        print('================', filename)

        # read the file
        file = open(filename, "r")
        lines = file.readlines()

        for line in lines:
            data = [int(s, 2) for s in line.split(',')]

            data_str = data_to_str(data)

            print(data)

            # print("primitive pairs:")

            # print(get_primitive_pairs(data))

            flippable_pairs = get_flippable_pairs(data,dim)

            print("flippable pairs:", flippable_pairs, '\n')

            flipped_data = [flip(data, flip_pair, dim) for flip_pair in flippable_pairs]

            for f in flipped_data:
                print('\t', f)

                f_str = data_to_str(f)

                if (data_str < f_str):
                    edges.add(data_str + ',' + f_str)
                else:
                    edges.add(f_str + ',' + data_str)


                    # bin_pairs = pairwise()

    out_file = open(out_file_name, "w")

    for edge in edges:
        print(edge)
        out_file.write(edge + '\n')
