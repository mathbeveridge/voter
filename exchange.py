import prefutils


### some simple code to investigate Kristin's ideas about
### going directly from words to CSPs

dim = 5



id = '31-30-29-28-27-23-26-22-25-15-21-24-14-20-19-13'

name= '(BBBB-BBBB-BBBB-BBBB-BBBB-)-'


data = prefutils.data_from_id(id)
bin_array = prefutils.data_to_bin_array(data, dim)

print(data)
print(name)

for i,a in enumerate(bin_array):
    aa = [str(x) for x in a]
    print(i, '\t', ','.join(aa))
