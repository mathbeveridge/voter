import mysql.connector
import flippable
import datetime

idx_get_unprocessed_query = 0
idx_pref_exists_query = 1
idx_flip_exists_query = 2
idx_update_pref_query = 3
idx_update_flip_query = 4
idx_update_processed_query = 5
idx_unprocessed_count_query = 6



query_list_5 = [
    "SELECT id FROM Pref_Five WHERE processed = False LIMIT 5000",  # get unprocessed query
    "SELECT COUNT(*) FROM Pref_Five WHERE id = %s", # pref exists query
    "SELECT COUNT(*) FROM Pref_Flip_Five WHERE (id1 = %s AND id2 = %s)", # flip exists query
    "INSERT IGNORE INTO Pref_Five (id, processed) VALUES (%s,%s)", # update pref query
    "INSERT IGNORE INTO Pref_Flip_Five (id1, id2, flip1, flip2) VALUES (%s,%s,%s,%s)", # update flip query
    "UPDATE Pref_Five SET processed=%s WHERE id=%s", # update processed query
    "SELECT COUNT(*) FROM Pref_Five WHERE processed = False",  # get unprocessed count query
    ]

query_list_6 = [
    "SELECT id FROM Pref_Six WHERE processed = False LIMIT 5000",  # get unprocessed query
    "SELECT COUNT(*) FROM Pref_Six WHERE id = %s", # pref exists query
    "SELECT COUNT(*) FROM Pref_Flip_Six WHERE (id1 = %s AND id2 = %s)", # flip exists query
    "INSERT IGNORE INTO Pref_Six (id, processed) VALUES (%s,%s)", # update pref query
    "INSERT IGNORE INTO Pref_Flip_Six (id1, id2, flip1, flip2) VALUES (%s,%s,%s,%s)", # update flip query
    "UPDATE Pref_Six SET processed=%s WHERE id=%s", # update processed query
    "SELECT COUNT(*) FROM Pref_Six WHERE processed = False",  # get unprocessed count query

    ]


query_list_7 = [
    "SELECT id FROM Pref_Seven WHERE processed = False LIMIT 5000",  # get unprocessed query
    "SELECT COUNT(*) FROM Pref_Seven WHERE id = %s", # pref exists query
    "SELECT COUNT(*) FROM Pref_Flip_Seven WHERE (id1 = %s AND id2 = %s)", # flip exists query
    "INSERT INTO Pref_Seven (id, processed) VALUES (%s,%s)", # update pref query
    "INSERT INTO Pref_Flip_Seven (id1, id2, flip1, flip2) VALUES (%s,%s,%s,%s)", # update flip query
    "UPDATE Pref_Seven SET processed=%s WHERE id=%s", # update processed query
    "SELECT COUNT(*) FROM Pref_Seven WHERE processed = False",  # get unprocessed count query

    ]



# def pref_exists(new_data):
#     ret_val = False
#
#     if pref_cache.get(new_data) is not None:
#         ret_val = True
#     else:
#         #pref_exists_query = "SELECT COUNT(*) FROM Pref_Six WHERE id = %s"
#         pref_exists_query = query_list[idx_pref_exists_query]
#         cur.execute(pref_exists_query, (new_data,))
#         result = cur.fetchone()
#         if result[0] > 0:
#             ret_val = True
#             pref_cache.update((new_data, new_data))
#
#     return ret_val


# def pref_exists(new_data):
#     #pref_exists_query = "SELECT COUNT(*) FROM Pref_Six WHERE id = %s"
#     pref_exists_query = query_list[idx_pref_exists_query]
#     cur.execute(pref_exists_query, (new_data,))
#     result = cur.fetchone()
#     return result[0] > 0
#
#
# def pref_flip_exists(new_data, pair):
#     #print('\t\t', pair, new_data)
# #    pref_exists_query = "SELECT COUNT(*) FROM Pref_Flip_Five WHERE (id1 = %s OR id2 = %s) AND (flip1=%s AND flip2=%s)"
# #    cur.execute(pref_exists_query, (new_data,new_data,pair[0],pair[1],))
#     #flip_exists_query = "SELECT COUNT(*) FROM Pref_Flip_Six WHERE (id1 = %s OR id2 = %s)"
#     flip_exists_query = query_list[idx_flip_exists_query]
#     cur.execute(flip_exists_query, (new_data,new_data))
#     result = cur.fetchone()
#     return result[0] > 0


def update_pref_table(new_data_list):
    update_query = query_list[idx_update_pref_query]

    param_list = [ (x, False) for x in new_data_list]

    #print(param_list)

    cur.executemany(update_query, param_list)
    conn.commit()
    #else:
    #    print("\t data exists")


def update_flip_table(flip_list):
 #    update_query = "BEGIN IF NOT EXISTS (SELECT * FROM Pref_Five WHERE id = %s BEGIN INSERT INTO Pref_Five (id, processed) VALUES (%s,%s) END END"
     #update_flip_query = "INSERT INTO Pref_Flip_Six (id1, id2, flip1, flip2) VALUES (%s,%s,%s,%s)"

    update_flip_query = query_list[idx_update_flip_query]

    cur.executemany(update_flip_query, flip_list)
    conn.commit()



def mark_processed(id_list):
    #processed_query = "UPDATE Pref_Six SET processed=true WHERE id=%s"
    param = [ (True, id) for id in id_list]
    #print('param is', param)
    processed_query = query_list[idx_update_processed_query]
    cur.executemany(processed_query, param)
    conn.commit()

def format_flip(id1, id2, p1, p2):

    # for now, list edge going towards reverse lex
    if check_bin_order(p1, p2):
        ids = [ id1, id2]
        p = [ p1, p2]
    else:
        ids = [id2, id1]
        p = [p2,p1]

    print('flipping pair', p, ids, 'from', p1, p2)

    #ids.sort()
    #p.sort()

    return ids + p




def int_to_bin_array(x):
    return [int(z) for z in bin(x)[2:]]

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

    if sum(x_bin) == sum(y_bin):
        ret_val =  x < y

        # THIS IS FLAWED
        #print(x,y,'sums are equal')
#        diff = [a - b for a, b in zip(x_bin, y_bin)]
#        diff.reverse()
        #print('\t',diff)
#        idx = next((i for i, j in enumerate(diff) if not j == 0), None)  # j!= 0 for strict match
        #print('\t', idx)
#        ret_val =  diff[idx] > 0
    else:
        ret_val =  sum(x_bin) < sum(y_bin)

    print('######', x, y, x_bin, y_bin, ret_val)
    return ret_val


###########




dim = 5
query_list = query_list_5

conn = mysql.connector.connect(host='localhost', database='mysql', user='root', password='50Fl**rs')

cur = conn.cursor(buffered=True)

# query = ("SELECT id FROM Pref_Six WHERE processed = False")

count_query = (query_list[idx_unprocessed_count_query])

query = (query_list[idx_get_unprocessed_query])
print(query)

has_unprocessed = True
idx = 1

while has_unprocessed:

    new_pref_list = set()
    new_flip_list = []
    processed_id_list = set()

    cur.execute(count_query)

    print(str(datetime.datetime.now()), '\tnum unprocessed=', cur.fetchone())

    idx = idx + 1

    cur.execute(query)

    id_list = []
    for (id,) in cur:
        id_list.append(id)

    has_unprocessed = len(id_list) > 0
    # has_unprocessed = False

    for id in id_list:
        data = flippable.data_from_id(id)

        flippable_pairs = flippable.get_flippable_pairs(data, dim)

        flipped_data = [flippable.flip(data, flip_pair, dim) for flip_pair in flippable_pairs]

        edges = []

        for pair, f in zip(flippable_pairs, flipped_data):

            f_id = flippable.data_to_id(f)
            new_pref_list.add(f_id)
            new_flip_list.append(format_flip(id, f_id, pair[0], pair[1]))

        #        update_pref_table(f_str)
        #        update_flip_table([id, f_str], pair)
        # update_flip_table([id, f_id], pair)

        processed_id_list.add(id)

    # print("updating for prefs ", len(new_pref_list))
    update_pref_table(new_pref_list)
    update_flip_table(new_flip_list)
    mark_processed(processed_id_list)

cur.close()
conn.close()

