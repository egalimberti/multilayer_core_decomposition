from collections import defaultdict

from subroutines.theorems import *
from utilities.time_measure import ExecutionTime
from utilities.print_console import print_end_algorithm_fcgqc


def crochet_plus(multilayer_graph, gammas, min_sup, min_size, print_file, nodes=None, print_end_algorithm=True):
    # start of the algorithm
    execution_time = ExecutionTime()

    # if the subset of nodes is not provided
    if nodes is None:
        # consider every node
        nodes = set(multilayer_graph.nodes_iterator)

    # solution list of frequent cross-graph quasi-cliques
    fcgqc = []

    # order the nodes by Heuristic 1
    nodes_order = order_nodes(multilayer_graph, gammas, nodes, set(multilayer_graph.layers_iterator))

    # for each node (except the last in the ordering)
    for index, node in enumerate(nodes_order[:-1]):
        # create the starting node of the enumeration tree
        tree_node = {node}

        # call the recursive subroutine
        recursive_mine(tree_node, set(nodes_order[index + 1:]), set(multilayer_graph.layers_iterator), multilayer_graph,
                       gammas, min_sup, min_size, fcgqc, nodes_order)

    # end of the algorithm
    execution_time.end_algorithm()

    # print algorithm's results
    if print_end_algorithm:
        print_end_algorithm_fcgqc(gammas, min_sup, min_size, execution_time.execution_time_seconds, len(fcgqc), None)

    # print the resulting fcgqc to file
    if print_file is not None:
        print_fcgqc(print_file, fcgqc)

    return fcgqc


def recursive_mine(tree_node, cand_v, cand_g, multilayer_graph, gammas, min_sup, min_size, fcgqc, nodes_order):
    # compute the candidate nodes for each layer
    cand_v_i = compute_candidate_nodes(tree_node, multilayer_graph, gammas, cand_v, cand_g)

    # start the pruning of cand_v and cand_g
    to_prune = True
    cand_v_len = len(cand_v)
    cand_g_len = len(cand_g)
    while to_prune:
        # initialize cand_v as empty, since it is computed from scratch later in the loop (not explicitly mentioned in the paper)
        cand_v = set()
        layers_to_prune = set()

        # check the pruning conditions in each layer
        for layer in cand_g:
            # lemma 4.1
            projection = reduce_nodes(multilayer_graph, gammas, min_size, tree_node | cand_v_i[layer], layer)

            # lemma 4.6
            if prune_subtree_46(tree_node, projection, fcgqc, min_size):
                # prune the layer
                cand_v_i[layer] = set()
                layers_to_prune.add(layer)
            else:
                # update cand_v_i and cand_v
                cand_v_i[layer] = projection - tree_node
                cand_v |= cand_v_i[layer]

        # update the layers set
        cand_g -= layers_to_prune

        # create the reversed map {node: layers}
        inv_v = defaultdict(set)
        for layer in cand_g:
            for node in cand_v_i[layer]:
                inv_v[node].add(layer)

        # lemma 5.1
        cand_v, cand_g, cand_v_i, inv_v = nodes_layers_reduction(multilayer_graph, tree_node, cand_v, cand_g, cand_v_i,
                                                                 inv_v, min_size, min_sup)

        # if anything has changed
        if len(cand_v) != cand_v_len or len(cand_g) != cand_g_len:
            # restart the pruning cycle
            cand_v_len = len(cand_v)
            cand_g_len = len(cand_g)
        else:
            to_prune = False

    # lemma 5.2
    if prune_subtree_52(multilayer_graph, tree_node, cand_v, cand_g, min_size, min_sup, fcgqc):
        return

    # start the recursive call
    unsubsumed = False
    for index, node in enumerate(nodes_order):
        if node in cand_v:
            # compute cand_g and cand_v for the visit of the child tree node
            cand_g_prime = inv_v[node]
            cand_v_prime = {inner_node for inner_node in nodes_order[index + 1:] if
                            len(cand_g_prime & inv_v[inner_node]) >= multilayer_graph.number_of_layers * min_sup}

            # cand_v_prime is computed differently than the paper, since it doesn't take into account the tree nodes that have at least min_sup * |L| candidate layers
            # then, tree nodes with fewer candidate layers can exist
            # our change guarantees the correctness of the algorithm

            # call of the recursive subroutine
            result_fcgqc = recursive_mine(tree_node.union({node}), cand_v_prime, cand_g_prime, multilayer_graph, gammas,
                                          min_sup, min_size, fcgqc, nodes_order)

            # if there are results
            if result_fcgqc:
                # add the results to the solution and stop the routine
                fcgqc.append(result_fcgqc)
                unsubsumed = True

    if unsubsumed:
        return

    # check that this tree_node is a fcgqc not subset of any other fcgqc
    if check_fcgqc(multilayer_graph, tree_node, gammas, min_size, min_sup):
        for clique in fcgqc:
            if tree_node.issubset(clique):
                return
        return tree_node
