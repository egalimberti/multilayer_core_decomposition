import re
from math import ceil


# pre-process core decomposition for selecting the cores that lead to fcgqcs
def compute_union_core(core_decomposition_file_name, gammas, min_sup, min_size):
    # regular expressions to read the file
    coreness_vector_reg = re.compile('\(.+\)')
    nodes_reg = re.compile('(?<=\t)\d+,.+\n')

    union_core = set()
    layers_threshold = ceil(len(gammas) * min_sup)
    limit_coreness_vector = tuple(ceil(gamma * (min_size - 1)) for gamma in gammas)

    with open('../output/' + core_decomposition_file_name + '.txt', 'r') as core_decomposition_file:
        for line in core_decomposition_file:
            # extract the coreness vector
            coreness_vector = eval('(' + coreness_vector_reg.match(line).group()[1:-1] + ')')

            # check the condition over the layers
            if len(tuple(True for index, limit_index in zip(coreness_vector, limit_coreness_vector) if index == limit_index)) == layers_threshold:
                x = eval('{' + nodes_reg.search(line).group() + '}')
                union_core |= eval('{' + nodes_reg.search(line).group() + '}')

    return union_core
