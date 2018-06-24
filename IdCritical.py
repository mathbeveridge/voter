import prefutils

critical_pairs = [ [ [0,0,0,0,0], [0,0,0,0,1], # 0 < 1
                     [0,0,0,0,1], [0,0,0,1,0], # 1 < 2
                     [0,0,0,1,0], [0,0,1,0,0], # 2 < 3
                     [0,0,1,0,0], [0,1,0,0,0], # 3 < 4
                     [0,1,0,0,0], [0,0,0,1,1], # 4 < 12
                     [0, 0, 0, 1, 1], [1, 0, 0, 0, 0],  # 12 < 5
                     [1, 0, 0, 0, 0], [0, 0, 1, 0, 1],  # 5 < 13
                     [0, 0, 1, 1, 0], [0, 1, 0, 0, 1],  # 23 < 14
                     [1, 0, 0, 0, 1], [0, 1, 0, 1, 0],  # 15 < 24
                     [1, 0, 0, 1, 0], [0, 1, 1, 0, 0],  # 25 < 34
                     [0, 1, 0, 1, 1], [1, 0, 1, 0, 0],  # 124 < 35
                     ]]
 #1 2 3 4 5

 #12 13 14 15
 #   23 24 25
 #      34 35

 # 123 124 125
 #     134 135
 #     234 235

 # 1234 1235 1245
 #           1345
 #           2345


 # 1234 1235 1236
 #      1245 1246 1256
 #      1345 1346 1356 1456
 #      2345 2346 2356 2456
 #                     3456


 # 123 124 125 126
 #     134 135 136
 #     234 235 236
 #         245 246
 #         345 346
 #             356


 # let's count primitive pairs that appear in CSPs
 # I am wondering whether using lists of primitive pairs will be more efficient
 # that listing the top half of the CSP

 # there is some savings, but I think it is more efficient to store a CSP in terms of its
 # n parents and the central flip.

dim = 6

id_list = prefutils.get_id_list(dim)

data_list = []
for id in id_list:
     data_list.append(prefutils.data_from_id(id))

#print(data_list)

count_list = [0] * 2**dim

for data in data_list:
    count = 0
    for i in range(len(data)-1):
        if data[i] + data[i+1] == data[i] ^ data[i+1]:
            #print('\t', data[i], data[i+1])
            count = count + 1

    #print(id, count)

    count_list[count] = count_list[count] + 1

print(count_list)
