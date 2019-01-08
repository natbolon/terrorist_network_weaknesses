from copy import deepcopy
from fragmentation_measures import *

def find_key_terrorists_fragmentation(adjacency):
    """
    Parameters
    ----------
    adjacency: numpy matrix representing the adjacency matrix of the network.
    
    Returns
    -------
    set_kt: list of indices corresponding to key terrorists in order of decreasing importance
    objective: list of cumulative values of the objective function with each additional key terrorist
    """
    
    # initialize the lists of key terrorists and objective values
    set_kt = []
    objective = [] # cumulative

    # compute metric
    score = F_measure(adjacency)

    # relative size of penalty for including more key terrorists
    C = 0.15
    
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

    while current < objective[-1]:
        # update current objective value
        current = objective[-1]

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
        score = F_measure(new_adjacency)
        key = np.argmax(score)

        # store optimal objective value (cumulative)
        best_score = max(score) - C*(len(set_kt) + 1)
        objective.append(best_score + objective[-1]) 
    return set_kt, objective