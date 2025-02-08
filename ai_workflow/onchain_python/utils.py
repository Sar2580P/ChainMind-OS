import numpy as np
from typing import List
import yaml

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data
  
def get_q_table_size_mb(q_table: np.ndarray) -> float:
    """Get the size of the Q-table in MB."""
    return q_table.nbytes / (1024 * 1024)

def create_q_table(states_dim_tuples: List, action_count: int) -> np.ndarray:
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
    q_table_shape = tuple(states_dim_tuples) + (action_count,)

    # Initialize Q-table with zeros, dtype=int16 to save memory
    q_table = np.zeros(q_table_shape, dtype=np.int16)

    return q_table

def get_gas_fee(curr_price: float, floor: float, ceiling: float, congestion_factor: float = 1.0) -> float:
    """
    Simulates gas fees as a function of NFT price and market conditions, with proper scaling.

    Args:
        curr_price (float): Current price of the NFT.
        floor (float): Lower bound for gas fee scaling.
        ceiling (float): Upper bound for gas fee scaling.
        congestion_factor (float, optional): Multiplier for network congestion (default = 1.0).

    Returns:
        float: Scaled simulated gas fee.
    """
    # Normalize price impact on gas fee (scaled between 0 and 1)
    price_factor = np.clip((curr_price - floor) / (ceiling - floor), 0, 1)

    # Simulate network congestion (random variation)
    congestion = np.random.uniform(0.8, 1.5) * congestion_factor

    # Introduce market volatility (random fluctuations)
    volatility = np.random.uniform(-0.2, 0.2) * price_factor

    # Compute base and dynamic gas fees (scaled properly)
    base_fee = floor * 0.05  # 5% of floor price as minimum fee
    dynamic_fee = price_factor * (ceiling * 0.1)  # Up to 10% of ceiling price

    # Compute final gas fee with scaling
    gas_fee = (base_fee + dynamic_fee) * (1 + congestion + volatility)

    return round(max(gas_fee, base_fee), 4)  # Ensure minimum fee is dynamically adjusted

def get_current_rarity_volume(curr_volumes: np.ndarray, volatility: float = 0.1, 
                              shock_prob: float = 0.05) -> np.ndarray:
    """
    Simulates stochastic NFT trading volume dynamics.

    Args:
        curr_volumes (np.ndarray): Array of current NFT trading volumes.
        volatility (float): Controls the magnitude of normal fluctuations (default: 0.1).
        shock_prob (float): Probability of an extreme market event (default: 5%).

    Returns:
        np.ndarray: Updated volumes for each NFT.
    """
    # Market sentiment shift (global impact)
    sentiment_shift = np.random.uniform(0.9, 1.1)  

    # Normal volume fluctuations
    volume_fluctuation = np.random.uniform(1 - volatility, 1 + volatility, size=len(curr_volumes))

    # Trend persistence (momentum)
    trend_factor = np.random.uniform(0.95, 1.05, size=len(curr_volumes))  

    # Apply occasional large market shocks
    shock_multiplier = np.where(np.random.rand(len(curr_volumes)) < shock_prob,  
                                np.random.uniform(0.5, 1.5, size=len(curr_volumes)),  
                                1)

    # Compute new volumes
    new_volumes = curr_volumes * volume_fluctuation * trend_factor * sentiment_shift * shock_multiplier

    # Ensure non-negative volumes and round to integers
    return np.maximum(new_volumes, 0)

def discretize(value: float,ceil_value :float , floor_value :float , num_levels: int) -> int:
    """
    Discretizes a continuous value into a fixed number of levels.

    Args:
        value (float): The continuous value to discretize.
        num_levels (int): The number of discrete levels to use.

    Returns:
        int: The discretized value (between 0 and num_levels-1).
    """
    # Normalize the value between 0 and 1
    normalized_value = (value - floor_value) / (ceil_value - floor_value)
    # Discretize the normalized value
    return int(np.clip(normalized_value * num_levels, 0, num_levels - 1))

# config = read_yaml('ai_workflow/onchain_python/config.yaml')
# print(config['gas_fees_params'])