from __future__ import division


def objective_function(vector, beta):
    # maximum density
    maximum_density = 0.0
    # set of layers that maximizes the density
    maximum_layers = set()

    # sort the layers by their minimum degree
    sorted_layers = [element[0] for element in sorted(enumerate(vector), key=lambda x:x[1], reverse=True)]

    try:
        # for each layer
        for number_of_layers, layer in enumerate(sorted_layers, 1):
            # compute the density
            layer_density = vector[layer] * number_of_layers ** beta

            # if the density is greater or equal than the maximum density
            if layer_density >= maximum_density:
                # update the maximum density
                maximum_density = layer_density
                # update the set of layers that maximizes the density
                maximum_layers = set(sorted_layers[:number_of_layers])
    except ZeroDivisionError:
            pass

    return maximum_density, maximum_layers
