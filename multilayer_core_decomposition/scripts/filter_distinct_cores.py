from __future__ import division
import argparse
from os import getcwd
from os.path import dirname
from ast import literal_eval
from array import array
import sys
sys.path.append('..')

from core_decomposition.subroutines.commons import filter_distinct_cores
from utilities.time_measure import ExecutionTime
from utilities.print_console import print_end_algorithm, print_dataset_name


if __name__ == '__main__':
    # create a parser
    parser = argparse.ArgumentParser(description='Filter Distinct Cores')

    # arguments
    parser.add_argument('cd', help='core decomposition file')

    # read the arguments
    args = parser.parse_args()

    # create the new file for distinct cores only
    distinct_cores_file = open(dirname(dirname(getcwd())) + '/output/' + args.cd + '_distinct.txt', 'w')

    # print the name of the input graph
    print_dataset_name(args.cd.split('_')[0])
    print '---------- Distinct Cores ---------'

    # start of the algorithm
    execution_time = ExecutionTime()

    # dict of cores
    cores = {}

    # open the file
    with open(dirname(dirname(getcwd())) + '/output/' + args.cd + '.txt') as cores_file:
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
    for vector, nodes in cores.iteritems():
        sorted_nodes = list(nodes)
        sorted_nodes.sort()
        distinct_cores_file.write(str(vector) + '\t' + str(len(nodes)) + '\t' + str(sorted_nodes).replace('[', '').replace(']','') + '\n')

    # end of the algorithm
    execution_time.end_algorithm()

    # print algorithm's results
    print_end_algorithm(execution_time.execution_time_seconds, len(cores), None)
