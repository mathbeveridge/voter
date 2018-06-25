import itertools

# one of the first python scripts that I wrote.
# it contains helper code to convert one CSP into another via
# the flip operation

# returns adjacent pairs of a list
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

# returns an array containing the xor of two arrays
def bytes_xor(a, b) :
    return bytes(x ^ y for x, y in zip(a, b))


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


# returns all possiblesubsets
def subsets(s):
    for cardinality in range(len(s) + 1):
        yield from itertools.combinations(s, cardinality)

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

# Gets the primitive pairs, and removes the ones that we don't want to
# flip: namely when the adjacent pair are both singletons (or zero).
# This keeps the CSP is the standard form
def get_lex_primitive_pairs(data):
    primitive_pairs = get_primitive_pairs(data)

    pair_list = []

    for pair in primitive_pairs:
        if not is_power2_or_zero(pair[0]) or not is_power2_or_zero(pair[1]):
            pair_list.append(pair)

    return pair_list


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




##########

# returns alist of all subsets of the list arr
def list_of_subsets(arr):
    """returns a list of all subsets of a list"""

    combs = []
    for i in range(0, len(arr) + 1):
        listing = [list(x) for x in itertools.combinations(arr, i)]
        combs.extend(listing)
    return combs




