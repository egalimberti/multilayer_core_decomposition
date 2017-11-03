from os import getcwd
from os.path import dirname


class PrintFile:

    def __init__(self, dataset_path=None):
        # create the output file
        self.core_decomposition_file = open(dirname(getcwd()) + '/output/' + dataset_path + '_core_decomposition.txt', 'w')

    def print_core(self, vector, k_core):
        # sort the nodes of the core
        sorted_k_core = list(k_core)
        sorted_k_core.sort()
        # write the core to the output file
        self.core_decomposition_file.write(str(vector) + '\t' + str(len(sorted_k_core)) + '\t' + str(sorted_k_core).replace('[', '').replace(']','') + '\n')
