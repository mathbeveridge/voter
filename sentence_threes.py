import itertools
import prefutils
import os
import mysql.connector


# Creates files containing id names that contain words corresponding to 3-sets
# to explore some ideas of Ian about efficient representation of CSPs.

def set_to_str(s):
    x = str(s)
    x = x.replace(',','')

    return x


########

dir_name = 'data/'
dim = 6

conn = mysql.connector.connect(host='localhost', database='mysql', user='root', password='50Fl**rs')

cur = conn.cursor(buffered=True)

cur.execute('SELECT id,name FROM Pref_Six')

pref_list = []

for (id, name) in cur:
    #print(id,name)
    pref_list.append((id,name))


pair_dict = {}
set_list = list(itertools.combinations(range(dim), 3))

# only care about the order of 100 and 011 to decide whether this 3-set
# corresponds to an A (in order) or a B (out of order)
for s in set_list:
    x = [0] * dim
    x[s[0]] = 1
    y = [0] * dim
    y[s[1]] = 1
    y[s[2]] = 1

    pair_dict[s] = (prefutils.bin_array_to_decimal(x),prefutils.bin_array_to_decimal(y))


type_list = []


for pref in pref_list:

    data = prefutils.data_from_id(pref[0])

    type = []

    for s in set_list:
        pair = pair_dict[s]
        if (data.index(pair[0]) > data.index(pair[1])):
            t = 'B'
        else:
            t = 'A'

        type.append(t)

    #print(type)
    type_list.append(type)



# output file
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

set_names = [set_to_str(s) for s in set_list]

#with open(dir_name + 'n' + str(dim) + "sep-named.csv", "w") as out_file:
    # header
#    out_file.write('id,name,' + ','.join(set_names) + '\n')

#    for pref,type in zip(pref_list,type_list):
#        out_file.write(','.join(pref) + ','  + ','.join(type) + '\n')

name_count = {}
out_dict = {}

for pref,type in zip(pref_list,type_list):
    temp_name = pref[1].replace(')','').replace('(','')
    temp_name = temp_name.replace('+',' ').replace('-',' ')

    #temp_type = ''.join(type)

    out_dict[temp_name] = type

    if temp_name in name_count:
        name_count[temp_name] = name_count[temp_name] + 1
    else:
        name_count[temp_name] = 1



print(len(out_dict))

#for name in name_count:
#    print(name, out_dict[name],name_count[name])

# this creates a file without the +/- and includes the count of names of that format
with open(dir_name + 'n' + str(dim) + "sep-shortname.csv", "w") as out_file:

    out_file.write('name,' + ','.join(set_names) + ',count\n')

    for name in name_count:
        out_file.write(name + ',' +  ','.join(out_dict[name]) + ','  + str(name_count[name]) + '\n')

