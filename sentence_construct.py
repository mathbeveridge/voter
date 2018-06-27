import itertools


A = 'A'
B = 'B'


def is_compatible(word, triple, type):

    if type == A:
        for i in range(triple[0]+1):
            for j in range(i+1,triple[1]+1):
                if word[( i,j, triple[2])] < 0 :
                    return False

    if type == B:
        for i in range(triple[1]+1,triple[2]+1):
            if word[(triple[0], triple[1], i)] > 0:
                return False

    return True


def set_triple(word, triple, type):
    word_copy = word.copy()

    if type == A:
        for i in range(triple[0]+1):
            for j in range(i+1,triple[1]+1):
                if word[( i,j, triple[2])] < 0 :
                    raise TypeError('incompatible', triple, type, word)
                word_copy[( i,j, triple[2])] = 1

    if type == B:
        for i in range(triple[1]+1,triple[2]+1):
            if word[(triple[0], triple[1], i)] > 0:
                raise TypeError('incompatible', triple, type, word)
            word_copy[(triple[0], triple[1], i)] = -1

    return word_copy



def build_words(partial_word):
    words = []
    #word_count = 0
    idx_list = []

    #print('building', partial_word)

    for s in set_list:
        if partial_word[s] == 0:
            idx_list.append(s)
            break

    #print('\t', idx_list)

    if len(idx_list) == 0:
        #print('completed', write_word(partial_word))
        #word_count = 1
        words.append(write_word(partial_word))
    else:
        s = idx_list[0]

        if is_compatible(partial_word, s, A):
            words = words + build_words(set_triple(partial_word, s, A))
            #word_count = word_count + build_words(set_triple(partial_word, s, A))
        if is_compatible(partial_word, s, B):
            words = words + build_words(set_triple(partial_word, s, B))
            #word_count = word_count + build_words(set_triple(partial_word, s, B))

    return words
    #return word_count


def write_word(word):
    letters = []
    for s in set_list:
        if word[s] == 1:
            letters.append(A)
        else:
            letters.append(B)

    return ''.join(letters)

#############
dim = 6

# I have reversed the roles of the numbers in my checks. So the subset enumeration is off.
# Come back to this hack fix and make it work for all n.

set_list1 = list(itertools.combinations(range(dim), 3))

set_list = [ (5 - x[2], 5-x[1], 5-x[0]) for x in set_list1]

#set_list = [(4,3,2),(4,3,1),(4,3,0),(4,2,1),(4,2,0),(4,1,0),(3,2,1),(3,2,0),(3,1,0),(2,1,0)]

#set_list = [(2,3,4),(1,3,4),(0,3,4),(1,2,4),(0,2,4),(0,1,4),(1,2,3),(0,2,3),(0,1,3),(0,1,2)]

print(set_list)

my_word = {}

for s in set_list:
    print(s)
    my_word[s] = 0

foo = build_words(my_word)

#print(foo)

for f in foo:
    print(f)

print('xxxxxxxxxxxxxxxxxxxxxx')

print(len(foo))
print(len(set(foo)))


csp_words = []

with open('/Users/abeverid/PycharmProjects/voter/data/n6sep-shortname.csv', 'r') as f:
    for line in f.readlines():
        data = line.split(',')
        data.pop(0)
        data.pop(-1)

        csp_words.append(''.join(data))

print('short name len', len(csp_words))

bad_words = []

for w in foo:
    if not w in csp_words:
        bad_words.append(w)
#    else:
#        print('found word', w)

print('bad words', len(bad_words))
for b in bad_words:
    print(b)


