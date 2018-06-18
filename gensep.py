import mysql.connector
import flippable


idx_get_unprocessed_query = 0
idx_pref_exists_query = 1
idx_flip_exists_query = 2
idx_update_pref_query = 3
idx_update_flip_query = 4
idx_update_processed_query = 5
idx_unprocessed_count_query = 6


query_list_5 = [
    "SELECT id FROM Pref_Five WHERE processed = False",  # get unprocessed query
    "SELECT COUNT(*) FROM Pref_Five WHERE id = %s", # pref exists query
    "SELECT COUNT(*) FROM Pref_Flip_Five WHERE (id1 = %s AND id2 = %s)", # flip exists query
    "INSERT INTO Pref_Five (id, processed) VALUES (%s,%s)", # update pref query
    "INSERT INTO Pref_Flip_Five (id1, id2, flip1, flip2) VALUES (%s,%s,%s,%s)", # update flip query
    "UPDATE Pref_Five SET processed=true WHERE id=%s", # update processed query
    "SELECT COUNT(*) FROM Pref_Five WHERE processed = False",  # get unprocessed count query
    ]

query_list_6 = [
    "SELECT id FROM Pref_Six WHERE processed = False",  # get unprocessed query
    "SELECT COUNT(*) FROM Pref_Six WHERE id = %s", # pref exists query
    "SELECT COUNT(*) FROM Pref_Flip_Six WHERE (id1 = %s AND id2 = %s)", # flip exists query
    "INSERT INTO Pref_Six (id, processed) VALUES (%s,%s)", # update pref query
    "INSERT INTO Pref_Flip_Six (id1, id2, flip1, flip2) VALUES (%s,%s,%s,%s)", # update flip query
    "UPDATE Pref_Six SET processed=true WHERE id=%s", # update processed query
    "SELECT COUNT(*) FROM Pref_Six WHERE processed = False",  # get unprocessed count query

    ]


query_list_7 = [
    "SELECT id FROM Pref_Seven WHERE processed = False LIMIT 5000",  # get unprocessed query
    "SELECT COUNT(*) FROM Pref_Seven WHERE id = %s", # pref exists query
    "SELECT COUNT(*) FROM Pref_Flip_Seven WHERE (id1 = %s AND id2 = %s)", # flip exists query
    "INSERT INTO Pref_Seven (id, processed) VALUES (%s,%s)", # update pref query
    "INSERT INTO Pref_Flip_Seven (id1, id2, flip1, flip2) VALUES (%s,%s,%s,%s)", # update flip query
    "UPDATE Pref_Seven SET processed=true WHERE id=%s", # update processed query
    "SELECT COUNT(*) FROM Pref_Seven WHERE processed = False",  # get unprocessed count query

    ]



def pref_exists(new_data):
    #pref_exists_query = "SELECT COUNT(*) FROM Pref_Six WHERE id = %s"
    pref_exists_query = query_list[idx_pref_exists_query]
    cur.execute(pref_exists_query, (new_data,))
    result = cur.fetchone()
    return result[0] > 0

def pref_flip_exists(new_data, pair):
    #print('\t\t', pair, new_data)
#    pref_exists_query = "SELECT COUNT(*) FROM Pref_Flip_Five WHERE (id1 = %s OR id2 = %s) AND (flip1=%s AND flip2=%s)"
#    cur.execute(pref_exists_query, (new_data,new_data,pair[0],pair[1],))
    #flip_exists_query = "SELECT COUNT(*) FROM Pref_Flip_Six WHERE (id1 = %s OR id2 = %s)"
    flip_exists_query = query_list[idx_flip_exists_query]
    cur.execute(flip_exists_query, (new_data,new_data))
    result = cur.fetchone()
    return result[0] > 0


def update_pref_table(new_data):
    #update_query = "IF NOT EXISTS (SELECT * FROM Pref_Five WHERE id = %s) BEGIN INSERT INTO Pref_Five (id, processed) VALUES (%s,%s) END"
    #update_query = "INSERT INTO Pref_Six (id, processed) VALUES (%s,%s)"
    update_query = query_list[idx_update_pref_query]

    if not pref_exists(new_data):
        #print('inserting:', new_data)
        cur.execute(update_query, (new_data, False,))
        conn.commit()
    #else:
    #    print("\t data exists")


def update_flip_table(data, pair):
#    update_query = "BEGIN IF NOT EXISTS (SELECT * FROM Pref_Five WHERE id = %s BEGIN INSERT INTO Pref_Five (id, processed) VALUES (%s,%s) END END"
    #update_flip_query = "INSERT INTO Pref_Flip_Six (id1, id2, flip1, flip2) VALUES (%s,%s,%s,%s)"
    update_flip_query = query_list[idx_update_flip_query]

    data.sort()
    p = [pair[0], pair[1]]
    p.sort()

    #print("data",data)
    #print("pair", p)

    if not pref_flip_exists(data[0], p):
        cur.execute(update_flip_query, (data[0], data[1], p[0], p[1],))
        conn.commit()
    #else:
    #    print("\t flip exists")


def mark_processed(id):
    #processed_query = "UPDATE Pref_Six SET processed=true WHERE id=%s"
    processed_query = query_list[idx_update_processed_query]
    cur.execute(processed_query, (id,))
    conn.commit()






###########

dim=7
query_list = query_list_7

conn = mysql.connector.connect(host='localhost',database='mysql',user='root',password='50Fl**rs')
cur = conn.cursor(buffered=True)

#query = ("SELECT id FROM Pref_Six WHERE processed = False")

count_query = (query_list[idx_unprocessed_count_query])

query = (query_list[idx_get_unprocessed_query])
print(query)

has_unprocessed = True
idx = 1

while has_unprocessed:

    #print('===========trying it again', idx)

    cur.execute(count_query)

    print('\tnum unprocessed=', cur.fetchone())

    idx=idx+1

    cur.execute(query)

    id_list = []
    for (id,) in cur:
        id_list.append(id)

    has_unprocessed = len(id_list) > 0
    #has_unprocessed = False

    for id in id_list:
      #print("id={}".format(id))
      #print(flippable.data_from_str(id))

#      data = flippable.data_from_str(id)
      data = flippable.data_from_id(id)

      flippable_pairs = flippable.get_flippable_pairs(data, dim)

      flipped_data = [flippable.flip(data, flip_pair, dim) for flip_pair in flippable_pairs]

      edges = []

      for pair, f in zip(flippable_pairs,flipped_data):
        #print('\t', pair, f)

#        f_str = flippable.data_to_str(f)
        f_id = flippable.data_to_id(f)

#        update_pref_table(f_str)
#        update_flip_table([id, f_str], pair)
        update_pref_table(f_id)
        #update_flip_table([id, f_id], pair)

      mark_processed(id)

cur.close()
conn.close()


############

