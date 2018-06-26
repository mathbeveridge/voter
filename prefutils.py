import mysql.connector


# helper functions for dealing with CSPs


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

bin_to_dec_dict = {}
dec_to_bin_dict = {}

# Converts [3,2,1,0] to '3-2-1-0'
def data_to_str(data):
    return '-'.join(str(x) for x in data)

# Converts '3-2-1-0' to [3,2,1,0]
def data_from_str(data_str):
    return [ int(x) for x in data_str.split('-')]


# only use first half for the id to make it smaller
# Converts [3,2] to '3-2'
def halfdata_to_id(half_data):
    return '-'.join(str(x) for x in half_data)

# only use first half for the id to make it smaller
# Converts [3,2,1,0] to '3-2'
def data_to_id(data):
    half = len(data)//2
    return '-'.join(str(x) for x in data[:half])

# recover full id from the first half
# Converts '3-2' to [3,2,1,0]
def data_from_id(id):
    list1 = [ int(x) for x in id.split('-')]
    return data_from_top_half(list1)

# recover full id from the first half
# Converts [3,2] to [3,2,1,0]
def data_from_top_half(list1):
    d = 2 * len(list1)-1
    top = [x for x in list1]
    bottom = [d - x for x in reversed(top)]
    return top + bottom

# get id as a tuple of ints of length 2**(dim-1)
# converts '3-2' to (3,2)
def tuple_from_id(id):
    return tuple([int(x) for x in id.split('-')])

# converts [3,2,1,0] to (3,2)
def tuple_from_data(data):
    half = len(data)//2
    return tuple(data[:half])

# xxxab change this to a tuple instead of an array
# and store the values: why recreate every time? just look it up

# Converts a binary array to a decimal
# Converts [1,0] to 2
# Converts [0,1] to 1
# Converts [1,1] to 3
# Converts [1,0,1,0] to 8 + 2 = 10
def bin_array_to_decimal(bin_array):
    return bin_tuple_to_decimal(tuple(bin_array))
#    return sum(x * 2**i for i,x in enumerate(reversed(bin_array)))

def bin_tuple_to_decimal(bin_tuple):
    if not bin_tuple in bin_to_dec_dict:
        bin_to_dec_dict[bin_tuple] =  sum(x * 2**i for i,x in enumerate(reversed(bin_tuple)))

    return bin_to_dec_dict[bin_tuple]

# converts decimal to binary array padded with leading zeros
# decimal_to_bin_array(3, 4) returns [0,0,1,1]
def decimal_to_bin_array(decimal, dim):
    key = (decimal, dim)

    if not key in dec_to_bin_dict:
        print('adding key', key)
        dec_to_bin_dict[key] = decimal_to_bin_array_impl(decimal, dim)

    return dec_to_bin_dict[key]

def decimal_to_bin_array_impl(decimal, dim):
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


# converts list of data to a binary array (padded with leading zeros)
# data_to_bin_array([3,1,2,0], 4) returns [[0,0,1,1], [0,0,0,1], [0,0,1,0], [0,0,0,0]]
def data_to_bin_array(data, dim):
    return [decimal_to_bin_array(x, dim) for x in data]

# Converts the top half of a binary array into the full data
# Converts [[1,1], [0,1]] to [3,1,2,0]
def data_from_half_bin_array(bin_array):
    top = [ bin_array_to_decimal(x) for x in bin_array]
    return data_from_top_half(top)


####### get ids from the database
def get_id_list(dim):
    id_list = []

    if dim == 4:
        id_list = list(name_dic4.keys())
    elif dim == 5:
        conn = mysql.connector.connect(host='localhost', database='mysql', user='root', password='50Fl**rs')

        cur = conn.cursor(buffered=True)

        cur.execute('SELECT id FROM Pref_Five')

        id_list = []

        for (id,) in cur:
            id_list.append(id)


    elif dim == 6:
        conn = mysql.connector.connect(host='localhost', database='mysql', user='root', password='50Fl**rs')

        cur = conn.cursor(buffered=True)

#        cur.execute('SELECT csp1, csp2, csp3, csp4, csp5, csp6, flip FROM Pref_Six_Address ORDER BY id' )
        cur.execute('SELECT id FROM Pref_Six' )


        id_list = []

#        for x in cur:
#            id_list.append(addresspref.regenerate_id(x, dim))

        for (id,) in cur:
            id_list.append(id)
    else:
        print('dimension not supported', dim)

    return id_list

# gets the ids as tuples instead of arrays
# this could improve performance
def get_id_tuple_list(dim):
    id_list = get_id_list(dim)
    #print(len(id_list))
    return [ tuple_from_id(x) for x in id_list ]



####### get names from the database
def get_name_list(dim):
    conn = mysql.connector.connect(host='localhost', database='mysql', user='root', password='50Fl**rs')

    cur = conn.cursor(buffered=True)

    cur.execute('SELECT name FROM Pref_Six')

    name_list = []

    #        for x in cur:
    #            id_list.append(addresspref.regenerate_id(x, dim))

    for (name,) in cur:
        name_list.append(name)

    return name_list
