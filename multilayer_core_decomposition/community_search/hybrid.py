from collections import defaultdict
from array import array

from core_decomposition.subroutines.pure_core_decomposition import pure_core_decomposition
from core_decomposition.subroutines.core import core
from core_decomposition.subroutines.commons import *
from subroutines.objective_function import objective_function
from utilities.time_measure import ExecutionTime


def hybrid_community_search(multilayer_graph, query_nodes, beta):
    # measures
    number_of_computed_cores = 0

    # start of the algorithm
    execution_time = ExecutionTime()

    # create the vector of zeros from which start the computation
    start_vector = tuple([0] * multilayer_graph.number_of_layers)

    # dict of cores
    cores = {}

    # solution initialized with the whole input graph
    community_search_density = 0.0
    community_search_nodes = array('i', multilayer_graph.get_nodes())
    community_search_layers = set(multilayer_graph.layers_iterator)
    community_search_vector = start_vector

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
        layer_cores, layer_cores_order = pure_core_decomposition(multilayer_graph, start_vector, layer, query_nodes=query_nodes)
        cores.update(layer_cores)

        # update the community search solution if needed
        try:
            core_density, core_layers = objective_function(layer_cores_order[-1], beta)
            if core_density >= community_search_density:
                community_search_density = core_density
                community_search_nodes = layer_cores[layer_cores_order[-1]]
                community_search_layers = core_layers
                community_search_vector = layer_cores_order[-1]
        except IndexError:
            pass
    number_of_computed_cores += len(cores) + multilayer_graph.number_of_layers

    # while vectors_queue is not empty
    while len(vectors_queue) > 0:
        # remove a vector from vectors_queue (FIFO policy)
        vector = vectors_queue.popleft()

        # if the number of non zero indexes of vector is equal to the number of its ancestors and is more than 1, build the intersection of its ancestor cores
        number_of_non_zero_indexes = len([index for index in vector if index > 0])
        number_of_ancestors = len(ancestors[vector])
        if number_of_non_zero_indexes == number_of_ancestors and number_of_non_zero_indexes > 1 and vector not in cores:
            ancestors_intersection = build_ancestors_intersection(ancestors[vector], cores, descendants_count, False)

            # if the intersection of its ancestor contains the query nodes
            if query_nodes <= set(ancestors_intersection):
                # compute the core from it
                k_core, minimum_degrees_vector = core(multilayer_graph, vector, ancestors_intersection, algorithm='h')
                number_of_computed_cores += 1

                # if the core contains the query nodes
                if query_nodes <= set(k_core):
                    # add the core to the dict of cores
                    cores[vector] = k_core

                    # if the vector of the minimum degrees is not equal to vector
                    if minimum_degrees_vector != vector:
                        # fill the cores that are equals
                        bottom_up_visit(multilayer_graph, minimum_degrees_vector, vector, cores, None, False)

                    # update the community search solution if needed
                    core_density, core_layers = objective_function(minimum_degrees_vector, beta)
                    if core_density >= community_search_density:
                        community_search_density = core_density
                        community_search_nodes = k_core
                        community_search_layers = core_layers
                        community_search_vector = minimum_degrees_vector
        else:
            # for each ancestor of vector
            for ancestor in ancestors[vector]:
                # decrement its number of descendants
                decrement_descendants_count(ancestor, cores, descendants_count, False)

        # if the core corresponding to the vector is in the dict of cores
        if vector in cores:
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
    print_end_algorithm_community_search(execution_time.execution_time_seconds, number_of_computed_cores)
    print_community_search(query_nodes, beta, community_search_density, community_search_nodes, community_search_layers, community_search_vector)
