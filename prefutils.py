

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



def data_to_bin_array(data, dim):
    return [decimal_to_bin_array(x, dim) for x in data]
