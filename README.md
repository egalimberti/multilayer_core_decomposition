# [Core Decomposition in Multilayer Networks: Theory, Algorithms, and Applications](http://edoardogalimberti.altervista.org/documents/papers/Core_Decomposition_and_Densest_Subgraph_in_Multilayer_Networks.pdf)

## Folders
* datasets: subset of datasets listed in Table 1 and example network of Figure 1
* multilayer\_core\_decomposition: code
* output: destination of code's output

## Code
To use the code, first run 'python setup.py build\_ext --inplace' from the folder 'multilayer\_core\_decomposition/'.
This command builds the .c files created by Cython.  
Alternatively, without running the mentioned command, it is possible to directly execute the Python code.

## Execution
Run the following command from the folder 'multilayer\_core\_decomposition/':  
'python multilayer\_core\_decomposition.py [-h] [-b B] [-g G] [-msup MSUP] [-ms MS] [-cd CD] [-q Q] [-r R] [--ver] [--dis] d m'

#### Positional arguments:
  * d           &nbsp;&nbsp;&nbsp;&nbsp;dataset
    * example
    * homo
    * sacchcere
    * dblp
    
  * m           &nbsp;&nbsp;&nbsp;&nbsp;method
    * n         &nbsp;&nbsp;&nbsp;&nbsp;naive method for Multilayer Core Decomposition (beginning of Section 3)
    * bfs       &nbsp;&nbsp;&nbsp;&nbsp;BFS-ML-cores (Algorithm 2)
    * dfs       &nbsp;&nbsp;&nbsp;&nbsp;DFS-ML-cores (Algorithm 3)
    * h         &nbsp;&nbsp;&nbsp;&nbsp;HYBRID-ML-cores (Algorithm 4)
    * i         &nbsp;&nbsp;&nbsp;&nbsp;IM-ML-cores (Algorithm 5)
    * ds        &nbsp;&nbsp;&nbsp;&nbsp;ML-densest (Algorithm 7)
    * c+        &nbsp;&nbsp;&nbsp;&nbsp;Crochet+ [49]
    * c+cd      &nbsp;&nbsp;&nbsp;&nbsp;Corollary 5
    * cs_bfs    &nbsp;&nbsp;&nbsp;&nbsp;BFS-ML-cores for Community Search
    * cs_dfs    &nbsp;&nbsp;&nbsp;&nbsp;DFS-ML-cores for Community Search
    * cs_h      &nbsp;&nbsp;&nbsp;&nbsp;HYBRID-ML-cores for Community Search
    * cs_all    &nbsp;&nbsp;&nbsp;&nbsp;all methods for Community Search
    * info      &nbsp;&nbsp;&nbsp;&nbsp;dataset info

#### Optional arguments:
  * -h, --help  
    show the help message and exit
  
  * -b          &nbsp;&nbsp;&nbsp;&nbsp;beta  
    required for ML-densest and Community Search
    
  * -g          &nbsp;&nbsp;&nbsp;&nbsp;gamma  
    required for Crochet+ and Corollary 5

  * -msup       &nbsp;&nbsp;&nbsp;&nbsp;min\_sup  
    required for Crochet+ and Corollary 5

  * -ms         &nbsp;&nbsp;&nbsp;&nbsp;min\_size  
    required for Crochet+ and Corollary 5

  * -cd         &nbsp;&nbsp;&nbsp;&nbsp;core decomposition file (in folder 'multilayer_core_decomposition/output/') 
    required for Corollary 5

  * -q          &nbsp;&nbsp;&nbsp;&nbsp;query vertices  
    required for Community Search

  * -r          &nbsp;&nbsp;&nbsp;&nbsp;number of random query vertices  
    required for Community Search (alternative to -q)
    
  * --ver       &nbsp;&nbsp;&nbsp;&nbsp;verbose  
  	print the results in the output folder
  	  	
  * --dis       &nbsp;&nbsp;&nbsp;&nbsp;distinct cores  
  	filter distinct cores removing duplicates (please note that this option requires additional memory)
  	
#### Examples:
'python multilayer\_core\_decomposition.py homo h --ver'  
'python multilayer\_core\_decomposition.py homo ds -b 0.1'  
'python multilayer\_core\_decomposition.py homo c+cd -g [0.2,0.2,0.2,0.2,0.2,0.2,0.2] -msup 0.7 -ms 3 -cd homo_h --ver'  
'python multilayer\_core\_decomposition.py homo cs\_bfs -q 1,2 -b 1'  
'python multilayer\_core\_decomposition.py homo cs\_h -r 3 -b 0.1'

## Scripts

### filter\_distinct\_cores.py
The same result obtained by option '--dis' can be achieved by executing a multilayer core decomposition method with option '--ver' and then running the following command from the folder 'multilayer\_core\_decomposition/scripts/':  
'python filter\_distinct\_cores.py [-h] cd'

#### Positional arguments:
  * cd          &nbsp;&nbsp;&nbsp;&nbsp;core decomposition file (in folder 'multilayer_core_decomposition/output/')

#### Optional arguments:
  * -h, --help  
  show the help message and exit
  
#### Example:
'python filter\_distinct\_cores.py homo_h'
  
### filter\_inner\_most\_cores.py
The same output of IM-ML-cores can be obtained by executing a multilayer core decomposition method with option '--ver' and then running the following command from the folder 'multilayer\_core\_decomposition/scripts/':  
'python filter\_inner\_most\_cores.py [-h] cd'

#### Positional arguments:
  * cd          &nbsp;&nbsp;&nbsp;&nbsp;core decomposition file (in folder 'multilayer_core_decomposition/output/')

#### Optional arguments:
  * -h, --help  
  show the help message and exit
  
#### Example:
'python filter\_inner\_most\_cores.py homo_h'
  
## Datasets
Mail to [edoardo.galimberti@isi.it](mailto:edoardo.galimberti@isi.it) for the datasets missing in this repository.
