from shard_memory_model import DenseModel
from flash_experiment.python.benchmark import measure_memory, measure_time_usage, measure_disk_usage, measure_temperature

if __name__ == '__main__':
    model = DenseModel(input_size=1000, hidden_layers=100)
    sharded_model = ShardedModel(model, num_shards=10, memory_constraint=5)



    print("")