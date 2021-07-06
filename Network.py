import torch
import torch.nn.functional as F

from FFN_helpers import *

import random

from CONSTANTS import MAX_SENSOR_DISTANCE


INPUT_SIZE=4
OUTPUT_SIZE=1

#Could also be implemented using just numpy but might as well use this
class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        architecture = generate_random_ffn_architecture(40)
        layer_sizes = [INPUT_SIZE]+architecture+[OUTPUT_SIZE]
        self.layers = torch.nn.ModuleList()

        for i in range(len(layer_sizes)-1):
            in_size = layer_sizes[i]
            out_size = layer_sizes[i+1]
            l = torch.nn.Linear(in_size,out_size)
            #for some reason the weight matrix is transposed?
            l.weight = torch.nn.Parameter(torch.tensor(generate_random_weight_matrix(out_size,in_size,(None,None))).float(),requires_grad=False)
            l.bias = torch.nn.Parameter(torch.tensor(generate_random_bias(out_size)).float(),requires_grad=False)
            self.layers.append(l)

    def forward(self, x):
        for l in self.layers[:-1]:
            #print(l.bias)
            x = F.relu(l(x))
        return self.layers[-1](x)

    def turn(self,food_sensor):
        food_sensor = food_sensor/MAX_SENSOR_DISTANCE
        out = self.forward(torch.tensor(food_sensor).float().unsqueeze(0))
        return out.item()

    def mutate(self):
        #print("Mutating weights")
        #pick random layer
        layer_to_mutate = self.layers[random.randint(0,len(self.layers)-1)].weight
        #print(layer_to_mutate)
        mutate_weight_matrix(layer_to_mutate,0.1)
        #print("Post mutation")
        #print(layer_to_mutate)

    
