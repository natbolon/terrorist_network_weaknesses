from copy import deepcopy
from tqdm import tqdm_notebook

def num_disconnected_components(adjacency):
    """
    Parameters
    ----------
    adjacency: numpy matrix representing the adjacency matrix of the network.\
    Assumes connected.
    
    Returns
    -------
    num_dis: a vector of integers, \
    representing the number of disconnected components resulted from removing one node at a time
    """
    
    num_dis = np.empty(adjacency.shape[0])
    for n in range(adjacency.shape[0]):
        temp = deepcopy(adjacency)
        temp[n,:] = 0
        temp[:,n] = 0
        zero_index = np.where(np.sum(temp, axis=0) == 0)[0]
        temp = np.delete(temp, zero_index, axis=0)
        temp = np.delete(temp, zero_index, axis=1)

        # Number of disconnected components normalized by the size of original network
        num_dis[n] = len(find_components(temp)) / adjacency.shape[0]
    return num_dis


def F_measure(adjacency):
    """
    Parameters
    ----------
    adjacency: numpy matrix representing the adjacency matrix of the network.\
        
    Returns
    -------
    If kwarges == None
        F_measure: a vector of floats between 0 and 1, \
        representing the number of disconnected pairs of nodes resulted from removing one node at a time
    
    Otherwise F_measure is a single float between 0 and 1
    """
    
    original_size = adjacency.shape[0]  
    
    F_measure = np.empty(original_size)
    for n in range(original_size):
        temp = deepcopy(adjacency)
        temp[n,:] = 0
        temp[:,n] = 0
        zero_index = np.where(np.sum(temp, axis=0) == 0)[0]
        temp = np.delete(temp, zero_index, axis=0)
        temp = np.delete(temp, zero_index, axis=1)

        components = find_components(temp)
        numerator = 0
        for k in range(len(components)):
            s_k = num_nodes(components[k])
            numerator += s_k * (s_k - 1)
    
        F_measure[n] = 1 - numerator / (original_size * (original_size - 1))
    return F_measure


def information_entropy(adjacency):
    """
    Parameters
    ----------
    adjacency: numpy matrix representing the adjacency matrix of the network.
    
    Returns
    -------
    entropy: a vector of floats between 0 and 1, \
    representing information entropy resulted from removing one node at a time
    """
    
    original_size = adjacency.shape[0]
    entropy = np.empty(original_size)
    for n in range(original_size):
        temp = deepcopy(adjacency)
        temp[n,:] = 0
        temp[:,n] = 0
        zero_index = np.where(np.sum(temp, axis=0) == 0)[0]
        temp = np.delete(temp, zero_index, axis=0)
        temp = np.delete(temp, zero_index, axis=1)

        components = find_components(temp)
        numerator = 0
        for k in range(len(components)):
            s_k = num_nodes(components[k])
            numerator += (s_k / original_size) * np.log(s_k / original_size)

        entropy[n] = -numerator
    return entropy


def Fd_measure(adjacency):
    """
    Parameters
    ----------
    adjacency: numpy matrix representing the adjacency matrix of the network.
    
    Returns
    -------
    Fd: a vector of floats between 0 and 1, \
    representing number of disconnected pairs of nodes, accounting for internal structure,\
    resulted from removing one node at a time
    """
    
    Fd = np.empty(adjacency.shape[0])
    denominator = (adjacency.shape[0]-1) * (adjacency.shape[0]-2) / 2
    for n in tqdm_notebook(range(adjacency.shape[0])):
        temp = deepcopy(adjacency)
        temp[n,:] = 0
        temp[:,n] = 0
        zero_index = np.where(np.sum(temp, axis=0) == 0)[0]
        temp = np.delete(temp, zero_index, axis=0)
        temp = np.delete(temp, zero_index, axis=1)

        numerator = 0
        for i in range(temp.shape[0]):
            shortest_paths_lengths = compute_shortest_path_lengths(temp, i)
            for j in range(temp.shape[0]):
                if i <= j: continue
                numerator += 1 / shortest_paths_lengths[j]

        Fd[n] =  1 - numerator / denominator
    return Fd