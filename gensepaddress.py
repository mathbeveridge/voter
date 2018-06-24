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
#idx_pref_exists_query = 1
#idx_flip_exists_query = 2
idx_update_pref_query = 1
#idx_update_flip_query = 4
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



def update_pref_table(new_pref_addr_list):
    update_query = query_list[idx_update_pref_query]

    param_list = [ x + (False,) for x in new_pref_addr_list]

    #print('query', update_query)
    #print('param', param_list)

    cur.executemany(update_query, param_list)
    conn.commit()


def mark_processed(id_list):
    param = [ (True, id) for id in id_list]
    processed_query = query_list[idx_update_processed_query]
    cur.executemany(processed_query, param)
    conn.commit()



dim = 6
query_list = query_list_6

conn = mysql.connector.connect(host='localhost', database='mysql', user='root', password='50Fl**rs')

cur = conn.cursor(buffered=True)

# query = ("SELECT id FROM Pref_Six WHERE processed = False")

count_query = (query_list[idx_unprocessed_count_query])

query = (query_list[idx_get_unprocessed_query])
print(query)

has_unprocessed = True
idx = 1

while has_unprocessed:

    new_pref_address_list = []
    processed_id_list = []

    cur.execute(count_query)

    print(str(datetime.datetime.now()), '\tnum unprocessed=', cur.fetchone())

    idx = idx + 1

    cur.execute(query)

    pref_line_list = []

#### xxxab this line depends on the dimension. update!
    for (id, csp1, csp2, csp3, csp4, csp5, csp6, flip) in cur:
        pref_line_list.append([id, (csp1, csp2, csp3, csp4, csp5, csp6, flip)])

    has_unprocessed = len(pref_line_list) > 0
    # has_unprocessed = False

    for pref_line in pref_line_list:
        top_data = addresspref.regenerate_top_data(pref_line[1], dim)
#        data = prefutils.data_from_half_bin_array(top_data)

        data = prefutils.data_from_top_half(top_data)

        flippable_pairs = flippable.get_flippable_pairs(data, dim)

        flipped_data = [flippable.flip(data, flip_pair, dim) for flip_pair in flippable_pairs]

        for pair, f in zip(flippable_pairs, flipped_data):

            flip_address = addresspref.generate_address(f,dim)
            #print(flip_address)
            new_pref_address_list.append(flip_address)

        processed_id_list.append(pref_line[0])

    # print("updating for prefs ", len(new_pref_list))
    update_pref_table(new_pref_address_list)
    mark_processed(processed_id_list)

cur.close()
conn.close()

