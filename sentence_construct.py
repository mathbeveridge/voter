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
dim = 4

set_list = list(itertools.combinations(range(dim), 3))

my_word = {}

for s in set_list:
    my_word[s] = 0

foo = build_words(my_word)

#print(foo)

for f in foo:
    print(f)

print(len(foo))
print(len(set(foo)))


