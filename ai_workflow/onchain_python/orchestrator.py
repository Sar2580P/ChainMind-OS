import random
from typing import List, Tuple, Dict
from ai_workflow.onchain_python.members import Buyer, Seller, NFTArtwork , calculate_buyer_reward, calculate_seller_reward
import numpy as np

class Orchestrator:
    @staticmethod
    def step(buyers: List['Buyer'], buyer_action: List, seller: 'Seller', 
             nft: 'NFTArtwork', seller_action: Dict[str, int], 
             curr_gas_fees:float, current_rarity_volume:float) -> Tuple[List[float], float]:
        # STEP-1 : Let the seller take the action first
        nft.TimeListed += 1
        buyers_rewards = np.zeros(len(buyers))
        if "increase" in seller_action:
            level = seller_action["increase"]
            seller.increase_price(level)
        elif "decrease" in seller_action:
            level = seller_action["decrease"]
            seller.decrease_price(level)
        elif "hold" in seller_action:
            return buyers_rewards, calculate_seller_reward(seller, curr_gas_fees, False) ,False
        
        # STEP-2 : Let the buyers take the action
        best_buyer_idx, best_bid = -1, nft.CurrPrice
        
        for idx, (buyer, action) in enumerate(zip(buyers, buyer_action)):
            print(action, "**************")
            action_name, action_value = list(action.items())[0]
            if action_name=="hold":
                continue
            elif action_name=="place_bid":
                bid_price = Buyer.place_bid(nft.CurrPrice, action_value)
                if bid_price > best_bid and bid_price <= buyer.AvailableFunds:
                    best_buyer_idx, best_bid = idx, bid_price
            elif action_name=="buy":
                if nft.CurrPrice <= buyer.AvailableFunds and best_buyer_idx==-1:
                    best_buyer_idx = idx
            
        # STEP-3 : Process the transaction
        if best_buyer_idx != -1:
            buyer = buyers[best_buyer_idx]
            buyer.AvailableFunds -= best_bid
            buyer_reward = calculate_buyer_reward(best_bid, curr_gas_fees, nft.RarityScore, current_rarity_volume)
            buyers_rewards[best_buyer_idx] = buyer_reward
            seller_reward = calculate_seller_reward(seller, curr_gas_fees, True, best_bid)
            return buyers_rewards, seller_reward, True
                    
        else: 
            seller_reward = calculate_seller_reward(seller, curr_gas_fees, False)
            return buyers_rewards, seller_reward, False
        
        