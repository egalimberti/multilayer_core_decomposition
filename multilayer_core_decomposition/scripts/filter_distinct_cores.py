from __future__ import division
import argparse
from os import getcwd
from os.path import dirname
from ast import literal_eval
from array import array
import sys
sys.path.append('..')

from core_decomposition.subroutines.commons import filter_distinct_cores


if __name__ == '__main__':
    # create a parser
    parser = argparse.ArgumentParser(description='Filter Distinct Cores')

    # arguments
    parser.add_argument('d', help='dataset')

    # read the arguments
    args = parser.parse_args()

    # create the new file for distinct cores only
    distinct_cores_file = open(dirname(dirname(getcwd())) + '/output/' + args.d + '_core_decomposition_distinct.txt', 'w')

    # dict of cores
    cores = {}

    # open the file
    with open(dirname(dirname(getcwd())) + '/output/' + args.d + '_core_decomposition.txt') as cores_file:
        # for each line
        for line in cores_file:
            # remove the \n from the line
            line = line.replace('\n', '')

            # split the line
            split_line = line.split('\t')
            vector = literal_eval(split_line[0])
            nodes = array('i', map(int, split_line[2].strip().split(', ')))

            # add the core
            cores[vector] = nodes

    # filter distinct cores
    filter_distinct_cores(cores)

    # print cores to file
    print 'Printing cores...'
    for vector, nodes in cores.iteritems():
        sorted_nodes = list(nodes)
        sorted_nodes.sort()
        distinct_cores_file.write(str(vector) + '\t' + str(len(nodes)) + '\t' + str(sorted_nodes).replace('[', '').replace(']','') + '\n')
