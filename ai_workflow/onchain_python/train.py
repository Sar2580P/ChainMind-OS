from tqdm import tqdm
from typing import List
from ai_workflow.onchain_python.members import Buyer, Seller, NFTArtwork, NFT_MARKET
from ai_workflow.onchain_python.rl_updation_rule import learn, take_action
from ai_workflow.onchain_python.orchestrator import Orchestrator
from ai_workflow.onchain_python.utils import create_q_table

def initialize_players(config:dict):
    buyers: List[Buyer] = []
    sellers: List[Seller] = []
    n_buyers , n_sellers = config['Num_buyers'], config['Num_sellers']
    for i in range(n_buyers):
        buyers.append(Buyer(**config["buyers_config"][i]))
        
    for i in range(n_sellers):
        nft = NFTArtwork(**config["sellers_config"][i]['nft'])
        sellers.append(Seller(**config["sellers_config"][i], nft=nft))
        
    return buyers, sellers

def train(config:dict):
    """
    Trains buyers and sellers using SARSA with interactions via the Orchestrator.

    Parameters:
    - N_episodes (int): Total episodes to run.
    - Episode_length (int): Number of steps per episode.
    - Num_sellers (int): Number of sellers per episode.
    - Num_buyers (int): Number of buyers per episode.
    - epsilon (float): Epsilon for exploration in epsilon-greedy policy.
    - alpha (float): Learning rate for SARSA update.
    - gamma (float): Discount factor for future rewards.
    """
    
    # Initialize Q-tables for buyers and sellers
    sellers_q_table = [create_q_table(states_dict=config['state_dim_sellers'], 
                                      action_count=config['action_count_seller']) for _ in range(config['Num_sellers'])]
    buyers_q_table = [create_q_table(states_dict=config['state_dim_buyers'],
                                        action_count=config['action_count_buyer']) for _ in range(config['Num_buyers'])]

    train_config = config['train_params']
    for episode in tqdm(range(train_config['N_episodes']), desc="Training Progress"):
        # Initialize Sellers, Buyers, and NFTs
        buyers, sellers = initialize_players(config=config)

        # Register NFTs in the Market
        for seller in sellers:
            price = seller.nft.CurrPrice
            if price not in NFT_MARKET:
                NFT_MARKET[price] = set()
            NFT_MARKET[price].add(seller.nft)

        for step in range(train_config['Episode_length']):
            for price, nft_segment in NFT_MARKET.items():
                for nft in nft_segment:
                    
                    # STEP-1 : let buyers take action
                    buyer_bids = [(take_action(buyers_q_table, buyer.get_state(),
                                               train_config['epsilon']), buyer) for buyer in buyers]
                    # STEP-2 : let owner of NFT take action(seller)
                    seller = sellers[nft.SellerID]
                    seller_action = take_action(sellers_q_table[nft.SellerID], seller.get_state() , train_config['epsilon'])
                    action_name = ...
                    action = {action_name: seller_action}
                    # STEP-3 : interact via Orchestrator
                    rewards_buyers, reward_seller = Orchestrator.step(buyer_bids, seller, nft, action)
                    
                    # STEP-4 : Update Q-tables using SARSA
                    for buyer, reward in zip(buyers, rewards_buyers):
                        new_state = buyer.get_state()
                        action_taken = buyer_bids[buyers.index(buyer)][0]
                        next_action = take_action(buyers_q_table, new_state, train_config['epsilon'])
                        learn(buyers_q_table, buyer.prev_state() , action_taken, reward, new_state, 
                              next_action, train_config['alpha'], train_config['gamma'])
                        
                    # Update seller Q-table
                    prev_state = seller.prev_state()
                    action_taken = list(action.keys())[0]
                    new_state = seller.get_state()
                    next_action = take_action(sellers_q_table[nft.SellerID], new_state, train_config['epsilon'])
                    learn(sellers_q_table[nft.SellerID], prev_state, action_taken, reward_seller, new_state, next_action, 
                          train_config['alpha'], train_config['gamma'])
        print(f"Episode {episode + 1}/{train_config['N_episodes']} completed")

    print("Training completed!")
