from __future__ import division

from memory_measure import memory_usage_resource


def print_dataset_name(dataset_path):
    print '------------- Dataset -------------'
    print 'Name: ' + dataset_path.split('/')[0].capitalize()


def print_dataset_info(multilayer_graph):
    number_of_nodes = multilayer_graph.number_of_nodes
    number_of_edges = multilayer_graph.get_number_of_edges()

    print 'Vertices:               ' + str(number_of_nodes)
    print 'Edges:                  ' + str(number_of_edges)
    print 'Layers:                 ' + str(multilayer_graph.number_of_layers)
    print 'Edge density:           ' + str((2 * number_of_edges) / (number_of_nodes * (number_of_nodes - 1)))
    print 'Average-degree density: ' + str(number_of_edges / number_of_nodes)

    for layer in multilayer_graph.layers_iterator:
        print_layer_info(multilayer_graph, layer)


def print_layer_info(multilayer_graph, layer):
    number_of_nodes = multilayer_graph.number_of_nodes
    number_of_edges = multilayer_graph.get_number_of_edges(layer)

    print '------------- Layer ' + str(multilayer_graph.get_layer_mapping(layer)) + ' -------------'
    print 'Edges:                  ' + str(number_of_edges)
    print 'Edge density:           ' + str((2 * number_of_edges) / (number_of_nodes * (number_of_nodes - 1)))
    print 'Average-degree density: ' + str(number_of_edges / number_of_nodes)


def print_end_algorithm(execution_time_seconds, number_of_cores, number_of_computed_cores):
    print 'Execution time:           ' + str(execution_time_seconds) + 's'
    print 'Memory usage:             ' + str(memory_usage_resource()) + 'MB'
    print 'Number of output cores:   ' + str(number_of_cores)
    print 'Number of computed cores: ' + str(number_of_computed_cores)


def print_end_algorithm_fcgqc(gammas, min_sup, min_size, execution_time_seconds, number_of_fcgqc,
                              union_core_size):
    print 'Gamma:                              ' + str(gammas)
    print 'min_sup:                            ' + str(min_sup)
    print 'min_size:                           ' + str(min_size)
    print 'Execution time:                     ' + str(execution_time_seconds) + 's'
    print 'Number of Multilayer Quasi-cliques: ' + str(number_of_fcgqc)
    print 'Number of considered vertices:      ' + str(union_core_size)


def print_end_algorithm_community_search(execution_time_seconds, number_of_computed_cores):
    print 'Execution time:           ' + str(execution_time_seconds) + 's'
    print 'Number of computed cores: ' + str(number_of_computed_cores)
    print '-----------------------------------'


def print_community_search(query, beta, density, nodes, layers, vector):
    # sort query nodes
    query = list(query)
    query.sort()

    print 'Query vertices:                ' + str(query).replace('[', '').replace(']', '')

    print_community(beta, density, nodes, layers, vector)


def print_densest_subgraph(beta, maximum_density, densest_subgraph, maximum_layers, densest_subgraph_vector,
                           maximum_average_degrees):
    print_community(beta, maximum_density, densest_subgraph, maximum_layers, densest_subgraph_vector)

    print 'Average-degree density vector: ' + str(
        tuple(round(average_degree, 2) for average_degree in maximum_average_degrees))


def print_community(beta, density, nodes, layers, vector):
    # sort nodes
    nodes = list(nodes)
    nodes.sort()

    print 'Beta:                          ' + str(beta)
    print 'Density:                       ' + str(density)
    print 'Selected layers:               ' + str([layer + 1 for layer in layers]).replace('[', '').replace(']', '')
    print 'Coreness vector:               ' + str(vector)
