import argparse
from random import randint

from multilayer_graph.multilayer_graph import MultilayerGraph
from core_decomposition.depth_first import depth_first
from core_decomposition.breadth_first import breadth_first
from core_decomposition.hybrid import hybrid
from inner_most_cores.inner_most import inner_most
from densest_subgraph.densest_subgraph import densest_subgraph
from community_search.breadth_first import breadth_first_community_search
from community_search.depth_first import depth_first_community_search
from community_search.hybrid import hybrid_community_search
from core_decomposition.naive import naive
from crochet_plus.union_core import union_core
from crochet_plus.crochet_plus import crochet_plus
from utilities.print_console import print_dataset_name, print_dataset_info
from utilities.print_file import PrintFile


if __name__ == '__main__':
    # create a parser
    parser = argparse.ArgumentParser(description='Core Decomposition and Densest Subgraph in Multilayer Networks')

    # arguments
    parser.add_argument('d', help='dataset')
    parser.add_argument('m', help='method')

    parser.add_argument('-b', help='beta', type=float)

    parser.add_argument('-g', help='gamma')
    parser.add_argument('-msup', help='min_sup', type=float)
    parser.add_argument('-ms', help='min_size', type=int)
    parser.add_argument('-cd', help='core decomposition file')

    parser.add_argument('-q', help='query vertices', type=str)
    parser.add_argument('-r', help='number of random query vertices', type=int)

    # options
    parser.add_argument('--ver', dest='ver', action='store_true', default=False, help='verbose')
    parser.add_argument('--dis', dest='dis', action='store_true', default=False, help='distinct cores')

    # read the arguments
    args = parser.parse_args()

    # select the ordering in function of the method
    ordering = None
    if args.m == 'i':
        ordering = 'i'

    # create the input graph and print its name
    multilayer_graph = MultilayerGraph(args.d, ordering)
    print_dataset_name(args.d)

    # create the output file if the --v option is provided
    if args.ver and args.m in {'n', 'bfs', 'dfs', 'h', 'i', 'c+', 'c+cd'}:
        if args.m in {'c+', 'c+cd'}:
            print_file = PrintFile(args.d + '_' + args.m + '_' + args.g + '_' + str(args.msup) + '_' + str(args.ms))
        else:
            print_file = PrintFile(args.d + '_' + args.m)
    # set it to None otherwise
    else:
        print_file = None

    # create the random query nodes string
    if args.r and args.m in {'cs_bfs', 'cs_dfs', 'cs_h', 'cs_all'}:
        args.q = ''.join([str(randint(1, multilayer_graph.maximum_node)) + ',' for _ in xrange(args.r - 1)]) + str(randint(1, multilayer_graph.maximum_node))

    # core decomposition
    if args.m == 'n':
        print '-------------- Naive --------------'
        naive(multilayer_graph, print_file, args.dis)
    elif args.m == 'bfs':
        print '---------- Breadth First ----------'
        breadth_first(multilayer_graph, print_file, args.dis)
    elif args.m == 'dfs':
        print '----------- Depth First -----------'
        depth_first(multilayer_graph, print_file, args.dis)
    elif args.m == 'h':
        print '------------- Hybrid --------------'
        hybrid(multilayer_graph, print_file, args.dis)

    # inner most cores
    elif args.m == 'i':
        print '------------ Inner-most -----------'
        inner_most(multilayer_graph, print_file)

    # densest subgraph
    elif args.m == 'ds' and args.b:
        print '--------- Densest Subgraph --------'
        densest_subgraph(multilayer_graph, args.b)

    # crochet+
    elif args.m == 'c+' and args.msup and args.ms and args.g:
        print '------------- Crochet+ ------------'
        crochet_plus(multilayer_graph, eval(args.g), args.msup, args.ms, print_file)
    elif args.m == 'c+cd' and args.msup and args.ms and args.g and args.cd:
        print '------------ Crochet+ CD ----------'
        union_core(args.cd, multilayer_graph, eval(args.g), args.msup, args.ms, print_file)

    # community search
    elif args.m == 'cs_bfs' and args.b and args.q:
        print '------ Community Search BFS -------'
        breadth_first_community_search(multilayer_graph, set([int(node) for node in args.q.split(',')]), args.b)
    elif args.m == 'cs_dfs' and args.b and args.q:
        print '------ Community Search DFS -------'
        depth_first_community_search(multilayer_graph, set([int(node) for node in args.q.split(',')]), args.b)
    elif args.m == 'cs_h' and args.b and args.q:
        print '------- Community Search H --------'
        hybrid_community_search(multilayer_graph, set([int(node) for node in args.q.split(',')]), args.b)
    elif args.m == 'cs_all' and args.b and args.q:
        query_nodes = set([int(node) for node in args.q.split(',')])
        print '------ Community Search BFS -------'
        breadth_first_community_search(multilayer_graph, query_nodes, args.b)
        print '------ Community Search DFS -------'
        depth_first_community_search(multilayer_graph, query_nodes, args.b)
        print '------- Community Search H --------'
        hybrid_community_search(multilayer_graph, query_nodes, args.b)

    # dataset information
    elif args.m == 'info':
        print_dataset_info(multilayer_graph)

    # unknown input
    else:
        parser.print_help()
