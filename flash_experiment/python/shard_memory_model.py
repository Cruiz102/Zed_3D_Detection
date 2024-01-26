import torch
import torch.nn as nn
import argparse

from safetensors import safe_open

from safetensors.torch import save_file
from typing import List
import os
import psutil
# Create a Dense model and serealized his weights into shards. So that only 1 shard can be load into ram
# We are going to test how fast can be a model with limited memory in hardware if sharding the processes step by step



class DenseModel(nn.Module):
    def __init__(self, input_size: int ,hidden_layers: int,layer_width: int,  output_size: int):
        super(DenseModel,self).__init__()
        self.input_size = input_size
        self.hidden_layers = hidden_layers
        self.layer_width = layer_width
        self.output_size = output_size


        # Layers
        self.layers = nn.ModuleList()
        last_size = input_size
        for i in range(self.hidden_layers):
            self.layers.append(nn.Linear(last_size, self.layer_width))
            self.layers.append(nn.ReLU())
            last_size = self.layer_width
            if i % 5 == 0:
                self.layers.append(nn.Dropout(0.2))


        # Output layer
        self.layers.append(nn.Linear(last_size, self.output_size))



    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x
    

class ShardedModel(nn.Module):
    def __init__(self, weight_path: str, model: torch.nn.Module):
        super(ShardedModel, self).__init__()
        self.weight_path = weight_path
        self.model_layers = model.children()

    def forward(self, x):
        # Gradients are not saved  for reducing memory
        with torch.no_grad():
            temporal_output_tensor = x
            shard_id = 0
            for path in os.listdir(self.weight_path):
                with safe_open(os.path.join(self.weight_path, f"shard_{shard_id}.safetensors"), framework="pt", device="cpu") as f:
                    for layer_name in f.keys():_
                        f.get_tensor(layer_name)
                        temporal_output_tensor = f.get_tensor(layer_name)
                del sharded_module
                
                shard_id += 1


        return temporal_output_tensor
    





def load_model_weights(model_path: str):
    pass

def get_sharded_model(model: nn.Module, num_shards: int, memory_constraint: int):
    # Create a list of shards
    pass


def check_contraint(runner_function, memory_constraint: int):
    if benchmark.measure_memory(runner_function, args.num_shards, args.memory_constraint) > memory_constraint:
        print(f"Memory constraint not satisfied")
        exit(1)
    else:
        print(f"Memory constraint satisfied")


def save_model_weights(model_dir: str, model: nn.Module, shards: int):
    state_dict = model.state_dict()
    total_params = len(state_dict)
    layers_per_shard = total_params // shards

    if not os.path.exists(model_dir):
        os.mkdir(model_dir)

    for shard_id in range(shards):
        # Starting and ending indices for slicing the state_dict
        start = shard_id * layers_per_shard
        end = start + layers_per_shard if shard_id < shards - 1 else total_params

        # Slicing the state_dict to create a shard
        shard = {k: state_dict[k] for k in list(state_dict)[start:end]}
        save_file(filename=os.path.join(model_dir, f"shard_{shard_id}.safetensors"), tensors=shard)


def get_available_storage_devices():
    path = os.path.realpath(path)
    partitions = psutil.disk_partitions()

    for p in partitions:
        if os.path.commonpath([p.mountpoint, path]) == p.mountpoint:
            return p.device

    return None


def load_model_weights(storage_type: str):

    DEFAULT_TMP_DIR = "/tmp"

    if storage_type == "ssd":
        pass
    elif storage_type == "flash":
        pass


    elif storage_type == "hdd":
        pass


    else:
        raise ValueError(f"Storage type {storage_type} not supported")






# Create a Dense model and serealized his weights into shards. So that only 1 shard can be load into ram
# We are going to test how fast can be a model with limited memory in hardware if sharding the processes step by step

if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('--input_size', type=int, default=1000)
    argparser.add_argument('--hidden_layers', type=int, default=100)
    argparser.add_argument('--layer_width', type=int, default=200)
    argparser.add_argument('--output_size', type=int, default=1000)
    argparser.add_argument('--num_shards', type=int, default=10)
    argparser.add_argument('--memory_constraint', type=int, default=5)
    args = argparser.parse_args()

    model = DenseModel(input_size=args.input_size,output_size= args.output_size, hidden_layers=args.hidden_layers, layer_width = 100)
    save_model_weights(model_dir="/home/cesar/models", model=model, shards=args.num_shards)
    model_path = "/home/cesar/models"

    sharded_model = ShardedModel(model_path)

    for i in range(100):
        output = sharded_model(torch.randn(1, args.input_size))
        print(output.shape)
