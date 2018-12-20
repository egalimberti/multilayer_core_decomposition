from array import array


def core_decomposition(multilayer_graph, vector, layer, nodes, query_nodes=None):
    # solution set
    cores = {}
    cores_order = []

    # populate current_k_core with the set of specified nodes
    current_k_core = set(nodes)
    # instantiate current_vector_list equal to the list of the input vector
    current_vector_list = list(vector)

    # degree of each node in each layer
    delta = {}
    # for each node
    for node in nodes:
        # compute the degree in each layer considering only the set of specified nodes
        delta[node] = [len([neighbor for neighbor in multilayer_graph.adjacency_list[node][inner_layer] if neighbor in current_k_core]) for inner_layer in multilayer_graph.layers_iterator]

    # sets of nodes divided by degree in the specified layer
    delta_sets = [set() for _ in xrange(max([node_degrees[layer] for node_degrees in delta.itervalues()]) + 1)]
    # for each node
    for node, node_degrees in delta.iteritems():
        # put the node in the set corresponding to its degree in the specified layer
        delta_sets[node_degrees[layer]].add(node)

    # for each set in delta_sets
    for index, delta_set in enumerate(delta_sets):
        # while the set is not empty
        while len(delta_set) > 0:
            # remove a node from the set and from current_k_core
            node = delta_set.pop()
            current_k_core.remove(node)

            # for each neighbor in current_k_core
            for inner_layer, layer_neighbors in enumerate(multilayer_graph.adjacency_list[node]):
                for neighbor in layer_neighbors:
                    if neighbor in current_k_core:
                        delta_neighbor = delta[neighbor][inner_layer]

                        # if inner_layer is the one we are performing the core decomposition on and the delta of the neighbor is more than index
                        if inner_layer == layer and delta_neighbor > index:
                            # update its delta_set
                            delta_sets[delta_neighbor].remove(neighbor)
                            delta_sets[delta_neighbor - 1].add(neighbor)

                            # update its delta
                            delta[neighbor][inner_layer] -= 1

                        # if inner_layer is another layer and the delta of the neighbor is more than the corresponding degree condition
                        elif inner_layer != layer and delta_neighbor >= vector[inner_layer]:
                            # update its delta
                            delta[neighbor][inner_layer] -= 1

                            # if the degree condition over inner_layer is no more satisfied
                            if delta[neighbor][inner_layer] < vector[inner_layer]:
                                # update its delta_set
                                delta_sets[delta[neighbor][layer]].remove(neighbor)
                                delta_sets[index].add(neighbor)

                                # update its delta
                                delta[neighbor][layer] = index

        # if the core contains the query nodes or exists
        if (query_nodes is None and len(current_k_core) > 0) or (query_nodes is not None and query_nodes <= current_k_core):
            # build the core index vector of the found core
            current_vector_list[layer] = index + 1
            current_vector = tuple(current_vector_list)
            # add it to the solution set
            cores[current_vector] = array('i', current_k_core)
            cores_order.append(current_vector)
        elif query_nodes is not None:
            # otherwise conclude the method
            break

    return cores, cores_order
