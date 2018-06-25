import os as os

import flippable
import prefutils

######


#dim = 4
#filenames = [ "/bean/mac/research/tran/n4sep/s3v1s4v1.csv",
#              "/bean/mac/research/tran/n4sep/s3v1s4v2.csv" ]
#out_file_name = "/bean/mac/research/tran/n4sep-coef/n4edges.csv"

# this is the file system version of gensep and gensepbatch
def run():

    dim = 6
    dirname = "/bean/mac/research/tran/n5sep/"
    filenames = os.listdir(dirname)
    filenames = [dirname + fn for fn in filenames]

    out_file_name = "/bean/mac/research/tran/n5sep-coef/n5edges.csv"

    edges = set()

    for filename in filenames:

        print('================', filename)

        # read the file
        file = open(filename, "r")
        lines = file.readlines()

        for line in lines:
            data = [int(s, 2) for s in line.split(',')]

            data_str = prefutils.data_to_str(data)

            print(data)

            # print("primitive pairs:")

            # print(get_primitive_pairs(data))

            flippable_pairs = flippable.get_flippable_pairs(data,dim)

            print("flippable pairs:", flippable_pairs, '\n')

            flipped_data = [flippable.flip(data, flip_pair, dim) for flip_pair in flippable_pairs]

            for f in flipped_data:
                print('\t', f)

                f_str = prefutils.data_to_str(f)

                if (data_str < f_str):
                    edges.add(data_str + ',' + f_str)
                else:
                    edges.add(f_str + ',' + data_str)


                    # bin_pairs = pairwise()

    out_file = open(out_file_name, "w")

    for edge in edges:
        print(edge)
        out_file.write(edge + '\n')