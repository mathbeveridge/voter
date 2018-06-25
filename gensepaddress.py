import mysql.connector
import datetime

import flippable
import prefutils
import addresspref

# A variation of gensepbatch that uses addresses instead of ids.
# This will be useful for the Amazon Web Services version, which will
# not use a database. It will keep the constructed CSP in memory, so
# we need an efficient way to represent them. We use an address,
# which is the idnum for the n CSPs of order n-1 you obtain by deleting a
# column, along with a 0/1 as to whether the middle is flipped.

idx_get_unprocessed_query = 0
idx_update_pref_query = 1
idx_update_processed_query = 2
idx_unprocessed_count_query = 3



query_list_5 = [
    "SELECT id, csp1, csp2, csp3, csp4, csp5, flip FROM Pref_Five_Address WHERE processed = False LIMIT 100",  # get unprocessed query
    "INSERT IGNORE INTO Pref_Five_Address (csp1, csp2, csp3, csp4, csp5, flip, processed) VALUES (%s,%s,%s,%s,%s,%s,%s)", # update pref query
    "UPDATE Pref_Five_Address SET processed=%s WHERE id=%s", # update processed query
    "SELECT COUNT(*) FROM Pref_Five_Address WHERE processed = False",  # get unprocessed count query
    ]

query_list_6 = [
    "SELECT id, csp1, csp2, csp3, csp4, csp5, csp6, flip FROM Pref_Six_Address WHERE processed = False LIMIT 5000",  # get unprocessed query
    "INSERT IGNORE INTO Pref_Six_Address (csp1, csp2, csp3, csp4, csp5, csp6, flip, processed) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", # update pref query
    "UPDATE Pref_Six_Address SET processed=%s WHERE id=%s", # update processed query
    "SELECT COUNT(*) FROM Pref_Six_Address WHERE processed = False",  # get unprocessed count query
    ]


############################################
#
# Database Implementation
#

# add the newly discovered CSPs to the table
def add_to_frontier_db(new_pref_addr_list):
    update_query = query_list[idx_update_pref_query]

    param_list = [ x + (False,) for x in new_pref_addr_list]

    cur.executemany(update_query, param_list)
    conn.commit()

# mark the processed CSPs
def move_to_visited_db(id_list):
    param = [ (True, id) for id in id_list]
    processed_query = query_list[idx_update_processed_query]
    cur.executemany(processed_query, param)
    conn.commit()

def log_frontier_size_db():
    cur.execute(count_query)

    print(str(datetime.datetime.now()), '\tnum unprocessed=', cur.fetchone())


def get_frontier_db():
    pref_line_list = []

    print(query)
    cur.execute(query)

    #### xxxab this line depends on the dimension. update!
    for (id, csp1, csp2, csp3, csp4, csp5, flip) in cur:
        pref_line_list.append([id, (csp1, csp2, csp3, csp4, csp5, flip)])

#    for (id, csp1, csp2, csp3, csp4, csp5, csp6, flip) in cur:
#        pref_line_list.append([id, (csp1, csp2, csp3, csp4, csp5, csp6, flip)])

    return pref_line_list

############################################


### In memory implementation
def log_frontier_size_naive():
    print(str(datetime.datetime.now()), '\tfrontier size=', len(stuff) - frontier_start)

def get_frontier_naive():
    global frontier_start
    ret_val = [(i,f) for i,f in enumerate(stuff[frontier_start:])]
    frontier_start = len(stuff)
    return ret_val

def add_to_frontier_naive(new_pref_addr_list):
    global stuff
    stuff = stuff + new_pref_addr_list


def move_to_visited_naive(id_list):
    # no op for now
    print("no op", len(stuff))



#####
#
# Wrapper methods for data access
#

# log the current frontier size
def log_frontier_size():
    log_frontier_size_db()

# returns a list of the form (id, address) where
# address = (id_1, .... , id_n, 0/1)
def get_frontier():
    return get_frontier_db()


# add newly discovered CSPs to the frontier
# input: a list of addresses to add to the frontier
def add_to_frontier(new_pref_addr_list):
    add_to_frontier_db(new_pref_addr_list)

#move from frontier to visited
# input: a list of ids to move from the frontier to visited
def move_to_visited(id_list):
    move_to_visited_db(id_list)

######################################
dim = 5

### DB specific initialization code
query_list = query_list_5

conn = mysql.connector.connect(host='localhost', database='mysql', user='root', password='50Fl**rs')
cur = conn.cursor(buffered=True)


count_query = (query_list[idx_unprocessed_count_query])
query = (query_list[idx_get_unprocessed_query])
### end DB code

### in memory initialization code

stuff = [ (1,(3,3,3,3,3,1,0)) ]
frontier_start = 0

###

has_frontier = True

while has_frontier:

    log_frontier_size()

    new_pref_address_list = []
    processed_id_list = []

    pref_line_list = get_frontier()


    has_frontier = len(pref_line_list) > 0
    # has_frontier = False

    for pref_line in pref_line_list:
        top_data = addresspref.regenerate_top_data(pref_line[1], dim)

        data = prefutils.data_from_top_half(top_data)

        flippable_pairs = flippable.get_flippable_pairs(data, dim)

        flipped_data = [flippable.flip(data, flip_pair, dim) for flip_pair in flippable_pairs]

        for pair, f in zip(flippable_pairs, flipped_data):

            flip_address = addresspref.generate_address(f,dim)
            #print(flip_address)
            new_pref_address_list.append(flip_address)

        processed_id_list.append(pref_line[0])

    # print("updating for prefs ", len(new_pref_list))
    add_to_frontier(new_pref_address_list)
    move_to_visited(processed_id_list)

cur.close()
conn.close()

