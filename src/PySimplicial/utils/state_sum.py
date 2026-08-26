import opt_einsum
import numpy as np


def state_sum(C, b_inv, v_p, g_edges, open_ports=()): # pass values from graph() and C (c3) and b_inv

    """
    This function deserves a separate discussion:

    it implements convolution over triangulation, but by itself does not guarantee topological invariance. Invariance depends on the tensors C and b_inv, which in the trained version may not satisfy the Frobenius axioms. That is, for the correct result you need a fixed Frobenius algebra
    
    """
    ops = [] # main list for opt_einsum, here we will add all arguments
    for (a,b,c) in v_p: # as example let take v_p = [(0,1,2),(3,4,5)]
        ops += [C, (a,b,c)] # for every unique port ID lets compare the index =>
        # => (t0,t1,t2,t3,t4,t5) => ops += [C, (0,1,2)] => C_t0,t1,t2 ; ops += [C,(3,4,5)] => C_t3,t4,t5 ; C_a,b,c for each triangle
    for (x,y) in g_edges: # g_edges=[1,5]
        ops += [b_inv, (x,y)] # b_inv = (B^-1)_t1,t5
    ops += [tuple(open_ports)] # open_ports=[0,2,3,4]
    # After all: Z_T0 = sum_t1,t2,t3,t4,t5 C_t0,t1,t2 * C_t3,t4,t5 * (B^-1)_t1,t5
    return opt_einsum.contract(*ops, optimize="greedy") # opt_einsum its just better version of basic einsum, it searches the best way to sum huge values
