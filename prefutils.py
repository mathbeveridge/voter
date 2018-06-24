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

def data_to_str(data):
    return '-'.join(str(x) for x in data)

def data_from_str(data_str):
    return [ int(x) for x in data_str.split('-')]


# only use first half for the id to make it smaller
def halfdata_to_id(half_data):
    return '-'.join(str(x) for x in half_data)

# only use first half for the id to make it smaller
def data_to_id(data):
    half = len(data)//2
    return '-'.join(str(x) for x in data[:half])

# recover full id from the first half
def data_from_id(id):
    list1 = [ int(x) for x in id.split('-')]
    return data_from_top_half(list1)

# recover full id from the first half
def data_from_top_half(list1):
    d = 2 * len(list1)-1
    top = [x for x in list1]
    bottom = [d - x for x in reversed(top)]
    return top + bottom

# get id as a tuple of ints of length 2**(dim-1)
def tuple_from_id(id):
    return tuple([int(x) for x in id.split('-')])

def tuple_from_data(data):
    half = len(data)//2
    return tuple(data[:half])

######

def bin_array_to_decimal(bin_array):
    return sum(x * 2**i for i,x in enumerate(reversed(bin_array)))



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

        cur.execute('SELECT csp1, csp2, csp3, csp4, csp5, csp6, flip FROM Pref_Six_Address ORDER BY id' )

        id_list = []

        for x in cur:
            id_list.append(addresspref.regenerate(x, dim))

        #for (id,) in cur:
        #    id_list.append(id)
    else:
        print('dimension not supported', dim)

    return id_list


def get_id_tuple_list(dim):
    id_list = get_id_list(dim)
    #print(len(id_list))
    return [ tuple_from_id(x) for x in id_list ]
