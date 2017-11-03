import argparse

from multilayer_graph.multilayer_graph import MultilayerGraph
from core_decomposition.depth_first import depth_first
from core_decomposition.breadth_first import breadth_first
from core_decomposition.hybrid import hybrid
from core_decomposition.densest_subgraph.densest_subgraph import densest_subgraph
from core_decomposition.naive import naive
from utilities.print_console import print_dataset_name, print_dataset_info
from utilities.print_file import PrintFile


if __name__ == '__main__':
    # create a parser
    parser = argparse.ArgumentParser(description='Core Decomposition and Densest Subgraph in Multilayer Networks')

    # arguments
    parser.add_argument('d', help='dataset')
    parser.add_argument('m', help='method')
    parser.add_argument('-b', help='beta', type=float)
    # options
    parser.add_argument('--ver', dest='ver', action='store_true', default=False ,help='verbose')
    parser.add_argument('--dis', dest='dis', action='store_true', default=False ,help='distinct cores')

    # read the arguments
    args = parser.parse_args()

    # create the input graph and print its name
    multilayer_graph = MultilayerGraph(args.d)
    print_dataset_name(args.d)

    # create the output file if the --v option is provided
    if args.ver and args.m in {'bfs', 'dfs', 'h', 'n'}:
        print_file = PrintFile(args.d)
    # set it to None otherwise
    else:
        print_file = None

    # core decomposition algorithms
    if args.m == 'bfs':
        print '---------- Breadth First ----------'
        breadth_first(multilayer_graph, print_file, args.dis)
    elif args.m == 'dfs':
        print '----------- Depth First -----------'
        depth_first(multilayer_graph, print_file, args.dis)
    elif args.m == 'h':
        print '------------- Hybrid --------------'
        hybrid(multilayer_graph, print_file, args.dis)

    # densest_subgraph
    elif args.m == 'ds' and args.b:
        print '--------- Densest Subgraph --------'
        densest_subgraph(multilayer_graph, args.b)

    # naive
    elif args.m == 'n':
        print '-------------- Naive --------------'
        naive(multilayer_graph, print_file, args.dis)

    # dataset information
    elif args.m == 'info':
        print_dataset_info(multilayer_graph)

    # unknown input
    else:
        parser.print_help()
