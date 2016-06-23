import numpy as np
import itertools
from random import shuffle

def create_expected_array(lst):
    if len(lst) != 5:
        raise ValueError("wrong list input")

    arr = []

    for i in range(0,4):
        for j in range(i+1,5):
            arr.append(np.sign(lst[i]-lst[j]))
            arr.append(np.sign(lst[j]-lst[i]))    
    return arr

def get_score(inp, compare_to):
    
    if len(inp) != len(compare_to):
        raise ValueError("unequal list lengths")

    score = 0;
    for i in range(len(inp)):
        if inp[i] == compare_to[i]:
            score += 1;
    return score


def has_distances(arr):
    return any([(b!=1 and b!=-1) for b in arr])

def get_order(inputarray):
    if len(inputarray) != 20:
        print("Invalid input array: ", inputarray)
        raise ValueError("Invalid input array")
    
    if(has_distances(inputarray)):
        print("has distances")
        raise ValueError("Distances have not yet been implemented in find_orders")

    currentscore = 0;
    currentorder = 0
    perms = list(itertools.permutations([1,2,3,4,5]))
    shuffle(perms)      # shuffle to take out a bias for orders higher up in the
                        # perms list (for similar scores, the first one that
                        # is encountered is taken)
    for order in perms:
        score = get_score(inputarray, create_expected_array(order))
        if score > currentscore:
            currentscore = score
            currentorder = order
    return currentorder

def find_orders(classification_result):
    step = 20
    i = 0;
    while((i+1)*step <= len(classification_result)):
        start = i*step;
        stop = (i+1)*step;
        order = get_order(classification_result[start:stop]); 
        i += 1
        print("Order: ", order)
        print("Score: ", evaluate(order))
        print("-------------------")


def evaluate(order):
    if len(order) != 5:
        print("Invalid order: ", order)
        raise ValueError("invalid order length")

    # Correct order: (1,2,3,4,5) -> on location i should be number i+1; 
    # Thus, the penalty is equal to abs(i+1 - order[i])
    penalty = 0;
    for i in range(5):
        penalty += abs(i+1 - order[i])
    return penalty


if __name__ == "__main__":
    inp_arr = [     -1, 1, -1, 1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, -1,
                1, -1, 1, -1, 1, -1, 1, -1, 1, 1, -1, 1, -1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1,
                -1, 1, -1, 1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, -1, 1, 1, -1, -1,
                1, -1, 1, 1, -1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, 1, -1, 1, -1, -1, 1,
                -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1,
                1, -1, 1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, -1, 1,
                -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, 1, -1, 1, -1, -1, 1, 1,
                -1, -1, 1, -1, 1, 1, -1, 1, -1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1, -1, -1, 1]
    
    step = 20
    i = 0;
    while((i+1)*step <= len(inp_arr)):
        start = i*step;
        stop = (i+1)*step;
        print(inp_arr[start:stop])
        get_order(inp_arr[start:stop]); 
        i += 1
        print("-------------------")
