import numpy as np
from typing import Tuple
import yaml

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data
  
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

def get_gas_fee(curr_price: float, floor: float, ceiling: float, congestion_factor: float = 1.0) -> float:
    """
    Simulates gas fees as a function of NFT price and market conditions.

    Args:
        curr_price (float): Current price of the NFT.
        support (float): Lower bound for gas fee scaling.
        ceiling (float): Upper bound for gas fee scaling.
        congestion_factor (float, optional): Multiplier for network congestion (default = 1.0).

    Returns:
        float: Simulated gas fee.
    """
    # Normalize price impact on gas fee
    price_factor = np.clip((curr_price - floor) / (ceiling - floor), 0, 1)

    # Simulate network congestion (random multiplier)
    congestion = np.random.uniform(0.8, 1.2) * congestion_factor

    # Introduce market volatility (random fluctuations)
    volatility = np.random.uniform(-0.05, 0.05)  # ±5% random noise

    # Compute gas fee
    base_fee = floor * 0.02  # 2% of support price as minimum fee
    dynamic_fee = price_factor * (ceiling * 0.05)  # Up to 5% of ceiling price
    gas_fee = base_fee + (dynamic_fee * congestion) + (dynamic_fee * volatility)

    return round(max(gas_fee, floor * 0.01), 4)  # Ensure minimum fee


def get_current_rarity_volume(curr_volumes: np.ndarray, volatility: float = 0.1, shock_prob: float = 0.05) -> np.ndarray:
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

