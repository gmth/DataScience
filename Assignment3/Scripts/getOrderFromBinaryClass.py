import numpy as np
import itertools
import scipy
from random import shuffle

def create_expected_bin_array(lst):
    if len(lst) != 5:
        raise ValueError("wrong list input")

    arr = []
    for i in range(0,4):
        for j in range(i+1,5):
            arr.append(np.sign(lst[i]-lst[j]))
            arr.append(np.sign(lst[j]-lst[i]))    
    return arr

def create_expected_mult_array(lst):
    if len(lst) != 5:
        raise ValueError("wrong list input")

    arr = []
    for i in range(0,4):
        for j in range(i+1,5):
            arr.append(lst[i]-lst[j])
            arr.append(lst[j]-lst[i])    
    return arr

def get_bin_score(inp, compare_to):    
    if len(inp) != len(compare_to):
        raise ValueError("unequal list lengths")

    score = 0;
    for i in range(len(inp)):
        if inp[i] == compare_to[i]:
            score += 1;
    return score

def get_mult_score(inp, compare_to):    
    if len(inp) != len(compare_to):
        raise ValueError("unequal list lengths")

    score = 0;
    for i in range(len(inp)):
        score += - abs(inp[i] - compare_to[i])
    return score

def is_binary(arr):
    return all([(b==1 or b==-1) for b in arr])

def get_order(inputarray):
    if len(inputarray) != 20:
        print("Invalid input array: ", inputarray)
        raise ValueError("Invalid input array")

    currentscore = -100000
    currentorder = 0
    perms = list(itertools.permutations([1,2,3,4,5]))
    shuffle(perms)      # shuffle to take out a bias for orders higher up in the
                        # perms list (for similar scores, the first one that
                        # is encountered is taken)

    # binary case
    if(is_binary(inputarray)):
        for order in perms:
            score = get_bin_score(inputarray, create_expected_bin_array(order))
            if score > currentscore:
                currentscore = score
                currentorder = order
    # multi-class case
    else:
        for order in perms:
            score = get_mult_score(inputarray, create_expected_mult_array(order))
            if score > currentscore:
                currentscore = score
                currentorder = order
        # raise ValueError("Multiple classes have not yet been implemented in find_orders")
    return currentorder

def find_orders(classification_result):
    step = 20
    i = 0;
    scores = []
    while((i+1)*step <= len(classification_result)):
        start = i*step;
        stop = (i+1)*step;
        order = get_order(classification_result[start:stop]); 
        i += 1

        score = evaluate(order)
        scores.append(score)
        print("Order: ", order)
        print("Score: ", score)
        print("-------------------")
    return scipy.mean(scores)

def evaluate(order):
    if len(order) != 5:
        print("Invalid order: ", order)
        raise ValueError("invalid order length")

    # calculate spearman's coefficient
    sum_d_squared = 0;
    for i in range(5):
        sum_d_squared += (i+1 - order[i])**2
    rho = 1 - (float(6*sum_d_squared) / float(5*(25-1)))
    return rho

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
