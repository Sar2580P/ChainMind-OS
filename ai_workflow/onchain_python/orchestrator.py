import random
from typing import List, Tuple, Dict
from ai_workflow.onchain_python.members import Buyer, Seller, NFTArtwork , calculate_buyer_reward, calculate_seller_reward

class Orchestrator:
    @staticmethod
    def step(buyers: List[Tuple[float, 'Buyer']], seller: 'Seller', 
             nft: 'NFTArtwork', action: Dict[str, int], 
             curr_gas_fees:float, current_rarity_volume:float) -> Tuple[List[float], float]:
                                                                
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
        
        # Initialize rewards
        buyer_rewards = []
        for _, buyer_instance in buyers:
            buyer_rewards.append(0.0)  
        seller_reward = 0.0

        # Handle Seller's "hold" action:
        if "hold" in action.keys():
            seller_reward = calculate_seller_reward(seller, curr_gas_fees, False)
            seller.reward += seller_reward

            # No price change for "hold" action, no transaction happens
            return buyer_rewards, seller_reward

        # Handle Seller's "increase" or "decrease" actions:
        elif "increment" in action:
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
            buyer_reward = calculate_buyer_reward(buyer_bid_price, curr_gas_fees, 
                                                  nft.RarityScore, current_rarity_volume)
            buyer_rewards[idx] = buyer_reward
            seller_reward = calculate_seller_reward(seller, curr_gas_fees, True , buyer_bid_price)

            # Update the market and reward (if needed)
            Orchestrator.update_market_state(nft)

        return buyer_rewards, seller_reward

    @staticmethod
    def update_market_state(buyer):
        """Update the market state after a transaction"""
        # Placeholder for updating global market (e.g., removing NFTs from the market)
        pass
