from collections import defaultdict
from array import array

from core import core
from objective_function import objective_function
from ..subroutines.commons import *
from utilities.time_measure import ExecutionTime


def densest_subgraph(multilayer_graph, beta):
    # start of the algorithm
    execution_time = ExecutionTime()

    # create the vector of zeros from which start the computation
    start_vector = tuple([0] * multilayer_graph.number_of_layers)

    # dict of cores
    cores = {}

    # solution initialized with the objective function of the whole input graph
    densest_subgraph = array('i', multilayer_graph.get_nodes())
    current_objective_function = objective_function(multilayer_graph.number_of_nodes, multilayer_graph.get_number_of_edges_layer_by_layer(), beta)
    maximum_density = current_objective_function[0]
    maximum_layers = current_objective_function[1]
    maximum_average_degrees = current_objective_function[2]
    densest_subgraph_vector = start_vector

    # initialize the queue of vectors with the descendants of start_vector and the structure that for each vector saves its ancestor vectors
    vectors_queue = deque()
    ancestors = {}
    for index in multilayer_graph.layers_iterator:
        descendant_vector = build_descendant_vector(start_vector, index)
        vectors_queue.append(descendant_vector)
        ancestors[descendant_vector] = [start_vector]

    # initialize the dictionary that for each vector counts the number of descendants in the queue
    descendants_count = defaultdict(int)

    # while vectors_queue is not empty
    while len(vectors_queue) > 0:
        # remove a vector from vectors_queue (FIFO policy)
        vector = vectors_queue.popleft()

        # if the number of non zero indexes of vector is equal to the number of its ancestors, build the intersection of its ancestor cores
        number_of_non_zero_indexes = len([index for index in vector if index > 0])
        number_of_ancestors = len(ancestors[vector])
        if number_of_non_zero_indexes == number_of_ancestors:
            ancestors_intersection = build_ancestors_intersection(ancestors[vector], cores, descendants_count, False, multilayer_graph=multilayer_graph)

            # if the intersection of its ancestor cores is not empty
            if len(ancestors_intersection) > 0:
                # compute the core from it
                core_result = core(multilayer_graph, beta, vector, ancestors_intersection)
                k_core = core_result[0]
            # otherwise
            else:
                # delete its entry from ancestors and continue
                del ancestors[vector]
                continue

            # if the core is not empty
            if len(k_core) > 0:
                # add the core to the dict of cores and increment the number of cores
                cores[vector] = k_core

                # update the densest subgraph if needed
                current_objective_function = core_result[1]
                if current_objective_function[0] >= maximum_density:
                    densest_subgraph = k_core
                    maximum_density = current_objective_function[0]
                    maximum_layers = current_objective_function[1]
                    maximum_average_degrees = current_objective_function[2]
                    densest_subgraph_vector = vector

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
        else:
            # for each ancestor of vector
            for ancestor in ancestors[vector]:
                # decrement its number of descendants
                decrement_descendants_count(ancestor, cores, descendants_count, False)

        # delete vector's entry from ancestors
        del ancestors[vector]

    # end of the algorithm
    execution_time.end_algorithm()

    # print the densest subgraph
    print_densest_subgraph(beta, maximum_density, densest_subgraph, maximum_layers, densest_subgraph_vector, maximum_average_degrees)
