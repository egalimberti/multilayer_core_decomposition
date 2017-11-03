# Core Decomposition and Densest Subgraph in Multilayer Networks

### Folders
* datasets: subset of datasets listed in Table 1 and example network of Figure 1
* multilayer_core_decomposition: code
* output: destination of code's output

### Code
To use the code, first run 'python setup.py build_ext --inplace' from the folder 'multilayer_core_decomposition/'.
This command builds the .c files created by Cython.
Alternatively, without running the mentioned command, it is possible to directly execute the Python code.

### Execution
Run the following command from the folder 'multilayer_core_decomposition/':
  'python multilayer_core_decomposition.py [-h] [-b B] [--ver] [--dis] d m'

#### Positional arguments:
  * d           dataset
    * example
    * homo
    * sacchcere
    * dblp
    * obamainisrael
    * amazon
    * friendfeedtwitter
    * higgs
    * friendfeed
    
  * m           method
    * n         naive method (beginning of Section 3)
    * bfs       BFS-ML-cores (Algorithm 2)
    * dfs       DFS-ML-cores, (Algorithm 3)
    * h         HYBRID-ML-cores, (Algorithm 4)
    * ds        ML-densest (Algorithm 5)
    * info      dataset info

#### Optional arguments:
  * -h, --help  show the help message and exit
  
  * -b B        beta
    required for ML-densest (Algorithm 5)
    
  * --ver       verbose
  	print the resulting multilayer core decomposition in the output folder with the format 'coreness_vector	size	nodes'
  	
  * --dis       distinct cores
  	filter distinct cores removing duplicates (please note that this option requires additional memory)
  	
#### Example:
  'python multilayer_core_decomposition.py homo h --ver'

### Script
The same result obtained by option '--dis' can be achieved by executing a multilayer core decomposition method with option '--ver' and then running the following command from the folder 'multilayer_core_decomposition/scripts/':
  'python filter_distinct_cores.py [-h] d'

#### Positional arguments:
  * d           dataset

#### Optional arguments:
  * -h, --help  show the help message and exit
  
#### Example:
  'python filter_distinct_cores.py homo'
