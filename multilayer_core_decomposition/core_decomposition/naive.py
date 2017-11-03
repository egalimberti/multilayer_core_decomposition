from array import array

from subroutines.core import core
from subroutines.commons import *
from utilities.time_measure import ExecutionTime


def naive(multilayer_graph, print_file, distinct_flag):
    # measures
    number_of_cores = 0
    number_of_computed_cores = 0

    # start of the algorithm
    execution_time = ExecutionTime()

    # create the vector of zeros from which start the computation
    start_vector = tuple([0] * multilayer_graph.number_of_layers)

    # dict of cores
    cores = {}

    # core [0]
    if print_file is not None and not distinct_flag:
        print_file.print_core(start_vector, array('i', multilayer_graph.get_nodes()))
    elif distinct_flag:
        cores[start_vector] = array('i', multilayer_graph.get_nodes())
    number_of_cores += 1

    # initialize the queue of vectors with the descendants of start_vector
    vectors_queue = deque()
    computed_vectors = set()
    for index in multilayer_graph.layers_iterator:
        descendant_vector = build_descendant_vector(start_vector, index)
        vectors_queue.append(descendant_vector)
        computed_vectors.add(descendant_vector)

    # set of the nodes of the input graph
    nodes = set(multilayer_graph.nodes_iterator)

    # while vectors_queue is not empty
    while len(vectors_queue) > 0:
        # remove a vector from vectors_queue (FIFO policy)
        vector = vectors_queue.popleft()

        # compute the corresponding core
        k_core = core(multilayer_graph, vector, nodes)
        number_of_computed_cores += 1

        # if the core is not empty
        if len(k_core) > 0:
            # add the core to the dict of cores and increment the number of cores
            if print_file is not None and not distinct_flag:
                print_file.print_core(vector, k_core)
            elif distinct_flag:
                cores[vector] = k_core
            number_of_cores += 1

            # compute its descendant vectors
            for index in multilayer_graph.layers_iterator:
                descendant_vector = build_descendant_vector(vector, index)

                # if the descendant vector has not already been added to the queue
                if descendant_vector not in computed_vectors:
                    # add the descendant vector to the queue
                    vectors_queue.append(descendant_vector)
                    computed_vectors.add(descendant_vector)

    # end of the algorithm
    execution_time.end_algorithm()

    # print algorithm's results
    print_end_algorithm(execution_time.execution_time_seconds, number_of_cores, number_of_computed_cores)

    # execute the post processing
    post_processing(cores, distinct_flag, print_file)
