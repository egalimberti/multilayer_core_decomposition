import os

if __name__ == '__main__':
    # files to be deleted
    paths = [
        'core_decomposition/densest_subgraph/core',
        'core_decomposition/densest_subgraph/densest_subgraph',
        'core_decomposition/densest_subgraph/objective_function',
        'core_decomposition/subroutines/commons',
        'core_decomposition/subroutines/core',
        'core_decomposition/subroutines/core_decomposition',
        'core_decomposition/subroutines/pure_core_decomposition',
        'core_decomposition/breadth_first',
        'core_decomposition/depth_first',
        'core_decomposition/hybrid',
        'core_decomposition/naive',
        'multilayer_graph/multilayer_graph',
        'scripts/filter_distinct_cores',
        'utilities/memory_measure',
        'utilities/print_console',
        'utilities/print_file',
        'utilities/time_measure'
    ]

    # extensions of the files to be deleted
    exts = [
        '.pyx',
        '.so'
    ]

    # for each path
    for path in paths:
        # for each extension
        for ext in exts:
            # delete the file
            try:
                os.remove(path + ext)
            except OSError:
                pass
