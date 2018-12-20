from crochet_plus import crochet_plus
from subroutines.preprocessing import compute_union_core
from subroutines.theorems import print_fcgqc
from utilities.time_measure import ExecutionTime
from utilities.print_console import print_end_algorithm_fcgqc


def union_core(core_decomposition_file_name, multilayer_graph, gammas, min_sup, min_size, print_file):
    # start of the algorithm
    execution_time = ExecutionTime()

    # obtain a restricted set of nodes from core decomposition
    nodes = compute_union_core(core_decomposition_file_name, gammas, min_sup, min_size)

    # execute crochet+
    fcgqc = crochet_plus(multilayer_graph, gammas, min_sup, min_size, None, nodes=nodes, print_end_algorithm=False)

    # end of the algorithm
    execution_time.end_algorithm()

    # print algorithm's results
    print_end_algorithm_fcgqc(gammas, min_sup, min_size, execution_time.execution_time_seconds, len(fcgqc), len(nodes))

    # print the resulting fcgqc to file
    if print_file is not None:
        print_fcgqc(print_file, fcgqc)

    return fcgqc
