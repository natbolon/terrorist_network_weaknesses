import numpy as np
import pandas as pd


def connected_graph(adjacency):
    """Determines whether a graph is connected.
    
    Parameters
    ----------
    adjacency: numpy array
        The (weighted) adjacency matrix of a graph.
    
    Returns
    -------
    bool
        True if the graph is connected, False otherwise.
    """
    
    # define all nodes visited in the BFS algorithm when we start from a randomly chosen vertex
    starting_vertex = 0
    visited_dict = breadth_first_search(adjacency, starting_vertex)
    # count total number of vertices
    temp_list = list(visited_dict.values())[:-1] #by default, the last element is an empty set
    count = 0
    for i in range(len(temp_list)):
        count += len(temp_list[i])
    
    # if number of visited vertices equal to total number of vertices, then graph is connected
    if count == len(adjacency):
        return True
    
    return False


def find_components(adjacency):
    """Find the connected components of a graph.
    
    Parameters
    ----------
    adjacency: numpy array
        The (weighted) adjacency matrix of a graph.
    
    Returns
    -------
    list of numpy arrays
        A list of adjacency matrices, one per connected component.
    """
    
    components = []
    # initially, the search list is all the nodes
    search_list = set(range(len(adjacency)))
    
    # run until the search_list is exhausted
    while search_list:
        # next vertex in queue
        vertex = list(search_list).pop(0)
        
        # define an empty adjacency matrix for a component
        component = np.zeros((len(adjacency), len(adjacency)), dtype=int)
        
        visited_dict = breadth_first_search(adjacency, vertex)
        
        # define empty set to collect all nodes in the component
        all_nodes = set()
        nodes_sets = list(visited_dict.values())[:-1] #by default, the last element is an empty set
        for i in range(len(nodes_sets)):
            all_nodes.update(nodes_sets[i])
        
        # create the adjacency matrix for the component
        component[list(all_nodes),:] = adjacency[list(all_nodes),:]
        component[:,list(all_nodes)] = adjacency[:,list(all_nodes)]
        
        # reduce search list by all vertices found in 'visited'
        search_list = search_list - all_nodes

        # add component to list
        components.append(component)
    
    return components

def num_nodes(adjacency):
    '''outputs the number of nodes in a graph given that it is connected'''
    return np.count_nonzero(np.sum(adjacency, axis=1))

def find_largest_component(components):
    '''Takes the list of all components as input (output of find_components)
    Returns the largest component (in terms of number of nodes) and its size.'''
    size = 0
    for c in range(len(components)):
        n = num_nodes(components[c])
        if n > size:
            size = n
            largest_component_index = c
    return components[largest_component_index], size


def breadth_first_search(graph, start):
    '''Takes the adjacencay matrix (graph) and the startin vertex.
    Returns a dictionary whose keys represent (hop) distance from start vertex\
    and values represent all vertices located at that distance from start vertex.
    Only the shortest path is counted.'''
    
    # define a set for all visited nodes.
    visited = set()
    # define dictionary; keys are distances; values are vertices at that distance (from start vertex)
    visited_dict = dict({0: {start}})
    # define a set to keep track of all searched nodes in the BFS algorithm
    searched = set([start])
    
    # all vertices found in the process of BFS are added to the list
    queue = [start]
    while queue:
        # next vertex in the queue
        vertex = queue.pop(0)
        
        if vertex not in visited:
            visited.add(vertex)
            
            # define all the neighbors of the current vertex
            neighbors = set([i for i, x in enumerate(graph[vertex]) if x==1])
            
            # get key of current vertex
            for n in range(len(list(visited_dict.values()))):
                if vertex in list(visited_dict.values())[n]:
                    key = list(visited_dict.keys())[list(visited_dict.values()).index(list(visited_dict.values())[n])]

            # create a new key if key + 1 does not exist yet
            if visited_dict.get(key+1) == None: 
                visited_dict.update({key+1: set()}) # define an empty set for the value of new key
            # update the value of the new key
            visited_dict.get(key+1).update(neighbors - searched)
            searched.update(neighbors)
            
            # add only ones that have not yet been visited to the queue
            queue.extend(neighbors - visited)
    return visited_dict


def compute_shortest_path_lengths(adjacency, source):
    """Compute the shortest path length between a source node and all nodes.
    
    Parameters
    ----------
    adjacency: numpy array
        The (weighted) adjacency matrix of a graph.
    source: int
        The source node. A number between 0 and n_nodes-1.
    
    Returns
    -------
    list of ints
        The length of the shortest path from source to all nodes. Returned list should be of length n_nodes.
    """
    
    shortest_path_lengths = np.zeros(len(adjacency)) - 1
    visited_dict = breadth_first_search(adjacency, source)
    
    list_visited_values = list(visited_dict.values())
    list_visited_keys = list(visited_dict.keys())
    
    for node in range(len(adjacency)):
        for n in range(len(list_visited_values)):
                if node in list(list_visited_values)[n]:
                    # the keys in the distionary are hop distances
                    shortest_path_length = list_visited_keys[list_visited_values.index(list_visited_values[n])]
                    shortest_path_lengths[node] = int(shortest_path_length)
        
    # entries whose values are -1 mean they were disconnected
    shortest_path_lengths[shortest_path_lengths == -1] = float('inf')
    
    return shortest_path_lengths


def compute_average_distance(adjacency):
    """returns the diameter of the provided graph.\
    Returns diameter (length of the longest shortest path between any pair of nodes)"""
    
    # number of nodes in the graph
    list_of_nodes = np.where(np.sum(adjacency, axis=1) > 0)[0]
    avg_dists = []
    
    for _, node in enumerate(list_of_nodes):
        shortest_path_lengths = compute_shortest_path_lengths(adjacency, node)
        
        # exclude infinite distances i.e. disconnected nodes
        shortest_path_lengths = shortest_path_lengths[shortest_path_lengths != float('inf')]
        avg_dists.append(np.average(shortest_path_lengths))
    
    return np.average(avg_dists)


def compute_diameter(adjacency):
    """returns the diameter of the provided graph.\
    Returns diameter (length of the longest shortest path between any pair of nodes)"""
    
    # number of nodes in the graph
    list_of_nodes = np.where(np.sum(adjacency, axis=1) > 0)[0]
    # initialize diameter to be 0
    diameter = 0
    
    for _, node in enumerate(list_of_nodes):
        shortest_path_lengths = compute_shortest_path_lengths(adjacency, node)
        
        # exclude infinite distances i.e. disconnected nodes
        shortest_path_lengths = shortest_path_lengths[shortest_path_lengths != float('inf')]
        max_s = max(shortest_path_lengths)
        
        if max_s > diameter:
            diameter = max_s
    
    return int(diameter)


def compute_clustering_coefficient(adjacency, node):
    """Compute the clustering coefficient of a node.
    
    Parameters
    ----------
    adjacency: numpy array
        The (weighted) adjacency matrix of a graph.
    node: int
        The node whose clustering coefficient will be computed. A number between 0 and n_nodes-1.
    
    Returns
    -------
    float
        The clustering coefficient of the node. A number between 0 and 1.
    """
    
    # CC  =2*L/(k*(k-1))
    # k := Number of neighbors
    # L := Number of links between neighbor nodes
    
    # Get the list of all neighbor nodes
    neighbors = np.nonzero(adjacency[:,node])[0]

    k = len(neighbors)
    if k < 2:
        return 0
    
    # Generate adjacency matrix of neighbor nodes to count their links
    else:
        A = np.take(np.take(adjacency, neighbors, axis=0), neighbors, axis=1)
        L = np.sum(A)/2
        clustering_coefficient = 2*L/(k*(k-1))
    
    
    return float(clustering_coefficient)

def get_true_labels(A):
    """Return the label of each node in he adjacency matrix A
    
    Parameters
    ----------
    A: numpy array
        The (weighted) adjacency matrix of a graph.
    
    Returns
    -------
    numpy array
        The numerical label for each node.
    """
    
    # First we want to get the nodes
    file_path3 = '../data/TerroristRel/TerroristRel_Colleague.nodes'
    file_path4 = '../data/TerroristRel/TerroristRel_Congregate.nodes'
    file_path5 = '../data/TerroristRel/TerroristRel_Contact.nodes'
    file_path6 = '../data/TerroristRel/TerroristRel_Family.nodes'

    n_nodes = A.shape[0]

        # Parse using tab and space delimiters
    terrorist_rel_coll = pd.read_csv(file_path3, delim_whitespace = True, header=None, engine='python')

        # Parse using tab and space delimiters
    terrorist_rel_cong = pd.read_csv(file_path4, delim_whitespace = True, header=None, engine='python')

        # Parse using tab and space delimiters
    terrorist_rel_cont = pd.read_csv(file_path5, delim_whitespace = True, header=None, engine='python')

        # Parse using tab and space delimiters
    terrorist_rel_fam = pd.read_csv(file_path6, delim_whitespace = True, header=None, engine='python')

    # keep id/label information
    colleague = terrorist_rel_coll[[0, 1225]]
    family = terrorist_rel_fam[[0, 1225]]
    congregate = terrorist_rel_cong[[0, 1225]]
    contact = terrorist_rel_cont[[0, 1225]]
    
    # create table containing all labels for each node
    colleague = colleague.set_index(0)
    family = family.set_index(0)
    congregate = congregate.set_index(0)
    contact = contact.set_index(0)
    
    # join to colleagues dataset since adjacency matrix was constructed based on its node ordering 
    labeledNodes = colleague.join(family, on=0, lsuffix='_colleague', rsuffix='_family')
    labeledNodes = labeledNodes.join(congregate, on=0, rsuffix='_congregate')
    labeledNodes = labeledNodes.join(contact, on=0, lsuffix='_congregate', rsuffix='_contact')
    labeledNodes.reset_index(level=0, inplace=True)
    
    labels = dict()
    for i in range(len(list(labeledNodes.index))):
        for relation in [('family',-2), ('congregate',-1), ('colleague',1), ('contact',2)]:
            if labeledNodes.loc[i, '1225_{}'.format(relation[0])] == relation[0]:
                labels[i] = relation[1]
    
    n = list(labels.keys())
    n.sort
    labeledNodes = np.array([labels[i] for i in n])
    
    return labeledNodes
    
def give_names_tonodes(A):
    
    # First we want to get the nodes
    file_path = '../data/TerroristRel/TerroristRel_Colleague.nodes'
    # Parse using tab and space delimiters
    terrorist_rel_coll = pd.read_csv(file_path, delim_whitespace = True, header=None, engine='python')
    
    # keep URL information
    colleague = terrorist_rel_coll[[0]]
    colleague = np.array(colleague)
    name_dict = {}
    for idx in range(colleague.shape[0]):
        url = np.array2string(colleague[idx])
        
        url_split = url.split('#')
        second_name = url_split[2].split("'")[0]
        first_name = url_split[1].split('_http')[0]
        colleague[idx] = first_name + ";" + second_name + "; node:" + str(idx)
        
        # update dictionary where key = name, value = node index
        if name_dict.get(first_name) == None:
            name_dict.update({first_name: set([idx])})
        else:
            name_dict.get(first_name).update(name_dict.get(first_name).union(set([idx])))
        
        if name_dict.get(second_name) == None:
            name_dict.update({second_name: set([idx])})
        else:
            name_dict.get(second_name).update(name_dict.get(second_name).union(set([idx])))
    
    zero_index = np.where(np.sum(A, axis=0) == 0)[0]
    A = np.delete(A, zero_index, axis=0)
    A = np.delete(A, zero_index, axis=1)
    colleague = np.delete(colleague, zero_index, axis=0)
    
    return colleague, A, name_dict;


def give_names_tonodes_dates_based(A):
    
    # First we want to get the nodes
    file_path = '../data/TerroristRel/TerroristRel_Colleague.nodes'
    # Parse using tab and space delimiters
    terrorist_rel_coll = pd.read_csv(file_path, delim_whitespace = True, header=None, engine='python')
    
    # keep URL information
    colleague = terrorist_rel_coll[[0]]
    colleague = np.array(colleague)
    name_dict = {}
    for idx in range(colleague.shape[0]):
        url = np.array2string(colleague[idx])
        
        url_split = url.split('http://')[1:]
        
        # Get name + information 
        info1, first_name = url_split[0].split('#')
       
        # If it has no name, identify by date
        if len(first_name) < 2:
            first_name = info1.split('document')[1]
        if first_name[-1] == '_':
            first_name = first_name[:-1]
            
        
        info2, second_name = url_split[1].split('#')
        # Delete the extra character ']'
        second_name = second_name.split(']')[0]
        
        if len(second_name) < 2:
            second_name = info2.split('document')[1]
            
        second_name = second_name.replace("'", "")
        colleague[idx] = first_name + ";" + second_name + "; node:" + str(idx)
        
        # update dictionary where key = name, value = node index
        if name_dict.get(first_name) == None:
            name_dict.update({first_name: set([idx])})
        else:
            name_dict.get(first_name).update(name_dict.get(first_name).union(set([idx])))
        
        if name_dict.get(second_name) == None:
            name_dict.update({second_name: set([idx])})
        else:
            name_dict.get(second_name).update(name_dict.get(second_name).union(set([idx])))
    
    zero_index = np.where(np.sum(A, axis=0) == 0)[0]
    A = np.delete(A, zero_index, axis=0)
    A = np.delete(A, zero_index, axis=1)
    colleague = np.delete(colleague, zero_index, axis=0)
    
    return colleague, A, name_dict;