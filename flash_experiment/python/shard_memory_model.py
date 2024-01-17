import torch
import torch.nn as nn
import argparse
import flash_experiment.python.benchmark as benchmark
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
    def __init__(self, weight_path: str):
        super(ShardedModel, self).__init__()
        self.weight_path = weight_path


    def forward(self, x):
        #Gradients are not saved  for reducing memory
        with torch.no_grad():
            temporal_output_tensor = x
            shard_id = 0
            for path in os.listdir(self.weight_path):
                with safe_open(os.path.join(self.weight_path, f"shard_{shard_id}.pt"), framework="pt", device="cpu") as f:
                    sharded_module = torch.load(f)
                    temporal_output_tensor = sharded_module(temporal_output_tensor)
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


def save_model_weights(model_dir: str, model: nn.Module, shards):
    layers = list(model.children())
    layers_per_shard = int(len(layers) / shards)
    sharded_layers = {
        f"shard{i}": nn.ModuleList(layers[i * layers_per_shard -1:  i * layers_per_shard ] )
        for i in range(1,shards+ 1 )
    }

    if not os.path.exists(model_dir):
        os.mkdir(model_dir)

    for shard_id, shard in sharded_layers.items():
        save_file(os.path.join(model_dir, f"shard_{shard_id}.pt"), shard, framework="pt")

    

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

    model = DenseModel(input_size=args.input_size, hidden_layers=args.hidden_layers, layer_width=args)
    