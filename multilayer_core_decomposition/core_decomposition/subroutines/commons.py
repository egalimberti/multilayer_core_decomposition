from collections import deque

from utilities.print_console import *


def build_ancestors_intersection(vector_ancestors, cores, descendants_count, distinct_flag, multilayer_graph=None):
    # order vector_ancestors by the length of the corresponding cores
    vector_ancestors.sort(lambda v, u: cmp(len(cores[v]), len(cores[u])))

    try:
        # initialize ancestors_intersection with the smallest core
        ancestors_intersection = set(cores[vector_ancestors[0]])
        # decrement descendants_count
        decrement_descendants_count(vector_ancestors[0], cores, descendants_count, distinct_flag)

        # for each left ancestor vector
        for ancestor in vector_ancestors[1:]:
            # intersect the corresponding core with ancestors_intersection
            ancestors_intersection &= set(cores[ancestor])
            decrement_descendants_count(ancestor, cores, descendants_count, distinct_flag)

    # if the only ancestor vector is start_vector
    except KeyError:
        ancestors_intersection = set(multilayer_graph.nodes_iterator)

    return ancestors_intersection


def decrement_descendants_count(vector, cores, descendants_count, distinct_flag):
    # decrement descendants_count
    descendants_count[vector] -= 1

    # if the vector has no more descendants in the queue
    if descendants_count[vector] == 0:
        # delete the core for the map of cores if the distinct_flag is off
        if not distinct_flag:
            del cores[vector]
        # delete vector's entry from descendants_count
        del descendants_count[vector]


def build_descendant_vector(ancestor, index):
    descendant = list(ancestor)
    descendant[index] += 1
    return tuple(descendant)


def build_ancestor_vector(descendant, index):
    ancestor = list(descendant)
    ancestor[index] -= 1
    return tuple(ancestor)


def bottom_up_visit(multilayer_graph, start_vector, end_vector, cores, print_file, distinct_flag):
    # initialize the queue of vectors
    vectors_queue = deque()
    vectors_queue.append(start_vector)
    # initialize the set of vectors
    processed_vectors = set()
    processed_vectors.add(start_vector)

    # while vectors_queue is not empty
    while len(vectors_queue) > 0:
        # remove a vector from vectors_queue (FIFO policy)
        vector = vectors_queue.popleft()

        # if the core corresponding to the vector is in not the dict of cores
        if vector not in cores:
            # add the core to the map of cores
            cores[vector] = cores[end_vector]
            if print_file is not None and not distinct_flag:
                print_file.print_core(vector, cores[end_vector])

        # for each layer
        for index in multilayer_graph.layers_iterator:
            # if the ancestor vector is not equal to end_vector
            if vector[index] > end_vector[index] + 1:
                # compute the ancestor vector
                ancestor_vector = build_ancestor_vector(vector, index)

                # if the corresponding core has not been computed yet and it is not in vectors_queue
                if ancestor_vector not in cores and ancestor_vector not in processed_vectors:
                    # add it to the queue
                    vectors_queue.append(ancestor_vector)
                    processed_vectors.add(ancestor_vector)


def post_processing(cores, distinct_flag, print_file):
    if distinct_flag:
        # filter distinct cores
        filter_distinct_cores(cores)

        if print_file is not None:
            print 'Printing cores...'

            # for each core
            for vector, k_core in cores.iteritems():
                # print it
                print_file.print_core(vector, k_core)


def filter_distinct_cores(cores):
    print 'Filtering distinct cores...'

    # vectors ordered by their level
    ordered_vectors = sorted(cores.iterkeys(), key=sum)

    # for each vector in the ordered list
    for vector in ordered_vectors:
        # build the list of its descendant vectors
        descendant_vectors = [build_descendant_vector(vector, index) for index in xrange(len(vector))]

        # for each descendant vector
        for descendant_vector in descendant_vectors:
            # if the descendant vector core is equal to the vector core
            if descendant_vector in cores and len(cores[vector]) == len(cores[descendant_vector]) and set(cores[vector]) == set(cores[descendant_vector]):
                # delete the core and break
                del cores[vector]
                break

    print 'Number of distinct cores: ' + str(len(cores))
