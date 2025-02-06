import numpy as np
from typing import Tuple

def get_q_table_size_mb(q_table: np.ndarray) -> float:
    """Get the size of the Q-table in MB."""
    return q_table.nbytes / (1024 * 1024)

def create_q_table(states_dim_tuples: Tuple, action_count: int) -> np.ndarray:
    """
    Create and initialize the Q-table for an agent with separate state dimensions and actions in the last dimension.

    Args:
    - states_dict (dict): Dictionary containing state indices (key) and state dimensions (value).
      Example: {0: 3, 1: 4, 2: 2} means state_idx 0 has state_dim 3, state_idx 1 has state_dim 4, and so on.
    - action_count (int): Number of available actions for the agent.

    Returns:
    - np.ndarray: Initialized Q-table with shape (state_dim_1, state_dim_2, ..., state_dim_n, action_count), dtype=np.int16.
    """
    # Create a tuple of state dimensions followed by action count
    q_table_shape = states_dim_tuples + (action_count,)

    # Initialize Q-table with zeros, dtype=int16 to save memory
    q_table = np.zeros(q_table_shape, dtype=np.int16)

    return q_table

def get_gas_price():
  pass

def calculate_seller_reward():
  pass

def calculate_buyer_reward():
  pass

# # Define states dictionary and action count
# states_dict = {0: 10, 1: 5, 2: 5, 3:10}  # Example state dimensions
# action_count = 12  # Example action count

# # Create Q-table
# q_table = create_q_table(states_dict, action_count)

# # Calculate the size of the Q-table in MB
# q_table_size_mb = get_q_table_size_mb(q_table)

# print(f"The size of the Q-table is: {q_table_size_mb:.6f} MB")


import yaml
def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data
  
config = read_yaml("ai_workflow/onchain_python/config.yaml")
print(config['sellers_config'][0]['NFT_config'])
