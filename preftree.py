import os as os

from anytree import Node, RenderTree

from anytree.exporter import DotExporter


#filenames = { "/bean/mac/research/tran/n4sep/s3v1s4v1.csv",
#          "/bean/mac/research/tran/n4sep/s3v1s4v2.csv"}


dim = 5

dirname = "/bean/mac/research/tran/n5sep/"

filenames = os.listdir(dirname)


#######
node_dict = {}

root_name = '/11111'
root = Node('11111')
node_dict[root_name] = root
#####

for filename in filenames:

    print('================', filename)



    # read the file
    file = open(dirname + filename, "r")
    lines = file.readlines()

    # print(lines)






    for line in lines:
        preference = line.strip().split(',')
        p = preference[0:2 ** (dim - 1)]

        path = ''

        for outcome in p:
            path = path + '/' + outcome
            # print('>>>>> path=' + path)

            if path in node_dict:
                node = node_dict[path]
                # print("    node is ", node)
            else:
                # print("didn't find", path, " and had node ", node)
                # print("   adding ", path, " to outcome ", outcome, "with parent", node)
                node = Node(outcome, parent=node)
                # print("   node is now ", node)
                node_dict[path] = node;


for pre, fill, node in RenderTree(root):
    print("%s%s" % (pre, node.name))

#print(RenderTree(root))
