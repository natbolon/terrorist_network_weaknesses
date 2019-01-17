from copy import deepcopy
from fragmentation_measures import *
import itertools
import networkx as nx

def compute_objective(adjacency):
    """
    Parameters
    ----------
    adjacency: numpy matrix representing the adjacency matrix of the network.
    
    Returns
    -------
    F + IE + Fd: combined score according to three metrics
    """
	
    F = F_measure(adjacency)
    IE = information_entropy(adjacency)
    Fd = Fd_measure(adjacency)
    return F + IE + Fd
	

def find_key_terrorists_fragmentation(adjacency, labels):
    """
    Parameters
    ----------
    adjacency: numpy matrix representing the adjacency matrix of the network.
    labels: numpy matrix representing the adjacency matrix with labels (-2, -1, 1, 2).
    
    Returns
    -------
    set_kt: list of indices corresponding to key terrorists in order of decreasing importance
    objective: list of cumulative values of the objective function with each additional key terrorist
    """
    
    # initialize the lists of key terrorists and objective values
    set_kt = []
    objective = [] # cumulative

    # compute metric
    score = compute_objective(adjacency)

    # relative size of penalty for including more key terrorists
    C = 0.75
    
    # maximize objective function and store its value
    best_score = max(score) - C*(len(set_kt) + 1)
    objective.append(best_score)

    # find key terrorist
    key = np.argmax(score)

    # initialize objective value
    current = -float('inf')

    # create deep copy of original network
    new_adjacency = deepcopy(adjacency)

    # need this to match identify terrorists later
    original_indices = np.array(range(adjacency.shape[0]))

    iter = 1
    while current < objective[-1]:
        # update current objective value
        current = objective[-1]
        
        graph = nx.from_numpy_matrix(adjacency)
        d = {}
        for index, value in enumerate(score):
            d[index] = value
        nx.set_node_attributes(graph, d, 'score')
        r = {}
        for index, value in np.ndenumerate(labels):
            r[index] = value
        nx.set_edge_attributes(graph, r, 'relations')
        nx.write_gml(graph, "graph_score"+str(iter)+".gml")
        iter = iter+1

        # If the adjacency has been reduced to size 1
        if new_adjacency.shape[0] == 1:
            # store the last key terrorist
            set_kt.append(original_indices[key])
            original_indices = np.delete(original_indices, original_indices[key])

            # default values
            score = 1
            key = 0
            best_score = score - C*(len(set_kt) + 1)
            objective.append(best_score + objective[-1])
            break

        # remove the key terrorist
        new_adjacency[key,:] = 0
        new_adjacency[:,key] = 0
        zero_index = np.where(np.sum(new_adjacency, axis=0) == 0)[0]
        new_adjacency = np.delete(new_adjacency, zero_index, axis=0)
        new_adjacency = np.delete(new_adjacency, zero_index, axis=1)

        # update set of key terrorists
        set_kt.append(original_indices[key])
        original_indices = np.delete(original_indices, original_indices[key])

        # find the next key terrorist
        score = compute_objective(new_adjacency)
        key = np.argmax(score)

        # store optimal objective value (cumulative)
        best_score = max(score) - C*(len(set_kt) + 1)
        objective.append(best_score + objective[-1]) 
    return set_kt, objective

def compute_obj_flow(l_nodes, distance, penalty=0.1):
    """
    Parameters
    ----------
    l_nodes: list of nodes to act as source 
    distance: numpy matrix with distances between all nodes
    penalty: penalty value for large distances
    
    Returns
    -------
    [maxi, n_maxi, mean]: list with maximum distance from the set to any node, 
    number of nodes at the maximum distance and mean distance. 
    obj: objective value 
    """
    # Distance matrix 
    dist = np.minimum(distance[l_nodes[0], :], distance[l_nodes[1], :])
    
    for j in range(2, len(l_nodes)):
        # Update distance as minimum between the new node and the set
        dist = np.minimum(distance[l_nodes[j], :], dist)
    
    maxi = max(dist)
    n_maxi = len(np.where(dist==maxi)[0])
    mean = sum(dist)/len(dist)
    # Compute objective value
    obj = mean + penalty*maxi*n_maxi

    return [maxi, n_maxi, mean] , obj


def find_key_terrorists_flow(adjacency, reg=0.5):
    """
    Parameters
    ----------
    adjacency: numpy matrix representing the adjacency matrix of the largest component
    reg: regularization parameter to penalize the size of the set.
    
    
    Returns
    -------
    OBJ: list of best objective value for the different size of sets.
    NODES: list with set of best nodes for different size of sets. 
    """
    # Create network with the largest component
    G = nx.from_numpy_matrix(adjacency)

    
    # Compute distances between all nodes
    distance_matrix = np.asarray(nx.floyd_warshall_numpy(G))
    
    # Set initial objective value arbitrarily high
    obj = 1000
    nodes = None
    
    best_score = [obj]
    nodes_sets = []
    k = 1 # size of the set
    current = obj
    
    while current >= best_score[-1] :
        # Update current score and size of set
        current = best_score[-1]
        k += 1
        
        print("Exploring sets of {} terrorists...".format(k))
        vals = {}
        vals_obj = {}
       
        # Generate all possible set of nodes with the given size
        for i in tqdm_notebook(list(itertools.combinations(list(range(len(G.nodes))), k))):
            # Compute objective
            args, obj_i = compute_obj_flow(i, distance_matrix)
            if obj_i < obj:
                obj = obj_i
                nodes = i
            vals[i], vals_obj[i] = args, obj_i
        print('Best score achieved with {} people: {}'.format(k, obj + k*0.5))
        best_score.append(obj + k*reg)
        nodes_sets.append(nodes)
        
    return best_score[1:], nodes_sets
