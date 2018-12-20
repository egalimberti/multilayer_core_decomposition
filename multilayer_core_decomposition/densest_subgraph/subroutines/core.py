from collections import deque
from array import array

from objective_function import objective_function


def core(multilayer_graph, beta, vector, ancestors_intersection):
    # solution set
    k_core = set()

    # queue of inactive nodes that have to be processed
    inactive_nodes = deque()
    # set of active nodes
    active_nodes = set(ancestors_intersection)

    # degree of each node in each layer
    delta = {}

    # for each node in ancestors_intersection
    for node in ancestors_intersection:
        # compute the degree in each layer considering only the set of active nodes
        delta[node] = [len([neighbor for neighbor in multilayer_graph.adjacency_list[node][layer] if neighbor in active_nodes]) for layer in multilayer_graph.layers_iterator]
        in_core = True

        # for each layer
        for layer in multilayer_graph.layers_iterator:
            # check if the degree condition over the layer is satisfied
            in_core &= delta[node][layer] >= vector[layer]

        # if the node is potentially in the core
        if in_core:
            # add the node to the solution set
            k_core.add(node)
        # otherwise
        else:
            # remove the node from the set of active nodes and add it to the queue of inactive nodes
            active_nodes.remove(node)
            inactive_nodes.append(node)

            # while the queue of inactive nodes is not empty
            while len(inactive_nodes) > 0:
                # pop a node
                inactive_node = inactive_nodes.popleft()

                # for each neighbor potentially in the core
                for layer, layer_neighbors in enumerate(multilayer_graph.adjacency_list[inactive_node]):
                    for neighbor in layer_neighbors:
                        if neighbor in k_core:
                            # update its delta
                            delta[neighbor][layer] -= 1

                            # if a degree condition over one layer is no more satisfied
                            if delta[neighbor][layer] < vector[layer]:
                                # remove the node from the solution set and from the set of the active nodes, and add it to the queue of inactive nodes
                                k_core.remove(neighbor)
                                active_nodes.remove(neighbor)
                                inactive_nodes.append(neighbor)

    # if the core exists
    core_objective_function = [0.0, set(), tuple()]
    if len(k_core) > 0:
        # compute the number of edges of each layer from delta
        number_of_edges_layer_by_layer = {}
        for layer in multilayer_graph.layers_iterator:
            number_of_edges_layer_by_layer[layer] = sum([delta[node][layer] for node in k_core]) / 2

        # compute k_core's objective function
        core_objective_function = objective_function(len(k_core), number_of_edges_layer_by_layer, beta)

    # return the computed core and its objective function
    return array('i', k_core), core_objective_function
