from array import array

from subroutines.core_decomposition import core_decomposition
from subroutines.commons import post_processing
from utilities.time_measure import ExecutionTime
from utilities.print_console import *


def depth_first(multilayer_graph, print_file, distinct_flag):
    # measures
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
                    new_cores = core_decomposition(multilayer_graph, vector, base_layer, nodes)
                    temp_base_cores.update(new_cores)
                    number_of_computed_cores += len(new_cores) + 1

                    new_cores_set = set(new_cores)
                    if print_file is not None and not distinct_flag:
                        for new_core in new_cores_set - computed_core_vectors:
                            print_file.print_core(new_core, new_cores[new_core])
                    elif distinct_flag:
                        for new_core in new_cores_set - computed_core_vectors:
                            cores[new_core] = new_cores[new_core]
                    # add the new cores to computed_core_vectors
                    computed_core_vectors |= new_cores_set

            # for each layer not in base_layers
            for layer in layers - base_layers:
                # compute its core decomposition
                if vector[layer] == 0:
                    new_cores = core_decomposition(multilayer_graph, vector, layer, nodes)
                    number_of_computed_cores += len(new_cores) + 1

                    new_cores_set = set(new_cores)
                    if print_file is not None and not distinct_flag:
                        for new_core in new_cores_set - computed_core_vectors:
                            print_file.print_core(new_core, new_cores[new_core])
                    elif distinct_flag:
                        for new_core in new_cores_set - computed_core_vectors:
                            cores[new_core] = new_cores[new_core]
                    # add the new cores to computed_core_vectors
                    computed_core_vectors |= new_cores_set

            # remove every node from the processed core to save memory
            base_cores[vector] = array('i')

        # update the base
        base_cores = temp_base_cores

    # end of the algorithm
    execution_time.end_algorithm()

    # print algorithm's results
    print_end_algorithm(execution_time.execution_time_seconds, len(computed_core_vectors), number_of_computed_cores)

    # execute the post processing
    post_processing(cores, distinct_flag, print_file)
