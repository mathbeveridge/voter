import mysql.connector
import flippable
import prefutils



### copied from gensepbatch AND FIXED!!!!
def int_to_bin_array(x):
    return [int(z) for z in bin(x)[2:]]


def check_order(x,y):
    return x < y
#    return check_bin_order(x,y)

# ordered by set size, then lex
# returns true if x < y
def check_bin_order(x,y):
    x_bin = int_to_bin_array(x)
    y_bin = int_to_bin_array(y)

    # pad with leading zeros if necessary
    if len(x_bin) < len(y_bin):
        x_bin = [0] * (len(y_bin) - len(x_bin)) + x_bin
    elif len(x_bin) > len(y_bin):
        y_bin = [0] * (len(x_bin) - len(y_bin)) + y_bin

    # this comparison code isn't quite right since [1,0,1,1,0] > [1,1,0,0,1]
    # if sum(x_bin) == sum(y_bin):
    #     #print(x,y,'sums are equal')
    #     diff = [a - b for a, b in zip(x_bin, y_bin)]
    #     #diff.reverse()
    #     #print('\t',diff)
    #     idx = next((i for i, j in enumerate(diff) if not j == 0), None)  # j!= 0 for strict match
    #     #print('\t', idx)
    #     ret_val =  diff[idx] > 0
    # else:
    #     print('second case')
    #     ret_val =  sum(x_bin) < sum(y_bin)

    if sum(x_bin) == sum(y_bin):
        #print(x,y,'sums are equal')
        ret_val = x < y
    else:
        ret_val =  sum(x_bin) < sum(y_bin)

    #print(x,y,x_bin,y_bin,ret_val)
    return ret_val



def bin_array_to_decimal(bin_array):
    return sum(x * 2**i for i,x in enumerate(reversed(bin_array)))


def decimal_to_bin_array(decimal, dim):
    """ Given a whole, decimal integer,
        convert it to a binary
        representation
    """
    # I'm only making this function support
    # non-negative, whole integer only.
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

# def lex_compare(num1, num2, dim):
#
#     bin1 = decimal_to_bin_array(num1, dim)
#     bin2 = decimal_to_bin_array(num2, dim)
#
#     retval = 0
#
#     if sum(bin1) > sum(bin2):
#         retval = 1
#     elif sum(bin1) < sum(bin1):
#         retval = -1
#     else:
#         #same number of digits: use lex
#
#         diff = [x-y for x,y in zip(bin1, bin2)]
#         vals = [x for x in diff if x]
#
#         if len(vals) == 0:
#             retval = 0
#         else:
#             retval = vals[0]
#
#     print(num1, num2, bin1, bin2, retval)
#     return retval

def checkDescendingOrder(id_list):

    for id in id_list:
        data = flippable.data_from_id(id)

        p_list = flippable.get_lex_primitive_pairs(data)
        f_list = flippable.get_flippable_pairs(data, dim)

        p_list2 = []
        for p in p_list:
            if p[0] < p[1]:
                p_list2.append(p)

        f_list2 = []
        for f in f_list:
            if f[0] < f[1]:
                f_list2.append(f)

        if len(f_list2) == 1:
            print('only one', flippable.data_to_id(data))
            print('t', f_list2)

    print('all done')


def check(id_list):
    ### check
    for id in id_list:
        data = flippable.data_from_id(id)

        f_list = flippable.get_flippable_pairs(data, dim)

        found_rev = []
        for f in f_list:
            if data.index(f[0]) < data.index(f[1]):
                if check_order(f[0], f[1]):
                    found_rev.append(f)
            else:
                # I don't think this block ever executes
                print('======== never get here')
                if check_order(f[1], f[0]):
                    found_rev.append(f)

        ff_list = []
        for f in f_list:
            comp = flippable.get_comp_subsets(f, dim)
            pair_list = [[f[0] + sum(s), f[1] + sum(s)] for s in comp]
            ff_list.append(pair_list)

        half_data = data[:len(data) // 2]

        # diff = [x-y for x,y in zip(lex_half_data,half_data)]

        # check for first occurrence
        # location  = next((i for i, x in enumerate(diff) if x), None)

        # if location is None:
        #    pair = []
        # else:
        #    pair = [data[location], data[location+1]]


        pair_reverse = []
        pair_forward = []
        pair_binary = []

        # check for the pair closest to the center that is out of order
        for i in reversed(range(0, 16)):
            # check for the pair closest to the center that is out of order
            # for i in range(0, 16):
            if check_order(data[i], data[i + 1]):
                print('first pair out of order:', data[i], data[i + 1])
                pair_reverse = [data[i], data[i + 1]]
                break

        # check for the pair closest to the center that is out of order
        for i in range(0, 16):
            # check for the pair closest to the center that is out of order
            # for i in range(0, 16):
            if check_order(data[i], data[i + 1]):
                print('first pair out of order:', data[i], data[i + 1])
                pair_forward = [data[i], data[i + 1]]
                break

        # check for the pair closest by "binary search"
        for i in [15, 7, 3, 11, 1, 5, 9, 13, 0, 2, 4, 6, 8, 10, 12, 14]:
            # check for the pair closest to the center that is out of order
            # for i in range(0, 16):
            if check_order(data[i], data[i + 1]):
                print('first bin pair out of order:', i, i + 1, data[i], data[i + 1])
                pair_binary = [data[i], data[i + 1]]
                break

        print(id)
        print('\t', lex_id)
        print('\t', id)
        print('\t', pair_forward, pair_reverse, pair_binary, f_list)
        print('\t\t', ff_list)

        found_reverse = False
        found_forward = False
        found_binary = False

        if len(pair_forward) > 0:
            for ff in ff_list:
                # if pair_reverse in ff:
                #     found_reverse = True
                # if pair_forward in ff:
                #     found_reverse = True
                for x in ff:
                    if x[0] == pair_reverse[0] and x[1] == pair_reverse[1]:
                        found_reverse = True
                    if x[0] == pair_forward[0] and x[1] == pair_forward[1]:
                        found_forward = True
                    if x[0] == pair_binary[0] and x[1] == pair_binary[1]:
                        found_binary = True

        if found_forward:
            print('\t found forward', pair_forward, found_rev)
        else:
            print('\t ****** did not find forward', pair_forward, found_rev)

        if found_reverse:
            print('\t found reverse', pair_reverse, found_rev)
        else:
            print('\t ****** did not find reverse', pair_reverse, found_rev)

        if found_binary:
            print('\t found binary', pair_binary, found_rev)
        else:
            print('\t ****** did not find binary', pair_binary, found_rev)

    print('all done')

    print(lex_data)

    for i in lex_data:
        print(i, int_to_bin_array(i))

    mypairs = [[25, 22], [17, 28], [28, 26], [26, 25], [21, 25], [7, 24]]

    for p in mypairs:
        print(p, check_order(p[0], p[1]))


def check_gap(id_list,dim):
    max_gap = 0
    for id in id_list:
        data = flippable.data_from_id(id)
        #print(data)
        gap = flippable.get_largest_gap(data, dim)
        max_gap = max(max_gap, gap)
        #print(gap, id)

    print('max gap=', max_gap)

#############

conn = mysql.connector.connect(host='localhost',database='mysql',user='root',password='50Fl**rs')
cur = conn.cursor(buffered=True)


#lex_half_data = [31,30,29,27,23,15,28,26,22,14,25,21,13,19,11,7]
lex_half_data = [31,30,29,27,23,15,28,26,25,22,21,19,14,13,11,7]
lex_data = prefutils.data_from_top_half(lex_half_data)
lex_id = prefutils.data_to_id(lex_data)

dim = 6

query = "SELECT id FROM Pref_Six"

id_list = []

cur.execute(query)

for (id,) in cur:
    id_list.append(id)

#check(id_list)

#check_gap(id_list, dim)
