from __future__ import print_function, division


import itertools
import numpy as np


def bin_tuple_to_decimal(bin_tuple):
    return  sum(x * 2**i for i,x in enumerate(reversed(bin_tuple)))

# Converts a binary array to a decimal
# Converts [1,0] to 2
# Converts [0,1] to 1
# Converts [1,1] to 3
# Converts [1,0,1,0] to 8 + 2 = 10
def bin_array_to_decimal(bin_array):
    return bin_tuple_to_decimal(tuple(bin_array))

def decimal_to_bin_array(decimal, dim):
    """ Given a whole, decimal integer,
        convert it to a binary
        representation
    """
    # This function supports non-negative, whole integer only.
    if not isinstance(decimal, int) or decimal < 0:
        raise TypeError('Input must be a non-negitive, whole integer.')
    # we need a stack to store each binary digit in.
    stack = []
    # while their are still digits left
    # to convert in decimal.
    while decimal > 0:
        # caclute each binary number by dividing decimal
        # by two. And since we are 'building' our binary
        # string backwards, insert() in the front of the
        # list instead of append()-ing to the back.
        stack.insert(0, decimal % 2)
        # after we've calcute the binary value of the current
        # decimal, divide the decimal by 2. But make sure we
        # use // instead of / to get a while number!
        decimal = decimal // 2

    return [0 for i in range(0,dim - len(stack))] + [ x for x in stack]

def data_to_bin_array(data, dim):
    return [decimal_to_bin_array(x, dim) for x in data]

# recover full id from the first half
# Converts [3,2] to [3,2,1,0]
def data_from_top_half(list1):
    d = 2 * len(list1)-1
    top = [x for x in list1]
    bottom = [d - x for x in reversed(top)]
    return top + bottom

### converts the top half to binary
### and stores it in a dictionary
def get_csp_bin_from_top(top_tuple, dim):
    #top = [t for t in top_tuple]

    data = data_from_top_half(top_tuple)
    bin_data = data_to_bin_array(data, dim-1)

    return bin_data

# gets the csp bin for the address
def get_csp_bin_for_address(prev_stage, address, dim):

    csp_list = []

    for i in range(len(address) - 1):
        csp_list.append(prev_stage[address[i]])

    #print('\tcsp_list',csp_list)

    csp_bin_list = [get_csp_bin_from_top(x, dim) for x in csp_list]

    return csp_bin_list


# recover full id from the first half
# Converts [3,2] to [3,2,1,0]
def data_from_top_half(list1):
    d = 2 * len(list1)-1
    top = [x for x in list1]
    bottom = [d - x for x in reversed(top)]
    return top + bottom

def line_passes(line, csp_bin_list, idx_list):

    passes = True

    for i,x in enumerate(line):
        if x == 1:
            temp_line = [y for y in line]
            temp_line.pop(i)

            # if (len(idx_list) == 6):
            #     print(i,x,line, idx_list)
            #     print(len(csp_bin_list))
            #     print(csp_bin_list)
            #     print(csp_bin_list[i])

            if not temp_line == csp_bin_list[i][idx_list[i]]:
                #print(line, temp_line, 'fails', i, csp_bin_list[i][idx_list[i]])
                passes = False
                break

    return passes

# returns adjacent pairs of a list
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

# whether num is a power of 2 or zero
def is_power2_or_zero(num):
    return ((num & (num - 1)) == 0)

# gets the primitive pairs, which are adjacent lines that are
# bitwise disjoint
def get_primitive_pairs(data):
    primitive_pairs = []

    for pair in pairwise(data):
        if (pair[0] + pair[1] == pair[0] ^ pair[1]):
            primitive_pairs.append(pair)
            #print('\t', '{0:04b}'.format(pair[0]), '{0:04b}'.format(pair[1]))

    return primitive_pairs

# turns a decimal into a binary number
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


# returns alist of all subsets of the list arr
def list_of_subsets(arr):
    """returns a list of all subsets of a list"""

    combs = []
    for i in range(0, len(arr) + 1):
        listing = [list(x) for x in itertools.combinations(arr, i)]
        combs.extend(listing)
    return combs

# Given a pair, returns all possible subsets of the complement
# of the union of the pair. This allows us to create the sister
# pairs that must also flip when we flip the given pair
def get_comp_subsets(pair, dim):
    comp = 2 ** dim - 1 - (pair[0] + pair[1])
    #print('\t comp=', comp)
    # print('\t', pair)
    # print('\t\t', get_binary(bin_comp))
    binary_comp = get_binary(comp)

    return list_of_subsets(binary_comp)


# Returns all the pairs of adjacent rows that are disjoint and flippable
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




# swap all occurrences of flippable A and B
def flip(data, pair, dim):
    comp_subsets = get_comp_subsets(pair, dim)

    new_data = list(data)

    for s in comp_subsets:
        t = sum(s)
        p0, p1 = data.index(t + pair[0]), data.index(t + pair[1])
        new_data[p1], new_data[p0] = data[p0], data[p1]

    return new_data

### returns an int corresponding to the tuple.
### I think that the tuple is a more efficient storage mechanism than
### the string id
def idnum_for_tuple(prev_stage, tuple):
    return prev_stage.index(tuple)

# converts [3,2,1,0] to (3,2)
def tuple_from_data(data):
    half = len(data)//2
    return tuple(data[:half])

# takes binary data and turns it into an address, which is a list of size n+1
# the first n entries are the ids of the CSP you get by deleting the ith column
# the final entry is either 1 or 0, depending on whether there is a central flip
def generate_address(prev_stage, data, dim):

    parent_list = []

    data_bin = data_to_bin_array(data, dim)

    for idx in range(0, dim):
        # print('\t handling idx', idx)

        mask_row_idx_list = []
        for i, d in enumerate(data_bin):
            if d[idx] == 0:
                mask_row_idx_list.append(i)

        data_array = np.array(data_bin)

        m = np.zeros_like(data_array)
        m[mask_row_idx_list, 0] = 1

        masked_array1 = np.ma.masked_array(data_array, m)
        c_array1 = np.ma.compress_rows(masked_array1)

        m2 = np.zeros_like(c_array1)
        m2[0, idx] = 1

        ma2 = np.ma.masked_array(c_array1, m2)
        ca2 = np.ma.compress_cols(ma2)


        parent_data = [bin_array_to_decimal(x) for x in ca2]

        parent_list.append((parent_data))

    # print(parent_list)

    address = [idnum_for_tuple(prev_stage, tuple_from_data(p)) for p in parent_list]

    if data[2 ** (dim - 1) - 1] < 2 ** (dim - 1):
        address.append(0)
    else:
        address.append(1)

    return tuple(address)

# recreates the top data from the address
def regenerate_top_data(prev_stage, address, dim):

    #print('regenerate', address)

    csp_bin_list = get_csp_bin_for_address(prev_stage, address, dim)

    top_idx = 0
    bottom_idx = 0

    idx_list = [0] * dim

    working_csp = []

    while(len(working_csp) < 2**(dim-1)):
        top_line = [1,]+ csp_bin_list[0][top_idx]
        bottom_line = [0,] + csp_bin_list[0][bottom_idx]

#        if dim == 6:
#            print(address)
#            print('top', top_line, 'bottom', bottom_line)
#            print(csp_bin_list)

        # xxxab
        # for performance on AWS, we should eliminate the second
        # line_passes check below. By design, it has to pass!
        if line_passes(top_line, csp_bin_list, idx_list):
            line = top_line
            top_idx = top_idx + 1
        elif line_passes(bottom_line, csp_bin_list, idx_list):
            line = bottom_line
            bottom_idx = bottom_idx + 1
        else:
            #print('both failed', top_line, bottom_line)
            #print('working csp', working_csp)
            raise ValueError('both top and bottom failed', top_line, bottom_line)

        working_csp.append(line)

        # advance the appropriate counters
        for i,x in enumerate(line):
            if x == 1:
                idx_list[i] = idx_list[i] + 1



    # take care of the middle flip
    if address[-1] == 0:
        working_csp[-1] = [1-x for x in working_csp[-1]]

    #print(working_csp)

    regen_data = [bin_array_to_decimal(x) for x in working_csp]

    return regen_data


def discover_prefs(prev_stage, initial_node, dim):
    frontier = set()
    visited = []
    frontier.add(initial_node)

    print('discovering from', initial_node, dim)

    while frontier:
        node = frontier.pop()
        for neighbor in node_neighbors(prev_stage, node, dim):
            if neighbor not in visited:
                frontier.add(neighbor)

        visited.append(node)
        if len(visited) % 1000 == 0:
            print('visited=%d, frontier=%d' % (len(visited), len(frontier)))

    return [tuple(regenerate_top_data(prev_stage, p, dim)) for p in visited]

SEP_4 = (
    (15, 14, 13, 12, 11, 10, 7, 6),#
    (15, 14, 13, 12, 11, 10, 7, 9),#

    (15, 14, 13, 12, 11, 10, 9, 7),#
    (15, 14, 13, 12, 11, 10, 9, 8),#

    (15, 14, 13, 12, 11, 7, 10, 6),
    (15, 14, 13, 12, 11, 7, 10, 9),#


    (15, 14, 13, 11, 12, 10, 7, 6),#
    (15, 14, 13, 11, 12, 10, 7, 9),#

    (15, 14, 13, 11, 12, 10, 9, 7),#
    (15, 14, 13, 11, 12, 10, 9, 8),#

    (15, 14, 13, 11, 12, 7, 10, 9),#
    (15, 14, 13, 11, 12, 7, 10, 6),

    (15, 14, 13, 11, 7, 12, 10, 9),#
    (15, 14, 13, 11, 7, 12, 10, 6)
)

def sparkless_main():


    sep5 = discover_prefs(SEP_4,(3, 3, 3, 3, 3, 1), 5)
    print(len(sep5))
    sep6 = discover_prefs(sep5, (0,0,0,0,0,0,1), 6)
    print(len(sep6))
    #sep7 = discover_prefs(sep6, (0,0,0,0,0,0,0,1), 7)
    #print(len(sep7))

def node_neighbors(prev_stage, node, dim):
    top_data = regenerate_top_data(prev_stage, node, dim)
    data = data_from_top_half(top_data)
    flippable_pairs = get_flippable_pairs(data, dim)
    flipped_data = [flip(data, flip_pair, dim) for flip_pair in flippable_pairs]

    neighbors = []
    for pair, f in zip(flippable_pairs, flipped_data):
        neighbors.append(generate_address(prev_stage, f, dim))
    return neighbors


import json


def dump_and_count(num_lines, node):
    num_lines += 1
    return json.dumps(node)

def node_to_file(sc, node_rdd, path):
    num_lines = sc.accumulator(0)

    node_rdd \
        .map(lambda node: dump_and_count(num_lines, node)) \
        .coalesce(100, False) \
        .saveAsTextFile(path)

    return num_lines.value

def file_to_nodes(sc, path):
    return sc.textFile(path) \
      .map(lambda line: tuple(json.loads(line)))

def discover_prefs_spark(sparkContext, prefix, initial_node, dim):
    print('discovering from', initial_node, dim)

    sc = sparkContext

    prev_stage = file_to_nodes(sc, '%s/dim-%d/final.visited' % (prefix, dim-1)).collect()
    print(prev_stage)
    prefix += '/dim-' + str(dim)

    prev_stage_bc = sc.broadcast(prev_stage)

    node_to_file(sc, sc.parallelize([initial_node]), prefix + '/0.frontier')
    node_to_file(sc, sc.parallelize([]), prefix + '/0.visited')

    for i in itertools.count():
        print('starting %d' % i)
        frontier = file_to_nodes(sc, '%s/%d.frontier' % (prefix, i))

        # Calculate nodes that can be seen in the next step
        reachable = frontier.flatMap(lambda node: node_neighbors(prev_stage_bc.value, node, dim)).distinct()
        # print('reachable length after %d is %d' % (i, reachable.count(),))
        node_to_file(sc, reachable, '%s/%d.reachable' % (prefix, i))

        # Calculate the next visited based on the current one visited and frontier
        visited = file_to_nodes(sc, '%s/%d.visited' % (prefix, i))
        next_visited = visited.union(frontier).distinct()
        # print('visited length after %d is %d' % (i, next_visited.count(),))
        node_to_file(sc, next_visited, '%s/%d.visited' % (prefix, i + 1))

        # Calculate the next frontier
        next_frontier = reachable.subtract(next_visited)
        # print('frontier length is %d' % (next_frontier.count(),))
        frontier_size = node_to_file(sc, next_frontier, '%s/%d.frontier' % (prefix, i + 1))
        print('size of frontier is %d' % frontier_size)

        if frontier_size == 0:
            node_to_file(sc, next_visited, '%s/final.visited' % (prefix,))
            break


def spark_main():
    from pyspark import SparkContext, SparkConf

    from pyspark.serializers import MarshalSerializer


    prefix = '/Users/ssen/PycharmProjects/voter/bfs'

    conf = SparkConf().setAppName("CSP").setMaster("local[*]")
    sc = SparkContext(conf=conf, serializer=MarshalSerializer())
    sc.setLogLevel("WARN")

    # Write the fourth step if it already exists, that's fine!
    node_to_file(sc, sc.parallelize(SEP_4), '%s/dim-4/final.visited' % (prefix,))

    discover_prefs_spark(sc, prefix, (3, 3, 3, 3, 3, 1), 5)


# sparkless_main()
spark_main()