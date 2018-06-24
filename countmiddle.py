import mysql.connector
import prefutils


#
# Counts the number of middle entries with k ones.
# This creates a triangle of numbers to study.
# Note that the # of middle entries with exactly one 1 is
# equal to the number of CSPs of the previous size.
#


conn = mysql.connector.connect(host='localhost', database='mysql', user='root', password='50Fl**rs')

cur = conn.cursor(buffered=True)


dim = 5

#cur.execute('SELECT id FROM Pref_Six WHERE name IS NULL LIMIT 5000')
cur.execute('SELECT id FROM Pref_Five')

id_list = []

for (id,) in cur:
    id_list.append(id)

count = [0] * dim

middle_dic = {}


for id in id_list:
    data = prefutils.data_from_id(id)
    #print(data)
    middle_num = data[2**(dim-1)]
    middle_data = prefutils.decimal_to_bin_array(data[2**(dim-1)], dim)
    total = sum(middle_data)


    # debug: looking at middle entries with exactly 2 ones.
    # where do they appear?
    if total == 2:
        #print(prefutils.data_to_bin_array(data, dim))
        print(middle_data)
        if middle_num in middle_dic:
            middle_dic[middle_num] = middle_dic[middle_num]+1
        else:
            middle_dic[middle_num] = 1

    # how many middle entries have num 1's = total?
    count[total-1] = count[total-1] + 1


print(count)
print(middle_dic)