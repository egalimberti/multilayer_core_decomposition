from array import array

from subroutines.right_inner_most_cores import right_inner_most_cores
from utilities.time_measure import ExecutionTime
from utilities.print_console import *


def inner_most(multilayer_graph, print_file):
    # start of the algorithm
    execution_time = ExecutionTime()

    # create the data structure
    m = {}

    # create the vector of zeros and the set of nodes
    vector = tuple([0] * multilayer_graph.number_of_layers)
    nodes = array('i', multilayer_graph.nodes_iterator)

    # call the subroutine
    number_of_inner_most_cores, number_of_computed_cores = right_inner_most_cores(multilayer_graph, vector, 0, nodes, m, print_file)

    # end of the algorithm
    execution_time.end_algorithm()

    # print algorithm's results
    print_end_algorithm(execution_time.execution_time_seconds, number_of_inner_most_cores, number_of_computed_cores)
