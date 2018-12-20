from array import array

from core_decomposition.subroutines.core_decomposition import core_decomposition
from subroutines.objective_function import objective_function
from utilities.time_measure import ExecutionTime
from utilities.print_console import *


def depth_first_community_search(multilayer_graph, query_nodes, beta):
    # measures
    number_of_computed_cores = 0

    # start of the algorithm
    execution_time = ExecutionTime()

    # create the vector of zeros from which start the computation
    start_vector = tuple([0] * multilayer_graph.number_of_layers)

    # solution initialized with the whole input graph
    community_search_density = 0.0
    community_search_nodes = array('i', multilayer_graph.get_nodes())
    community_search_layers = set(multilayer_graph.layers_iterator)
    community_search_vector = start_vector

    # initialize the set of layers
    layers = set(multilayer_graph.layers_iterator)

    # initialize the base of layers
    base_layers = set(layers)

    # initialize the base of cores
    base_cores = {start_vector: array('i', multilayer_graph.nodes_iterator)}

    # set of the vectors corresponding to the computed cores
    computed_core_vectors = set()
    computed_core_vectors.add(start_vector)

    # for each layer
    while len(base_layers) > 0:
        # delete a layer from base_layers
        base_layers.pop()

        # set of the temporary base of cores
        temp_base_cores = {}

        # for each core in the base
        for vector, nodes in base_cores.iteritems():
            # for each layer in the base
            for base_layer in base_layers:
                # compute its core decomposition and store it in temp_base_cores
                if vector[base_layer] == 0:
                    new_cores, new_cores_order = core_decomposition(multilayer_graph, vector, base_layer, nodes, query_nodes=query_nodes)
                    temp_base_cores.update(new_cores)
                    number_of_computed_cores += len(new_cores) + 1

                    # update the community search solution if needed
                    try:
                        core_density, core_layers = objective_function(new_cores_order[-1], beta)
                        if core_density >= community_search_density and [1 if i > j else -1 if i < j else 0 for i, j in zip(new_cores_order[-1], community_search_vector)].count(1) > 0:
                            community_search_density = core_density
                            community_search_nodes = new_cores[new_cores_order[-1]]
                            community_search_layers = core_layers
                            community_search_vector = new_cores_order[-1]
                    except IndexError:
                        pass

                    # add the new cores to computed_core_vectors
                    computed_core_vectors |= set(new_cores)

            # for each layer not in base_layers
            for layer in layers - base_layers:
                # compute its core decomposition
                if vector[layer] == 0:
                    new_cores, new_cores_order = core_decomposition(multilayer_graph, vector, layer, nodes, query_nodes=query_nodes)
                    number_of_computed_cores += len(new_cores) + 1

                    # update the community search solution if needed
                    try:
                        core_density, core_layers = objective_function(new_cores_order[-1], beta)
                        if core_density >= community_search_density and [1 if i > j else -1 if i < j else 0 for i, j in zip(new_cores_order[-1], community_search_vector)].count(1) > 0:
                            community_search_density = core_density
                            community_search_nodes = new_cores[new_cores_order[-1]]
                            community_search_layers = core_layers
                            community_search_vector = new_cores_order[-1]
                    except IndexError:
                        pass

                    # add the new cores to computed_core_vectors
                    computed_core_vectors |= set(new_cores)

            # remove every node from the processed core to save memory
            base_cores[vector] = array('i')

        # update the base
        base_cores = temp_base_cores

    # end of the algorithm
    execution_time.end_algorithm()

    # print algorithm's results
    print_end_algorithm_community_search(execution_time.execution_time_seconds, number_of_computed_cores)
    print_community_search(query_nodes, beta, community_search_density, community_search_nodes, community_search_layers, community_search_vector)
