from __future__ import division
from collections import deque
import math


# compute the upper bound of the diameter of a quasi-complete graph according to Theorem 1 (pg. 10)
def theorem_diameter(nodes_len, gamma):
    if 1 >= gamma > (nodes_len - 2) / (nodes_len - 1):
        upper_bound = 1
    elif (nodes_len - 2) / (nodes_len - 1) >= gamma >= 1 / 2:
        upper_bound = 2
    elif 1 / 2 > gamma > 1 / (nodes_len - 1) and nodes_len % (math.ceil(gamma * (nodes_len - 1)) + 1) == 0:
        upper_bound = 3 * (math.floor(nodes_len / (math.ceil(gamma * (nodes_len - 1)) + 1))) - 3
    elif 1 / 2 > gamma > 1 / (nodes_len - 1) and nodes_len % (math.ceil(gamma * (nodes_len - 1)) + 1) == 1:
        upper_bound = 3 * (math.floor(nodes_len / (math.ceil(gamma * (nodes_len - 1)) + 1))) - 2
    elif 1 / 2 > gamma > 1 / (nodes_len - 1) and nodes_len % (math.ceil(gamma * (nodes_len - 1)) + 1) >= 2:
        upper_bound = 3 * (math.floor(nodes_len / (math.ceil(gamma * (nodes_len - 1)) + 1))) - 1
    else:
        upper_bound = nodes_len - 1

    return int(upper_bound)


# compute the upper bound of the diameter of a quasi-complete graph according to Corollary 3 (pg. 12)
def upper_bound_diameter(nodes_len, gamma):
    if 1 / 2 <= gamma <= 1:
        return theorem_diameter(nodes_len, gamma)
    else:
        return max(theorem_diameter(length, gamma) for length in xrange(2, nodes_len + 1))


# visit the neighborhood of a node in a layers within a given distance
# optimized to stop once the conditions of the Lemma 4.1 (pg. 17) are not verified anymore
def visit_neighborhood(multilayer_graph, start, layer, distance, nodes, min_size=None, check_all=True):
    # visited nodes and main queue
    visited = {start}
    queue = deque([start])

    # up to the distance
    for _ in xrange(distance):
        # queue to be processed at the next iteration
        next_queue = deque()

        # for each node in the queue
        for node in queue:
            # compute the neighbors not visited yet
            neighbors = {neighbor for neighbor in multilayer_graph.adjacency_list[node][layer] if
                         neighbor in nodes and neighbor not in visited}

            # update the visited nodes and the queue
            visited.update(neighbors)
            next_queue.extend(neighbors)

            # check the return condition
            if not check_all and len(visited) >= min_size:
                return False

        # update the queue for the next iteration
        queue = deque(next_queue)

    if not check_all:
        return True
    else:
        return visited


# reduce the nodes according to the Lemma 4.1 (pg. 17)
def reduce_nodes(multilayer_graph, gammas, min_size, nodes, layer):
    while True:
        # find the first node to prune
        node_to_prune = None
        for node in nodes:
            if len([neighbor for neighbor in multilayer_graph.adjacency_list[node][layer] if neighbor in nodes]) < \
                    gammas[layer] * (min_size - 1) or \
                    visit_neighborhood(multilayer_graph, node, layer,
                                       upper_bound_diameter(len(nodes), gammas[layer]),
                                       nodes, min_size=min_size, check_all=False):
                node_to_prune = node
                break

        # if there is a node to prune
        if node_to_prune:
            nodes.remove(node_to_prune)
        # otherwise the pruning is over
        else:
            return nodes


# order vertices according to Heuristic 1 (pg. 21)
def order_nodes(multilayer_graph, gammas, nodes, layers):
    # compute theta_min for each node
    thetas = {node: min(
        [len([neighbor for neighbor in multilayer_graph.adjacency_list[node][layer] if neighbor in nodes]) / gammas[
            layer] for
         layer in layers]) for node in nodes}

    # order the vertices by thetas
    nodes_order = [node for node, _ in sorted(thetas.iteritems(), key=lambda x: x[1], reverse=True)]

    # return the ordering
    return nodes_order


# compute the candidate nodes according to Lemma 4.4 (pg. 19)
def compute_candidate_nodes(tree_node, multilayer_graph, gammas, cand_v, cand_g):
    # compute the set of nodes to consider
    nodes = tree_node | cand_v

    # compute the difference between C and X
    diff = cand_v - tree_node

    # candidate nodes for each layer
    cand_v_i = {}

    # for each layer
    for layer in cand_g:
        # compute the candidates
        intersection_nodes = [
            visit_neighborhood(multilayer_graph, node, layer, upper_bound_diameter(len(nodes), gammas[layer]), nodes)
            for node in tree_node]
        intersection_nodes.append(diff)
        cand_v_i[layer] = set.intersection(*intersection_nodes)

    # return
    return cand_v_i


# check whether a subtree can be pruned according to Lemma 4.6 (pg. 20)
def prune_subtree_46(tree_node, projection, fcgqc, min_size):
    if len(projection) < min_size:
        return True

    if not tree_node.issubset(projection):
        return True

    for clique in fcgqc:
        if projection.issubset(clique):
            return True

    return False


# reduce candV and candG according to Lemma 5.1 (pg. 26)
def nodes_layers_reduction(multilayer_graph, tree_node, cand_v, cand_g, cand_v_i, inv_v, min_size, min_sup):
    # start the pruning process
    to_prune = True
    while to_prune:
        to_prune = False

        # prune vertices
        nodes_to_prune = set()
        for node in cand_v:
            if len(inv_v[node]) < multilayer_graph.number_of_layers * min_sup:
                # iterate once more since this node will be pruned
                to_prune = True
                nodes_to_prune.add(node)

                # update cand_v_i
                for layer in inv_v[node]:
                    cand_v_i[layer].remove(node)

                # update inv_v
                inv_v[node] = set()

        cand_v -= nodes_to_prune

        # prune layers
        layers_to_prune = set()
        for layer in cand_g:
            if len(tree_node) + len(cand_v_i[layer]) < min_size:
                # iterate once more since this layer will be pruned
                to_prune = True
                layers_to_prune.add(layer)

                # update inv_v
                for node in cand_v_i[layer]:
                    inv_v[node].remove(layer)

                # update cand_v_i
                cand_v_i[layer] = set()
        cand_g.difference_update(layers_to_prune)

    return cand_v, cand_g, cand_v_i, inv_v


# check whether a subtree rooted to a tree_node can be pruned according to Lemma 5.2 (pg. 27)
def prune_subtree_52(multilayer_graph, tree_node, cand_v, cand_g, min_size, min_sup, fcgqc):
    if len(tree_node) + len(cand_v) < min_size:
        return True

    if len(cand_g) < multilayer_graph.number_of_layers * min_sup:
        return True

    # the paper doesn't take into account the union between the tree_node and its candidates but just the tree_node itself
    nodes = tree_node | cand_v
    for clique in fcgqc:
        if nodes.issubset(clique):
            return True

    return False


# check if the nodes are a fcgqc
def check_fcgqc(multilayer_graph, nodes, gammas, min_size, min_sup):
    # verify the number of nodes
    if len(nodes) < min_size:
        return False

    # number of layers in which the nodes have to be quasi-complete
    layers_goal = multilayer_graph.number_of_layers * min_sup

    # check that the requirement is verified
    layers_ok = 0
    for layer in multilayer_graph.layers_iterator:
        layer_ok = True

        # verify that each node satisfies the degree threshold
        degree_threshold = gammas[layer] * (len(nodes) - 1)
        for node in nodes:
            if len([neighbor for neighbor in multilayer_graph.adjacency_list[node][layer] if
                    neighbor in nodes]) < degree_threshold:
                layer_ok = False
                break

        # if the degree condition on the layer is satisfied
        if layer_ok:
            # check the connectivity on the same layer
            if check_connectivity(multilayer_graph, nodes, layer):
                layers_ok += 1

        # if the minimum number of layers is met the nodes form a fcgqc
        if layers_ok >= layers_goal:
            return True

    return False


# verifies the conncetivity of the graph induced by nodes in layer
def check_connectivity(multilayer_graph, nodes, layer):
    # get a random node where to start the visit from
    start = nodes.pop()
    nodes.add(start)

    # start the visit from the node
    queue = deque()
    queue.append(start)
    explored = {start}
    while len(queue) != 0:
        node = queue.pop()

        # get its neighbors and update the structures
        neighbors = {neighbor for neighbor in multilayer_graph.adjacency_list[node][layer] if neighbor in nodes}

        queue.extend(neighbors - explored)
        explored |= neighbors

        # check if all nodes have been visited
        if len(explored) == len(nodes):
            return True

    return False


# print all fcgqc to file
def print_fcgqc(print_file, fcgqc):
    for clique in fcgqc:
        print_file.print_fcgqc(clique)
