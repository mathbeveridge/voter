import mysql.connector
import numpy as np

import prefutils

## an address for a CSP of order n is a list of n+1 numbers. The first
## n are id numbers, corresponding to the n-1 dimensional CSPs
## obtained by fixing the outcome on a singleton. The last number is 0 or 1
## depending on whether the central pair is flipped.
##
## This is the most efficient way that I can think of to represent a CSP

#def name_for_id(id):
#    return name_dic[id]

### returns an int corresponding to the tuple.
### I think that the tuple is a more efficient storage mechanism than
### the string id
def idnum_for_tuple(tuple, dim):
    if dim in id_tuple_dict:
        id_list = id_tuple_dict[dim]
        return id_list.index(tuple)
    else:
        raise ValueError('id_tuple_dict not initialized for', dim)

def update_tuple_list(tuple_list, dim):
    print('********* updating', dim, tuple_list)
    id_tuple_dict[dim] = tuple_list

def idnum_for_tuple_old(tuple, dim):
    # print('tuple', tuple)
    if dim == 4:
        return name_dic4a[tuple]
    elif dim == 5:
        # auto increment starts at 1
        return id_tuple_list5.index(tuple) + 1
    else:
        raise ValueError('id_tuple_dict not initialized for', dim)


### the address is an integer that tells you where to find the tuple
### representation for the CSP. the address for dim+1 is a list of these
### integer addresses
###
### xxxab I need to change this name. location? index? pk? cspid?
def get_tuple_for_address(address, dim):
    if dim in id_tuple_dict:
        id_list = id_tuple_dict[dim]
        #print('address', address, 'id_list', id_list[address])
        return id_list[address]
    else:
        raise ValueError('dimension not supported', dim)


def get_tuple_for_address_old(address, dim):
    if dim == 4:
        return sep4[address]
    if dim == 5:
        #auto increment starts at 1 not 0
        return id_tuple_list5[address-1]
    else:
        raise ValueError('dimension not supported', dim)


### converts the top half to binary
### and stores it in a dictionary
def get_csp_bin_from_top(top_tuple, dim):
    #top = [t for t in top_tuple]

    if top_tuple in csp_bin_dict:
        bin_data = csp_bin_dict[top_tuple]
    else:
        data = prefutils.data_from_top_half(top_tuple)
        bin_data = prefutils.data_to_bin_array(data, dim-1)

        csp_bin_dict[top_tuple] = bin_data

    return bin_data

# gets the csp bin for the address
def get_csp_bin_for_address(address, dim):

    csp_list = []

    for i in range(len(address) - 1):
        csp_list.append(get_tuple_for_address(address[i], dim - 1))

    #print('\tcsp_list',csp_list)

    csp_bin_list = [get_csp_bin_from_top(x, dim) for x in csp_list]

    return csp_bin_list

# takes binary data and turns it into an address, which is a list of size n+1
# the first n entries are the ids of the CSP you get by deleting the ith column
# the final entry is either 1 or 0, depending on whether there is a central flip
def generate_address(data, dim):

    parent_list = []

    data_bin = prefutils.data_to_bin_array(data, dim)

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


        parent_data = [prefutils.bin_array_to_decimal(x) for x in ca2]

        parent_list.append((parent_data))


    # print(parent_list)

    address = [idnum_for_tuple(prefutils.tuple_from_data(p), dim-1) for p in parent_list]

    if data[2 ** (dim - 1) - 1] < 2 ** (dim - 1):
        address.append(0)
    else:
        address.append(1)

    return tuple(address)


def regenerate_id(address, dim):
    return prefutils.halfdata_to_id(regenerate_top_data(address, dim))

# recreates the top data from the address
def regenerate_top_data(address, dim):

    #print('regenerate', address)

    csp_bin_list = get_csp_bin_for_address(address, dim)

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

    regen_data = [prefutils.bin_array_to_decimal(x) for x in working_csp]

    return regen_data



def line_passes(line, csp_bin_list, idx_list):

    passes = True

    for i,x in enumerate(line):
        if x == 1:
            temp_line = [y for y in line]
            temp_line.pop(i)

            if not temp_line == csp_bin_list[i][idx_list[i]]:
                #print(line, temp_line, 'fails', i, csp_bin_list[i][idx_list[i]])
                passes = False
                break

    return passes


name_dic4 = {'15-14-13-12-11-10-7-6': 'AAAB-',
             '15-14-13-12-11-10-7-9': 'AAAB+',
             '15-14-13-12-11-10-9-7': 'AAAA-',
             '15-14-13-12-11-10-9-8': 'AAAA+',
             '15-14-13-12-11-7-10-6': 'AABB-',
             '15-14-13-12-11-7-10-9': 'AABB+',
             '15-14-13-11-12-10-7-6': 'BAAB-',
             '15-14-13-11-12-10-7-9': 'BAAB+',
             '15-14-13-11-12-10-9-7': 'BAAA-',
             '15-14-13-11-12-10-9-8': 'BAAA+',
             '15-14-13-11-12-7-10-9': 'BABB+',
             '15-14-13-11-12-7-10-6': 'BABB-',
             '15-14-13-11-7-12-10-9': 'BBBB+',
             '15-14-13-11-7-12-10-6': 'BBBB-',
             }



#######

sep4 = (
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

name_dic4a = {
    (15, 14, 13, 12, 11, 10, 7, 6): 0,
    (15, 14, 13, 12, 11, 10, 7, 9): 1,

    (15, 14, 13, 12, 11, 10, 9, 7): 2,
    (15, 14, 13, 12, 11, 10, 9, 8): 3,

    (15, 14, 13, 12, 11, 7, 10, 6): 4,
    (15, 14, 13, 12, 11, 7, 10, 9): 5,


    (15, 14, 13, 11, 12, 10, 7, 6): 6,
    (15, 14, 13, 11, 12, 10, 7, 9): 7,

    (15, 14, 13, 11, 12, 10, 9, 7): 8,
    (15, 14, 13, 11, 12, 10, 9, 8): 9,

    (15, 14, 13, 11, 12, 7, 10, 9): 10,
    (15, 14, 13, 11, 12, 7, 10, 6): 11,

    (15, 14, 13, 11, 7, 12, 10, 9): 12,
    (15, 14, 13, 11, 7, 12, 10, 6): 13,
}





####### get ids from the database
def get_id_list(dim):
    id_list = []

    if dim == 4:
        id_list = list(name_dic4.keys())
    elif dim == 5:
        # conn = mysql.connector.connect(host='localhost', database='mysql', user='root', password='50Fl**rs')
        #
        # cur = conn.cursor(buffered=True)
        #
        # cur.execute('SELECT id FROM Pref_Five')
        #
        # id_list = []
        #
        # for (id,) in cur:
        #     id_list.append(id)

        # must ensure that we have the right order

        conn = mysql.connector.connect(host='localhost', database='mysql', user='root', password='50Fl**rs')

        cur = conn.cursor(buffered=True)

        cur.execute('SELECT csp1, csp2, csp3, csp4, csp5, flip FROM Pref_Five_Address ORDER BY id' )

        id_list = []

        for x in cur:
            id_list.append(regenerate_id(x, dim))
    elif dim == 6:
        conn = mysql.connector.connect(host='localhost', database='mysql', user='root', password='50Fl**rs')

        cur = conn.cursor(buffered=True)

        cur.execute('SELECT csp1, csp2, csp3, csp4, csp5, csp6, flip FROM Pref_Six_Address ORDER BY id' )

        id_list = []

        for x in cur:
            id_list.append(regenerate_id(x, dim))

        #for (id,) in cur:
        #    id_list.append(id)
    else:
        print('dimension not supported', dim)

    return id_list


def get_id_tuple_list(dim):
    id_list = get_id_list(dim)
    #print(len(id_list))
    return [ prefutils.tuple_from_id(x) for x in id_list ]


def run():
    dim = 4

    conn = mysql.connector.connect(host='localhost', database='mysql', user='root', password='50Fl**rs')

    cur = conn.cursor(buffered=True)

    #name_dic = name_dic4a

    # populate the name_dic
    # name_dic = {}
    # cur.execute('SELECT id, name from Pref_Five')

    # for (id, name) in cur:
    #    name_dic[id] = name


    keep_running = True

    while (keep_running):

        # cur.execute('SELECT id FROM Pref_Six WHERE name IS NULL LIMIT 5000')
        cur.execute('SELECT id FROM Pref_Five')

        id_list = []

        name_list = []

        for (id,) in cur:
            id_list.append(id)

            #    keep_running = len(id_list) > 0
        keep_running = False

        if (keep_running):
            print('processed starting with', id_list[0])

        for id in id_list:

            #    for id in [ id_list[0], id_list[1]]:

            data = prefutils.data_from_id(id)

            # print('++++++++++++ handling id', id)

            address = generate_address(data, dim)

            print(id, address)

            regen_id = regenerate_id(address, dim)

            # print(address, id)


            # print(data)

            #regen_data = [prefutils.bin_array_to_decimal(x) for x in regen_bin_data]

            #regen_id = prefutils.halfdata_to_id(regen_data)

            num_errors = 0

            if not regen_id == id:
                print('error id and regen_id dont match', id, regen_id)
                num_errors = num_errors + 1

            # for a,b in zip(data_bin, regen_bin_data):
            #    print(a,b)

            # print('name array', address)

            name = '(' + ','.join(str(x) for x in address) + ')'
            name_list.append(name)

        # for id, name in zip(id_list, name_list):
        #    print(id, name)

        # print(name_list)
        print(len(name_list))
        print(len(list(set(name_list))))

        print('num errors', num_errors)
        # print('adding to DB')

        param_list = [(name, id) for name, id in zip(name_list, id_list)]

        # cur.executemany('UPDATE Pref_Five SET name=%s WHERE id=%s', param_list)
        # cur.executemany('UPDATE Pref_Six SET name=%s WHERE id=%s', param_list)


        # conn.commit()

    cur.close()

    #    for p in param_list:
    #        print(p)


#######
#id_list5 = prefutils.get_id_list(5)


csp_bin_dict = {}

id_tuple_dict = {}
id_tuple_dict[4] = sep4


#### xxxab fix this: code moved from pref utils because import conflicts
#id_tuple_list5 = get_id_tuple_list(5)


