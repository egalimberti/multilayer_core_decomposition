from distutils.core import setup
from distutils.extension import Extension
from shutil import copyfile

if __name__ == '__main__':
    # files to be included in the extensions
    paths = [
        'community_search/breadth_first',
        'community_search/depth_first',
        'community_search/hybrid',
        'community_search/subroutines/objective_function',
        'core_decomposition/subroutines/commons',
        'core_decomposition/subroutines/core',
        'core_decomposition/subroutines/core_decomposition',
        'core_decomposition/subroutines/pure_core_decomposition',
        'core_decomposition/breadth_first',
        'core_decomposition/depth_first',
        'core_decomposition/hybrid',
        'core_decomposition/naive',
        'core_decomposition/naive',
        'crochet_plus/subroutines/preprocessing',
        'crochet_plus/subroutines/theorems',
        'crochet_plus/crochet_plus',
        'crochet_plus/union_core',
        'densest_subgraph/subroutines/core',
        'densest_subgraph/subroutines/objective_function',
        'densest_subgraph/densest_subgraph',
        'inner_most_cores/inner_most',
        'inner_most_cores/subroutines/inner_most_core',
        'inner_most_cores/subroutines/right_inner_most_cores',
        'multilayer_graph/multilayer_graph',
        'scripts/filter_distinct_cores',
        'scripts/filter_inner_most_cores',
        'utilities/memory_measure',
        'utilities/print_console',
        'utilities/print_file',
        'utilities/time_measure'
    ]

    # import Cython if available
    USE_CYTHON = True
    try:
        from Cython.Build import cythonize
    except ImportError:
        cythonize = None
        USE_CYTHON = False

    # if Cython is available
    if USE_CYTHON:
        # set the .pyx extension
        ext = '.pyx'

        # create the new .pyx files
        for path in paths:
            copyfile(path + '.py', path + ext)
    # otherwise
    else:
        # set the .c extension
        ext = '.c'

    # build the extensions list
    extensions = [Extension(path.replace('/', '.'), [path + ext]) for path in paths]

    # if Cython is available
    if USE_CYTHON:
        # cythonize the extensions
        extensions = cythonize(extensions)

    # run the setup
    setup(
         ext_modules=extensions
    )
