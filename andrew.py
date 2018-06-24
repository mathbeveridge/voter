import flippable
import checkflip
import prefutils



# this is a file with some random test code

mylist = reversed(range(0,128))
mylist_str = [str(x) for x in mylist]
my_str = '-'.join(mylist_str)
print(my_str)
print(len(my_str))






#data_str = '31-30-29-28-27-26-25-24-23-22-21-20-19-18-17-16-15-14-13-12-11-10-9-8-7-6-5-4-3-2-1-0'
#data = flippable.data_from_str(data_str)

data = [x for x in reversed(range(0,128))]

print('zzzzzz',data)

id = flippable.data_to_id(data)
data2 = flippable.data_from_id(id)



print(data)
print(len(data))

print(id)
print(len(id))

#id_str2 = [str(x) for x in id]
#id_str2 = '-'.join(id_str2)

#print(id_str2)
#print(len(id_str2))

print(len('31-30-29-28-27-26-25-23-24-22-21-20-19-18-17-16'))


print(len('63-62-61-60-59-58-57-56-55-54-53-52-51-50-49-48-47-46-45-44-43-42-41-40-39-38-37-36-35-34-33-32'))


dim = 5


print('==================================================')

id = "31-30-29-27-23-28-26-22-25-15-21-19-24-14-20-13"

id = "31-30-29-27-28-23-26-25-22-21-24-15-19-20-14-13"

id = "31-30-29-27-28-23-26-15-25-22-14-21-24-19-13-20"

id = "31-30-29-27-28-23-26-25-15-22-21-24-19-14-13-11"


#dim = 6

#id = '63-62-61-59-55-47-60-31-58-54-46-57-53-45-51-43-39-30-29-56-27-52-23-44-15-50-42-38-49-41-37-35'

#id = '63-62-61-59-60-58-57-55-47-31-56-54-53-46-51-45-30-43-29-52-27-50-44-49-42-28-41-26-39-25-23-15'

data = flippable.data_from_id(id)

bottom = [18,11,17,12,10,7,16,6,9,8,5,3,4,2,1,0]
top = [31-x for x in reversed(bottom)]
data = top + bottom

# print(sum(data))
# print(31*16)
#
# print(data)
#
# flip_pairs = flippable.get_flippable_pairs(data, dim)
#
#
# print(data)
#
# for i, d in enumerate(data):
#     bin_array = checkflip.int_to_bin_array(d)
#     if len(bin_array) < dim:
#         bin_array = [0] * (dim - len(bin_array)) + bin_array
#     print(bin_array, '\t', d, '\t', i )
#
# print('\t', flip_pairs)
#
# ff_list = []
# for f in flip_pairs:
#     if checkflip.check_order(f[0], f[1]):
#         comp = flippable.get_comp_subsets(f, dim)
#         pair_list = [[f[0] + sum(s), f[1] + sum(s)] for s in comp]
#         print('\t\t', f, pair_list)
#         ff_list.append(pair_list)
#     else:
#         print('\tin  order:', f)

dim = 5

id_list = prefutils.get_id_list(5)

for id in id_list:
    print(id)