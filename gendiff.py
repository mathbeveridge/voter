import mysql.connector

import flippable
import checkflip



####
#
# Generates the differences between adjacent separable preferences. We create a list
# where pref 2i-1 and 2i are adjacent. This can be fed into a mma file that figures out the
# vector that changes from one to the other
#
sep_dir = '/bean/mac/research/tran/n5sep/'
coef_dir = '/bean/mac/research/tran/n5sep-coef/'

edge_file_name = "n5edges.csv"

out_file_name = "n5coef-diff.csv"

file_names = [
    's3v1s4v1s5v1.csv',
    's3v1s4v1s5v5.csv',
    's3v1s4v2s5v1.csv',
    's3v1s4v1s5v10.csv',
    's3v1s4v1s5v6.csv',
    's3v1s4v2s5v2.csv',
    's3v1s4v1s5v2.csv',
    's3v1s4v1s5v7.csv',
    's3v1s4v2s5v3.csv',
    's3v1s4v1s5v3.csv',
    's3v1s4v1s5v8.csv',
    's3v1s4v2s5v4.csv',
    's3v1s4v1s5v4.csv',
    's3v1s4v1s5v9.csv'
]


def str_to_bin_array(mystr):
    mylist = list(mystr)
    return [ int(s) for s in mylist]

def str_to_decimal(str):
    new_str = str.strip()
    return checkflip.bin_array_to_decimal(str_to_bin_array(new_str))


########

def runFive():
    # create coefficient dictionary
    coef_dict = {}

    for file_name in file_names:
        sep_file = open(sep_dir + file_name, "r")
        sep_lines = sep_file.readlines()

        coef_file = open(coef_dir + file_name, "r")
        coef_lines = coef_file.readlines()

        print(sep_dir, file_name, len(sep_lines))
        print(coef_dir, file_name, len(coef_lines))

        for sep_line, coef_line in zip(sep_lines, coef_lines):

            sep_line.strip()
            data = [ str_to_decimal(val) for val in sep_line.split(',')]
            id = flippable.data_to_id(data)

            coef_line.strip()
            coef_data = [int(val) for val in coef_line.split(',')]
            coef_dict[id] = coef_data

    # get the edges
    file = open(coef_dir + edge_file_name, "r")
    lines = file.readlines()

    edge_list = [line.split(',') for line in lines]

    #print(edge_list)

    #short_edge_list = [edge_list[0], edge_list[1]]

    output = [];

    for edge in edge_list:
        data1 = flippable.data_from_str(edge[0])
        data2 = flippable.data_from_str(edge[1])
        id1 = flippable.data_to_id(data1)
        id2 = flippable.data_to_id(data2)
        coef1 = coef_dict[id1]
        coef2 = coef_dict[id2]
        diff = [str(c1 - c2) for c1,c2 in zip(coef1, coef2)]

        flip="none"

        for d1, d2 in zip(data1, data2):
            print(d1,d2)
            if not d1 == d2:
                bin_array = checkflip.decimal_to_bin_array(d1^d2,5)
                bin_str = ''.join(str(x) for x in bin_array)
                flip = str(d1) + '--' + str(d2) + ',' + bin_str
                break

        output.append(id1 + ',' + id2 + ',' + flip + ',' + ",".join(diff))

        #print(id1, id2, [c1 - c2 for c1,c2 in zip(coef1, coef2)])


    with open(coef_dir + out_file_name, "w") as out_file:
        for x in output:
            print(x)
            out_file.write(x)
            out_file.write('\n')


def runSix():
    conn = mysql.connector.connect(host='localhost', database='mysql', user='root', password='50Fl**rs')

    cur = conn.cursor(buffered=True)

    cur.execute('SELECT DISTINCT flip1, flip2 from Pref_Flip_Six')

    #print()

    flip_list = []
    #for (flip1, flip2) in cur:
    #    print(flip1, flip2, flip1^flip2, checkflip.decimal_to_bin_array(flip1^flip2,6))

    #print('part 2')

#    cur.execute('SELECT * FROM Pref_Flip_Five WHERE flip1 = 4 and flip2 = 3')
#    cur.execute('SELECT * FROM Pref_Flip_Five')
    cur.execute('SELECT * FROM Pref_Flip_Six')

    diff_data = []
    out_data = []

    print('processing flips')
    for (id1, id2, flip1, flip2) in cur:
        data1 = flippable.data_from_id(id1)
        data2 = flippable.data_from_id(id2)

#        diff_data.append([d1 - d2 for d1, d2 in zip(data1, data2)])
        diff = [d1 - d2 for d1, d2 in zip(data1, data2)]

        if not diff in diff_data:
            # we haven't seen this difference before
            diff_data.append(diff)
            #print(diff)
            out_data.append(data1)
            out_data.append(data2)

    #diff_data_set = set(diff_data)

    print('writing flips', len(out_data))
    with open(coef_dir + "n6-diff-all.csv", "w") as out_file:
        for x in out_data:
            #print(x)
            out_file.write(str(x))
            out_file.write('\n')

#######
runSix()