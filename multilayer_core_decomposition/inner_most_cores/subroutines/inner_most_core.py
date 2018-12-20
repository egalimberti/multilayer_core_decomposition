from array import array


# @profile
def inner_most_core(multilayer_graph, vector, layer, nodes):
    # set of active nodes
    active_nodes = set(nodes)

    # degree of each node in each layer
    delta = {}
    # for each node
    for node in nodes:
        # compute the degree in each layer considering only the set of specified nodes
        delta[node] = [len([neighbor for neighbor in multilayer_graph.adjacency_list[node][inner_layer] if neighbor in active_nodes]) for inner_layer in multilayer_graph.layers_iterator]

    # sets of nodes divided by degree in the specified layer
    delta_sets = [set() for _ in xrange(max([node_degrees[layer] for node_degrees in delta.itervalues()]) + 1)]
    # for each node
    for node, node_degrees in delta.iteritems():
        # put the node in the set corresponding to its degree in the specified layer
        delta_sets[node_degrees[layer]].add(node)

    # for each set in delta_sets
    for index, delta_set in enumerate(delta_sets):
        # nodes in the last computed shell
        last_shell = []

        # while the set is not empty
        while len(delta_set) > 0:
            # remove a node from the set and from active_nodes, and add it to last_shell
            node = delta_set.pop()
            active_nodes.remove(node)
            last_shell.append(node)

            # for each neighbor in active_nodes
            for inner_layer, layer_neighbors in enumerate(multilayer_graph.adjacency_list[node]):
                for neighbor in layer_neighbors:
                    if neighbor in active_nodes:
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

        # if there are no active nodes
        if len(active_nodes) == 0:
            # if the core is inner most
            if index > vector[layer]:
                # compute the vector
                last_vector = list(vector)
                last_vector[layer] = index

                # return the inner most core
                return tuple(last_vector), array('i', last_shell)

            # return an empty inner most core
            return vector, array('i')
