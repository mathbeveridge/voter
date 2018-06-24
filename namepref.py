import mysql.connector
import numpy as np
import flippable
import checkflip

import prefutils


name_dic3 = {'7-6-5-4': 'A', '7-6-5-3': 'B'}

# named according to the flip graph
# name_dic4 = {'15-14-13-12-11-10-7-6': 'AAAB2',
#              '15-14-13-12-11-10-7-9': 'AAAB1',
#              '15-14-13-12-11-10-9-7': 'AAAA1',
#              '15-14-13-12-11-10-9-8': 'AAAA2',
#              '15-14-13-12-11-7-10-6': 'AABB2',
#              '15-14-13-12-11-7-10-9': 'AABB1',
#              '15-14-13-11-12-10-7-6': 'BAAB2',
#              '15-14-13-11-12-10-7-9': 'BAAB1',
#              '15-14-13-11-12-10-9-7': 'BAAA1',
#              '15-14-13-11-12-10-9-8': 'BAAA2',
#              '15-14-13-11-12-7-10-9': 'BABB1',
#              '15-14-13-11-12-7-10-6': 'BABB2',
#              '15-14-13-11-7-12-10-9': 'BBBB1',
#              '15-14-13-11-7-12-10-6': 'BBBB2',
#              }

# named according to the central element
# name_dic4 = {'15-14-13-12-11-10-7-6': 'AAAB+6',
#              '15-14-13-12-11-10-7-9': 'AAAB+9',
#              '15-14-13-12-11-10-9-7': 'AAAA+7',
#              '15-14-13-12-11-10-9-8': 'AAAA+8',
#              '15-14-13-12-11-7-10-6': 'AABB+6',
#              '15-14-13-12-11-7-10-9': 'AABB+9',
#              '15-14-13-11-12-10-7-6': 'BAAB+6',
#              '15-14-13-11-12-10-7-9': 'BAAB+9',
#              '15-14-13-11-12-10-9-7': 'BAAA+7',
#              '15-14-13-11-12-10-9-8': 'BAAA+8',
#              '15-14-13-11-12-7-10-9': 'BABB+9',
#              '15-14-13-11-12-7-10-6': 'BABB+6',
#              '15-14-13-11-7-12-10-9': 'BBBB+9',
#              '15-14-13-11-7-12-10-6': 'BBBB+6',
#              }


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

def name_for_id(id):
    return name_dic[id]





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


dim=5

conn = mysql.connector.connect(host='localhost', database='mysql', user='root', password='50Fl**rs')

cur = conn.cursor(buffered=True)

name_dic = name_dic4

# populate the name_dic
#name_dic = {}
#cur.execute('SELECT id, name from Pref_Five')

#for (id, name) in cur:
#    name_dic[id] = name


keep_running = True

while (keep_running):

    #cur.execute('SELECT id FROM Pref_Six WHERE name IS NULL LIMIT 5000')
    cur.execute('SELECT id FROM Pref_Five')

    id_list = []

    name_list = []

    for (id,) in cur:
        id_list.append(id)

    keep_running = len(id_list) > 0
#    keep_running = False

    if (keep_running):
        print('processed starting with', id_list[0])

    for id in id_list:
        data = flippable.data_from_id(id)

        #data = flippable.data_from_top_half(id)
        data_bin = prefutils.data_to_bin_array(data, dim)

        #print('++++++++++++ handling id', id)

        #print('\t', data_bin)

        parent_list = []

        for idx in range(0,dim):
            #print('\t handling idx', idx)

            mask_row_idx_list = []
            for i,d in enumerate(data_bin):
                if d[idx] == 0:
                    mask_row_idx_list.append(i)

            data_array = np.array(data_bin)

            m = np.zeros_like(data_array)

            m[mask_row_idx_list,:] = 1

            #print(data_array)

            masked_array1 = np.ma.masked_array(data_array,m)
            c_array1 = np.ma.compress_rows(masked_array1)

            #print('=====',c_array1)

            m2 = np.zeros_like(c_array1)
            #print('m2', m2)
            m2[:,idx] = 1

            #print('m2', m2)

            ma2 = np.ma.masked_array(c_array1, m2)
            ca2 = np.ma.compress_cols(ma2)

            #print(ca2)

            parent_data = [ checkflip.bin_array_to_decimal(x) for x in ca2]

            #print('\t\t', parent_data)

            parent_list.append((parent_data))

        #print(parent_list)

        name_array = [ name_for_id(flippable.data_to_id(p)) for p in parent_list ]
#        name = '-'.join(name_array) + "+" +  str(data[2**(dim-1) -1])
        if data[2**(dim-1) -1] < 2**(dim-1):
            end = '-'
        else:
            end = '+'

        name = '(' + ''.join(name_array) + ')' + end
        name_list.append(name)

        print(name)


    #for id, name in zip(id_list, name_list):
    #    print(id, name)

    #print(name_list)
    print(len(name_list))
    print(len(list(set(name_list))))

    #print('adding to DB')

    param_list = [(name, id) for name, id in zip(name_list, id_list)]

    #cur.executemany('UPDATE Pref_Five SET name=%s WHERE id=%s', param_list)
    #cur.executemany('UPDATE Pref_Six SET name=%s WHERE id=%s', param_list)


    #conn.commit()




cur.close()

#    for p in param_list:
#        print(p)
