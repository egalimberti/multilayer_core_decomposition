from array import array

from utilities.print_console import *


def pure_core_decomposition(multilayer_graph, vector, layer, print_file, distinct_flag):
    # solution set
    cores = {}

    # populate current_k_core with the set of all nodes of the input multilayer_graph
    current_k_core = set(multilayer_graph.nodes_iterator)
    # instantiate current_vector_list equal to the input vector
    current_vector_list = list(vector)

    # degree of each node in the specified layer
    delta = {}
    # for each node
    for node, neighbors in enumerate(multilayer_graph.adjacency_list):
        # compute the degree in the specified layer
        delta[node] = len(neighbors[layer])

    # sets of nodes divided by degree in the specified layer
    delta_sets = [set() for _ in xrange(max(delta.itervalues()) + 1)]
    # for each node
    for node, degree in delta.iteritems():
        # put the node in the set corresponding to its degree in the specified layer
        delta_sets[degree].add(node)

    # for each set in delta_sets
    for index, delta_set in enumerate(delta_sets):
        # while the set is not empty
        while len(delta_set) > 0:
            # remove a node from the set and from current_k_core
            node = delta_set.pop()
            current_k_core.remove(node)

            # for each neighbor in the specified layer
            for neighbor in multilayer_graph.adjacency_list[node][layer]:
                # if the neighbor is in current_k_core and its delta is more than index
                if neighbor in current_k_core and delta[neighbor] > index:
                    # update its delta_set
                    delta_sets[delta[neighbor]].remove(neighbor)
                    delta_sets[delta[neighbor] - 1].add(neighbor)

                    # update its delta
                    delta[neighbor] -= 1

        # if the core exists
        if len(current_k_core) > 0:
            # build the core index vector of the found core
            current_vector_list[layer] = index + 1
            current_vector = tuple(current_vector_list)
            # add it to the solution set
            cores[current_vector] = array('i', current_k_core)
            if print_file is not None and not distinct_flag:
                print_file.print_core(current_vector, current_k_core)

    return cores
