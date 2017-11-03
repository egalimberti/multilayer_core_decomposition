from __future__ import division

from memory_measure import memory_usage_resource


def print_dataset_name(dataset_path):
    print '------------- Dataset -------------'
    print 'Name: ' + dataset_path.split('/')[0].capitalize()


def print_dataset_info(multilayer_graph):
    number_of_nodes = multilayer_graph.number_of_nodes
    number_of_edges = multilayer_graph.get_number_of_edges()

    print 'Nodes: ' + str(number_of_nodes)
    print 'Edges: ' + str(number_of_edges)
    print 'Layers: ' + str(multilayer_graph.number_of_layers)
    print 'Edge density: ' + str((2 * number_of_edges) / (number_of_nodes * (number_of_nodes - 1)))
    print 'Average-degree density: ' + str(number_of_edges / number_of_nodes)

    for layer in multilayer_graph.layers_iterator:
        print_layer_info(multilayer_graph, layer)


def print_layer_info(multilayer_graph, layer):
    number_of_nodes = multilayer_graph.number_of_nodes
    number_of_edges = multilayer_graph.get_number_of_edges(layer)

    print '------------- Layer ' + str(multilayer_graph.get_layer_mapping(layer)) + ' -------------'
    print 'Edges: ' + str(number_of_edges)
    print 'Edge density: ' + str((2 * number_of_edges) / (number_of_nodes * (number_of_nodes - 1)))
    print 'Average-degree density: ' + str(number_of_edges / number_of_nodes)


def print_end_algorithm(execution_time_seconds, number_of_cores, number_of_computed_cores):
    print 'Execution time: ' + str(execution_time_seconds) + 's'
    print 'Memory usage: ' + str(memory_usage_resource()) + 'MB'
    print 'Number of cores: ' + str(number_of_cores)
    print 'Number of computed cores: ' + str(number_of_computed_cores)


def print_densest_subgraph(beta, maximum_density, densest_subgraph, maximum_layers, densest_subgraph_vector, maximum_average_degrees):
    # sort nodes
    densest_subgraph = list(densest_subgraph)
    densest_subgraph.sort()

    print 'Beta: ' + str(beta)
    print 'Delta: ' + str(maximum_density)
    print 'Size: ' + str(len(densest_subgraph))
    print 'Number of selected layers: ' + str(len(maximum_layers))
    print 'Selected layers: ' + str([layer + 1 for layer in maximum_layers]).replace('[', '').replace(']', '')
    print 'Corness vector: ' + str(densest_subgraph_vector)
    print 'Average-degree density vector: ' + str(tuple(round(average_degree, 2) for average_degree in maximum_average_degrees))
