
import numpy as np

from CONSTANTS import *

import random


def generate_random_ffn_architecture(n_nodes):
    used_nodes=0
    layer_sizes=[]
    while(used_nodes<n_nodes):
        if(n_nodes-used_nodes>MIN_NODES_PER_LAYER):
            l = max(MIN_NODES_PER_LAYER,int(np.random.randn()*3) +8)
            layer_sizes.append(l)
            used_nodes+=l
        else:
            break
    return layer_sizes

#weight_range doesnt do anything yet
def generate_random_weight_matrix(m,n,weight_range):
    min_w,max_w = weight_range
    #values in [0,1]
    mat = np.random.random((m,n))
    #values in [-2,2]
    mat = (mat-0.5)*4
    #randomly 0 a random percentage of them
    mask = np.random.random((m,n))<np.random.random()
    mat[mask]=0
    return mat

def generate_random_bias(n):
    #vec = np.expand_dims((np.random.random(n)-0.5),0)
    vec = np.expand_dims([-0.2 for i in range(n)],0)
    return vec

#should we also mutate biases? I dont think traditional neurons do
#can update this to mutate multiple at once
#changes in place
def mutate_weight_matrix(mat,sigma):
    r,c = np.random.randint(mat.shape[0]),np.random.randint(mat.shape[1])
    new_weight = sigma*np.random.randn()+mat[r,c]
    mat[r,c]=new_weight



#will have to be implemented in torch
#basically add another node at a random layer with random weight vector (with high 0 percentage)
def add_new_node():
    pass





