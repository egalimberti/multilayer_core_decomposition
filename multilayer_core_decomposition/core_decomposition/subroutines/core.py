from collections import deque
from array import array


def core(multilayer_graph, vector, ancestors_intersection, algorithm=None):
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

    # if the algorithm is hybrid
    if algorithm == 'h':
        # if the core exists
        if len(k_core) > 0:
            # return the computed core and the vector of the minimum degrees
            return array('i', k_core), tuple([min([delta[node][layer] for node in k_core]) for layer in multilayer_graph.layers_iterator])

        # otherwise return the computed empty core and vector
        return array('i', k_core), vector
    else:
        # otherwise return the computed core
        return array('i', k_core)
