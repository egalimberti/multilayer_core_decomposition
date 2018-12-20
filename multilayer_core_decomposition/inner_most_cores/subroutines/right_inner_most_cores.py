from collections import deque
from inner_most_core import inner_most_core
from core_decomposition.subroutines.core_decomposition import core_decomposition


# @profile
def right_inner_most_cores(multilayer_graph, vector, layer, nodes, m, print_file):
    # number of inner most cores
    number_of_inner_most_cores = 0
    number_of_computed_cores = 0

    # *** CASE 1 *** #
    # if the layer is not the last
    next_layer = layer + 1
    if next_layer != multilayer_graph.number_of_layers:
        # create the queue of vectors and the dict of cores
        vectors_queue = deque()
        cores = {vector: nodes}

        # compute the core decomposition
        new_cores, new_cores_order = core_decomposition(multilayer_graph, vector, layer, nodes)
        cores.update(new_cores)
        number_of_computed_cores += len(new_cores_order)

        # update the queue
        vectors_queue.extendleft(new_cores_order)
        vectors_queue.append(vector)

        # recursively call the subroutine
        for next_vector in vectors_queue:
            right_number_of_inner_most_cores, right_number_of_computed_cores = right_inner_most_cores(multilayer_graph, next_vector, next_layer, cores[next_vector], m, print_file)

            number_of_inner_most_cores += right_number_of_inner_most_cores
            number_of_computed_cores += right_number_of_computed_cores

    # *** CASE 2 *** #
    # if the layer is the last
    else:
        # compute the lower bound for the core to be inner most
        k_s = []
        for edit_layer in xrange(layer):
            edit_vector = list(vector[:layer])
            edit_vector[edit_layer] += 1
            edit_vector = tuple(edit_vector)

            try:
                k_s.append(m[edit_vector])
            except KeyError:
                k_s.append(-1)
        lower_bound = max(k_s)

        # build the vector with the lower bound
        lower_bound_vector = list(vector[:layer])
        lower_bound_vector.append(lower_bound)
        lower_bound_vector = tuple(lower_bound_vector)

        # compute the inner most core
        vector_i, nodes_i = inner_most_core(multilayer_graph, lower_bound_vector, layer, nodes)
        number_of_computed_cores += 1

        # if the core exists
        if len(nodes_i) > 0:
            # the core is inner most
            number_of_inner_most_cores += 1

            if print_file is not None:
                print_file.print_core(vector_i, nodes_i)

        # update the structure
        m[vector_i[:layer]] = vector_i[layer]

    # return the inner most cores
    return number_of_inner_most_cores, number_of_computed_cores
