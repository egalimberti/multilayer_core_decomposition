from os import getcwd
from os.path import dirname
from array import array
import gc


class MultilayerGraph:

    def __init__(self, dataset_path=None):
        # ****** instance variables ******
        # layers
        self.number_of_layers = 0
        self.layers_iterator = xrange(0)
        self.layers_map = {}

        # nodes and adjacency list
        self.number_of_nodes = 0
        self.maximum_node = 0
        self.nodes_iterator = xrange(0)
        self.adjacency_list = []

        # if dataset_path has been specified
        if dataset_path is not None:
            # read the graph from the specified path
            self.load_dataset(dataset_path)
            # set the dataset path
            self.dataset_path = dataset_path

        # call the garbage collector
        gc.collect()

    def load_dataset(self, dataset_path):
        # open the file
        dataset_file = open(dirname(getcwd()) + '/datasets/' + dataset_path + '.txt')

        # read the first line of the file
        first_line = dataset_file.readline()
        split_first_line = first_line.split(' ')

        # set the number of layers
        self.number_of_layers = int(split_first_line[0])
        self.layers_iterator = xrange(self.number_of_layers)
        # set the number of nodes
        self.number_of_nodes = int(split_first_line[1])
        self.maximum_node = int(split_first_line[2])
        self.nodes_iterator = xrange(self.maximum_node + 1)
        # create the empty adjacency list
        self.adjacency_list = [[array('i') for _ in self.layers_iterator] for _ in self.nodes_iterator]

        # map and oracle of the layers
        layers_map = {}
        layers_oracle = 0

        # for each line of the file
        for index, line in enumerate(dataset_file):
            # split the line
            split_line = line.split(' ')
            layer = int(split_line[0])
            from_node = int(split_line[1])
            to_node = int(split_line[2])

            # if the layer is not in the map
            if layer not in layers_map:
                # add the mapping of the layer
                layers_map[layer] = layers_oracle
                self.layers_map[layers_oracle] = layer
                # increment the oracle
                layers_oracle += 1

            # add the undirected edge
            self.add_edge(from_node, to_node, layers_map[layer])

    def add_edge(self, from_node, to_node, layer):
        # if the edge is not a self-loop
        if from_node != to_node:
            # add the edge
            self.adjacency_list[from_node][layer].append(to_node)
            self.adjacency_list[to_node][layer].append(from_node)

    # ****** nodes ******
    def get_nodes(self):
        if self.number_of_nodes == self.maximum_node:
            nodes = set(self.nodes_iterator)
            nodes.remove(0)
            return nodes
        else:
            return set(self.nodes_iterator)

    # ****** edges ******
    def get_number_of_edges(self, layer=None):
        number_of_edges = 0

        for neighbors in self.adjacency_list:
            for inner_layer, layer_neighbors in enumerate(neighbors):
                if layer is None:
                    number_of_edges += len(layer_neighbors)
                elif layer == inner_layer:
                    number_of_edges += len(layer_neighbors)

        return number_of_edges / 2

    def get_number_of_edges_layer_by_layer(self):
        number_of_edges_layer_by_layer = {}

        for layer in self.layers_iterator:
            number_of_edges_layer_by_layer[layer] = sum([len(neighbors[layer]) for neighbors in self.adjacency_list]) / 2

        return number_of_edges_layer_by_layer

    # ****** layers ******
    def get_layer_mapping(self, layer):
        return self.layers_map[layer]
