import numpy as np
from typing import Tuple

def learn(q_table: np.ndarray, prev_state: Tuple[int, ...], action: int, reward: float, 
          next_state: Tuple[int, ...], next_action: int, alpha: float = 0.1, gamma: float = 0.99):
    """
    Updates the Q-table using the SARSA algorithm.
    
    Parameters:
    - q_table (np.ndarray): The Q-table of the agent.
    - prev_state (Tuple[int, ...]): The previous state of the agent (multi-dimensional index).
    - action (int): The action taken at the previous state.
    - reward (float): The reward received at time-step t.
    - next_state (Tuple[int, ...]): The new state of the agent after taking the action.
    - next_action (int): The action chosen for the next state.
    - alpha (float): The learning rate (default: 0.1).
    - gamma (float): The discount factor (default: 0.99).
    
    Returns:
    - None (updates the Q-table in-place).
    """

    # Get current Q-value
    q_current = q_table[prev_state + (action,)]

    # Get next Q-value for the next state-action pair
    q_next = q_table[next_state + (next_action,)]

    # Compute SARSA update
    q_table[prev_state + (action,)] = q_current + alpha * (reward + gamma * q_next - q_current)
    
    return None


def take_action(q_table: np.ndarray, state: Tuple[int, ...], epsilon: float = 0.1) -> int:
    """
    Selects an action using the epsilon-greedy policy.
    
    Parameters:
    - q_table (np.ndarray): The Q-table, where the last axis corresponds to actions.
    - state (Tuple[int, ...]): The current state (multi-dimensional index).
    - epsilon (float): The probability of selecting a random action (default: 0.1).
    
    Returns:
    - action (int): The selected action.
    """
    num_actions = q_table.shape[-1]  # Last axis corresponds to action space

    if np.random.rand() < epsilon:
        # Exploration: Choose a random action
        return np.random.randint(num_actions)
    
    # Exploitation: Choose the action with the highest Q-value
    return np.argmax(q_table[state])

