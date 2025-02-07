from tqdm import tqdm
from typing import List, Tuple, Dict
from ai_workflow.onchain_python.members import Buyer, Seller, NFTArtwork, NFT_MARKET
from ai_workflow.onchain_python.rl_updation_rule import learn, take_action
from ai_workflow.onchain_python.orchestrator import Orchestrator
from ai_workflow.onchain_python.utils import (create_q_table, get_gas_fee, read_yaml,
                                              get_current_rarity_volume)

def initialize_players(config:dict)-> Tuple[List[Buyer], List[Seller]]:
    buyers: List[Buyer] = []
    sellers: List[Seller] = []
    n_buyers , n_sellers = config['Num_buyers'], config['Num_sellers']
    for i in range(n_buyers):
        buyers.append(Buyer(**config["buyers_config"][i]))
        
    for i in range(n_sellers):
        c :Dict = config['sellers_config'][i]['NFT_config']
        nft = NFTArtwork(**c['NFT_params'])
        nft.SellerID = c['SellerID']
        c.pop('NFT_params')
        sellers.append(Seller(**c, nft=nft))
        
    return buyers, sellers

def train(config_path:str):
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
    config = read_yaml(config_path)
    # Initialize Q-tables for buyers and sellers
    sellers_q_table = [create_q_table(states_dim_tuples=config['state_dim_sellers'], 
                                      action_count=config['action_count_seller']) for _ in range(config['Num_sellers'])]
    buyers_q_table = [create_q_table(states_dim_tuples=config['state_dim_buyers'],
                                        action_count=config['action_count_buyer']) for _ in range(config['Num_buyers'])]

    train_config = config['train_params']
    for episode in tqdm(range(train_config['N_episodes']), desc="Training Progress"):
        # Initialize Sellers, Buyers, and NFTs
        config = read_yaml(config_path)
        buyers, sellers = initialize_players(config=config)

        # Register NFTs in the Market
        for seller in sellers:
            price = seller.nft.CurrPrice
            if price not in NFT_MARKET:
                NFT_MARKET[price] = []
            NFT_MARKET[price].append(seller.nft)
            
        gas_config = config['gas_fees_params']
        curr_gas_fees = gas_config['initial_gas_fees']
        
        vol_config = config['nft_volume_params']
        curr_nft_volume = vol_config['initial_nft_volumes']

        for step in range(train_config['Episode_length']):
            # Update gas fees
            curr_gas_fees = get_gas_fee(curr_price=curr_gas_fees, floor=gas_config['floor_gas_fees'], 
                                        ceiling=gas_config['ceiling_gas_fees'], congestion_factor=gas_config['congestion_factor'])
            curr_nft_volume = get_current_rarity_volume(curr_nft_volume, volatility=vol_config['volatility'], 
                                                        shock_prob=vol_config['shock_prob'])
            
            buyer_rewards , seller_rewards = {}, {}
            available_prices = list(NFT_MARKET.keys())
            for price in available_prices:
                nft_segment = NFT_MARKET.get(price, [])
                for nft in nft_segment:
                    seller:Seller = sellers[nft.SellerID]
                    
                    # Get the current state of the seller and buyers
                    curr_seller_state = seller.get_curr_state(gas_fees=curr_gas_fees, config=config)
                    curr_buyers_states = [buyer.get_curr_state(curr_gas_fees, nft.RarityScore , nft.CurrPrice, config) for buyer in buyers]
                    
                    # STEP-1 : let buyers take action
                    buyer_bids = [(take_action(buyers_q_table[buyer.BuyerID], curr_buyers_states[buyer.BuyerID],
                                               train_config['epsilon']), buyer) for buyer in buyers]
                    # STEP-2 : let owner of NFT take action(seller)
                    seller_action = take_action(sellers_q_table[nft.SellerID], curr_seller_state , train_config['epsilon'])
                    action_name, action_code = seller.get_action_name(seller_action)
                    action = {action_name: action_code}
                    # STEP-3 : interact via Orchestrator
                    rarity_volume = curr_nft_volume[nft.RarityScore]
                    rewards_buyers, reward_seller = Orchestrator.step(buyer_bids, seller, nft, action, 
                                                                      curr_gas_fees=curr_gas_fees, current_rarity_volume=rarity_volume)
                    
                    # STEP-4 : Update Q-tables using SARSA
                    for idx, (buyer, reward) in enumerate(zip(buyers, rewards_buyers)):
                        new_buyer_state = buyer.get_curr_state(curr_gas_fees, nft.RarityScore , nft.CurrPrice, config)
                        action_taken = buyer_bids[buyers.index(buyer)][0]
                        next_action = take_action(buyers_q_table[buyer.BuyerID], new_buyer_state, train_config['epsilon'])
                        learn(buyers_q_table[buyer.BuyerID], curr_buyers_states[idx] , action_taken, reward, new_buyer_state, 
                              next_action, train_config['alpha'], train_config['gamma'])
                        
                    # Update seller Q-table
                    action_taken = seller_action
                    new_seller_state = seller.get_curr_state(gas_fees=curr_gas_fees, config=config)
                    next_action = take_action(sellers_q_table[nft.SellerID], new_seller_state, train_config['epsilon'])
                    learn(sellers_q_table[nft.SellerID], curr_seller_state, action_taken, reward_seller, new_seller_state, next_action, 
                          train_config['alpha'], train_config['gamma'])
                    
                    # log rewards of the agents
                    seller_rewards['Seller_'+str(nft.SellerID)] = reward_seller
                    for idx, buyer in enumerate(buyers):
                        if 'Buyer_'+str(buyer.BuyerID) not in buyer_rewards:
                            buyer_rewards['Buyer_'+str(buyer.BuyerID)] = 0
                        buyer_rewards['Buyer_'+str(buyer.BuyerID)] += buyer.total_rewards_achieved
                        
            # Log the rewards of the agents
            seller_rewards_ = ", ".join([f"{k}: {v}" for k, v in seller_rewards.items()])
            buyer_rewards_ = ", ".join([f"{k}: {v}" for k, v in buyer_rewards.items()])
            print(f"Episode: {episode+1}, Step: {step+1}, {seller_rewards_}, {buyer_rewards_}")
            print("\t\t", f"Current Gas Fees: {curr_gas_fees}, Current NFT Volumes: {curr_nft_volume}")
        print(f"Episode {episode + 1}/{train_config['N_episodes']} completed", "_"*10)
        print("\n\n")
        
        
    print("Training completed!")

# if __name__=="__main__":
#     train(config_path='ai_workflow/onchain_python/config.yaml')
    