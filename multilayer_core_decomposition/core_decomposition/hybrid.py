from collections import defaultdict
from array import array

from subroutines.pure_core_decomposition import pure_core_decomposition
from subroutines.core import core
from subroutines.commons import *
from utilities.time_measure import ExecutionTime


def hybrid(multilayer_graph, print_file, distinct_flag):
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
        number_of_computed_cores -= 1
    number_of_cores += 1

    # initialize the queue of vectors with the descendants of start_vector and the structure that for each vector saves its ancestor vectors
    vectors_queue = deque()
    ancestors = {}
    for index in multilayer_graph.layers_iterator:
        descendant_vector = build_descendant_vector(start_vector, index)
        vectors_queue.append(descendant_vector)
        ancestors[descendant_vector] = [start_vector]

    # initialize the dictionary that for each vector counts the number of descendants in the queue
    descendants_count = defaultdict(int)

    # compute the core decomposition layer by layer
    for layer in multilayer_graph.layers_iterator:
        cores.update(pure_core_decomposition(multilayer_graph, start_vector, layer, print_file=print_file, distinct_flag=distinct_flag)[0])
    number_of_computed_cores += len(cores) + multilayer_graph.number_of_layers

    # while vectors_queue is not empty
    while len(vectors_queue) > 0:
        # remove a vector from vectors_queue (FIFO policy)
        vector = vectors_queue.popleft()

        # if the number of non zero indexes of vector is equal to the number of its ancestors and is more than 1, build the intersection of its ancestor cores
        number_of_non_zero_indexes = len([index for index in vector if index > 0])
        number_of_ancestors = len(ancestors[vector])
        if number_of_non_zero_indexes == number_of_ancestors and number_of_non_zero_indexes > 1 and vector not in cores:
            ancestors_intersection = build_ancestors_intersection(ancestors[vector], cores, descendants_count, distinct_flag)

            # if the intersection of its ancestor cores is not empty
            if len(ancestors_intersection) > 0:
                # compute the core from it
                k_core, minimum_degrees_vector = core(multilayer_graph, vector, ancestors_intersection, algorithm='h')
                number_of_computed_cores += 1

                # if the core is not empty
                if len(k_core) > 0:
                    # add the core to the dict of cores
                    cores[vector] = k_core
                    if print_file is not None and not distinct_flag:
                        print_file.print_core(vector, k_core)

                    # if the vector of the minimum degrees is not equal to vector
                    if minimum_degrees_vector != vector:
                        # fill the cores that are equals
                        bottom_up_visit(multilayer_graph, minimum_degrees_vector, vector, cores, print_file, distinct_flag)
        else:
            # for each ancestor of vector
            for ancestor in ancestors[vector]:
                # decrement its number of descendants
                decrement_descendants_count(ancestor, cores, descendants_count, distinct_flag)

        # if the core corresponding to the vector is in the dict of cores
        if vector in cores:
            # increment the number of cores
            number_of_cores += 1

            # compute its descendant vectors
            for index in multilayer_graph.layers_iterator:
                descendant_vector = build_descendant_vector(vector, index)

                try:
                    # update the list of the ancestors of the descendant vector
                    ancestors[descendant_vector].append(vector)

                # if the descendant vector has not already been found
                except KeyError:
                    # add the descendant vector to the queue
                    vectors_queue.append(descendant_vector)
                    ancestors[descendant_vector] = [vector]

                # increment descendants_count
                descendants_count[vector] += 1

        # delete vector's entry from ancestors
        del ancestors[vector]

    # end of the algorithm
    execution_time.end_algorithm()

    # print algorithm's results
    print_end_algorithm(execution_time.execution_time_seconds, number_of_cores, number_of_computed_cores)

    # execute the post processing
    post_processing(cores, distinct_flag, print_file)
