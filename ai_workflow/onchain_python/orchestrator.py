import random
from typing import List, Tuple, Dict
from ai_workflow.onchain_python.members import Buyer, Seller, NFTArtwork
from ai_workflow.onchain_python.utils import (get_gas_price, calculate_buyer_reward, 
                                              calculate_seller_reward)

class Orchestrator:
    @staticmethod
    def step(buyers: List[Tuple[float, 'Buyer']], seller: 'Seller', 
             nft: 'NFTArtwork', action: Dict[str, int]) -> Tuple[List[float], float]:
                                                                
        """
        Simulates one step of interaction between a list of buyers and a seller for a particular NFT.

        Parameters:
        - buyers: List of tuples containing (bid_price, buyer_instance)
        - seller: Seller object
        - nft: NFTArtwork object
        - action: Dictionary containing seller's action:
          {"increment": value} | {"decrement": value} | {"hold": 1}

        Returns:
        - Tuple of buyer rewards (list), seller reward (float), updated NFT price (float)
        """
        
        # Fetch gas price
        gas_price = get_gas_price()

        # Initialize rewards
        buyer_rewards = []
        for _, buyer_instance in buyers:
            buyer_rewards.append(0.0)  
        seller_reward = 0.0

        # Handle Seller's "hold" action:
        if "hold" in action:
            seller_reward = calculate_seller_reward(seller, gas_price, False)
            seller.reward += seller_reward

            # No price change for "hold" action, no transaction happens
            return buyer_rewards, seller_reward

        # Handle Seller's "increase" or "decrease" actions:
        if "increment" in action:
            percentage_change = action["increment"]
            seller.increase_price(percentage_change)
        elif "decrement" in action:
            percentage_change = action["decrement"]
            seller.decrease_price(percentage_change)

        # Update NFT price after seller's action
        updated_price = nft.CurrPrice

        # Handle the buyers' bids
        max_bidder = None
        for idx, (bid_price, buyer_instance) in enumerate(buyers):
            if bid_price >= updated_price:
                if max_bidder is None or bid_price > max_bidder[0]:
                    max_bidder = (idx, bid_price, buyer_instance)

        if max_bidder:
            # Process the transaction with the highest bidder
            idx, buyer_bid_price, buyer_instance = max_bidder
            buyer_instance.AvailableFunds -= buyer_bid_price  # Deduct buyer funds
            buyer_reward = calculate_buyer_reward(buyer_instance, buyer_bid_price, gas_price, nft.RarityScore)
            buyer_rewards[idx] = buyer_reward
            seller_reward = calculate_seller_reward(seller, gas_price, True)

            # Update the market and reward (if needed)
            Orchestrator.update_market_state(nft)

        return buyer_rewards, seller_reward

    @staticmethod
    def update_market_state(buyer):
        """Update the market state after a transaction"""
        # Placeholder for updating global market (e.g., removing NFTs from the market)
        pass
