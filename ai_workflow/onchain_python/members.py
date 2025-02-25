from pydantic import BaseModel, Field
from sortedcontainers import SortedDict
from typing import Dict, Set, List, ClassVar
import random  # To simulate gas fee changes over time
import heapq
import numpy as np
from ai_workflow.onchain_python.utils import discretize

NFT_MARKET: Dict[int, List[BaseModel]] = {}

class Episode_Stats(BaseModel):
    episode_num: int = Field(..., ge=0, description="Episode number.")
    seller_rewards: Dict[str, List] = Field(default={}, description="Rewards earned by sellers.")
    buyer_rewards: Dict[str, List] = Field(default={}, description="Rewards earned by sellers.")
    gas_fees: List = Field(default=[] , description="Gas Fees variation")
    rarity_volume_traded: List[List] = Field(default=[] , description="Gas Fees variation")
    
    
class NFTArtwork(BaseModel):
    nft_artwork_id: int
    BasePrice: float = Field(..., gt=0, description="Original listing price of the NFT.")
    CurrPrice: float = Field(..., gt=0, description="Current market price of the NFT.")
    RarityScore: int = Field(..., ge=1, le=5, description="NFT rarity level (1-5).")
    TimeListed: int = Field(..., ge=0, description="Number of time-steps the NFT has been listed.")
    SellerID: int = Field(default=0, description="ID of the seller currently owning this NFT.")

    def update_price(self, new_price: float):
        """Update NFT price and maintain the global market listing."""
        old_price_str = f"{self.CurrPrice:.2f}"
        new_price_str = f"{new_price:.2f}"

        # Remove from old price entry (if it exists)
        if old_price_str in NFT_MARKET and self in NFT_MARKET[old_price_str]:
            NFT_MARKET[old_price_str].remove(self)  # Remove current NFT object
            if not NFT_MARKET[old_price_str]:  # Remove empty set
                del NFT_MARKET[old_price_str]

        # Update price
        self.CurrPrice = new_price

        # Add to new price entry
        if new_price_str not in NFT_MARKET:
            NFT_MARKET[new_price_str] = []
        NFT_MARKET[new_price_str].append(self)



class Seller(BaseModel):
    SellerID: int
    nft: NFTArtwork  # Link to the NFT owned
    pricing_variability_level: int = 5  # Default: 5 discrete levels
    max_percentage_change: float = 20.0  # Maximum percentage change (e.g., 20%)
    reward: float = 0.0  # Seller's reward (initially 0)

    def _get_random_percentage(self, idx: int) -> float:
        """Get a random percentage from the range corresponding to the given index (0-4)."""
        assert 0 <= idx < self.pricing_variability_level, "Invalid index for discretization."

        # Define percentage ranges for each discrete level
        min_percent = 1 + (idx * 4)  # 1%, 5%, 9%, 13%, 17%
        max_percent = min(min_percent + 3, self.max_percentage_change)  # Apply the max_percentage_change constraint

        return random.uniform(min_percent, max_percent)  # Pick a random % in range

    def increase_price(self, idx: int):
        """Increase price by a random percentage within the selected range."""
        percentage = self._get_random_percentage(idx)
        new_price = round(self.nft.CurrPrice * (1 + percentage / 100), 2)
        self.nft.update_price(new_price)

    def decrease_price(self, idx: int):
        """Decrease price by a random percentage within the selected range."""
        percentage = self._get_random_percentage(idx)
        new_price = round(self.nft.CurrPrice * (1 - percentage / 100), 2)
        self.nft.update_price(new_price)

    def update_reward(self, reward: float):
        """Update the seller's reward by adding the specified amount."""
        self.reward += reward
        
    def get_curr_state(self, gas_fees:float, config) -> np.ndarray:
        gas_discrete = discretize(gas_fees, config['gas_fees_params']['ceiling_gas_fees'], 
                                  config['gas_fees_params']['floor_gas_fees'], config['gas_fees_params']['n_bins'])
        
        discrete_config = config['seller_discretization_params']
        time_listed_discrete = discretize(self.nft.TimeListed, discrete_config['time_listed']['max'], 
                                          discrete_config['time_listed']['min'], discrete_config['time_listed']['n_bins'])
        rarity_score_discrete = discretize(self.nft.RarityScore, discrete_config['rarity_score']['max'],
                                             discrete_config['rarity_score']['min'], discrete_config['rarity_score']['n_bins'])
        curr_price_discrete = discretize(self.nft.CurrPrice, discrete_config['curr_price']['max'],
                                                discrete_config['curr_price']['min'], discrete_config['curr_price']['n_bins'])
        continuous_states = [gas_discrete, time_listed_discrete, rarity_score_discrete, curr_price_discrete]
        return np.array(continuous_states).astype(np.int8)
    
    def get_action_name(self, action: int) -> str:
        if action<5:
            return "increment", action
        elif action<10:
            return "decrement", action-5
        elif action==10:
            return "hold" , 1
        elif action==11:
            return "accept" , 1
        raise ValueError("Invalid action index provided.")



class Buyer(BaseModel):
    BuyerID: int
    AvailableFunds: float = Field(..., ge=0, description="Total funds available for purchase.")
    total_rewards_achieved: float = Field(default=0.0, description="Total rewards the buyer has accumulated.")
    max_percentage_decrease: ClassVar[float] = 10.0  # Class attribute
    
    # Max-heap to store NFTs as (-price, nft_object) for efficient access to the most expensive NFTs
    nft_track: List[BaseModel] = Field(default=[], description="Tracking nft")  # List of tuples (-price, nft_object)
    nft_art_ids: Set[int] = Field(default=set(), description="Set of NFT artwork IDs the buyer owns.")
        
    @classmethod
    def get_max_decrease(cls) -> float:
        return cls.max_percentage_decrease  # Accessing class variable
    
    @staticmethod
    def place_bid(nft_price , decrease_level:int):
        """Place a bid on the NFT by decreasing the price by a certain percentage."""
        # chunk the range of (1, max_decrease) into (decrease_level) equal parts
        # then select a random percentage from the selected chunk
        max_decrease = Buyer.get_max_decrease()
        min_percent = 1 + (decrease_level * (max_decrease) / 5)
        max_percent = min(min_percent + (max_decrease-1) / 5, max_decrease)
        percentage = random.uniform(min_percent, max_percent)
        bid_price = round(nft_price * (1 - percentage / 100), 2)
        return bid_price
        
    def get_action_name(self, action: int) -> str:
        if action<5:
            return "place_bid", action
        elif action==5:
            return "hold" , 1
        elif action==6:
            return "accept" , 1
        raise ValueError("Invalid action index provided.")
        
    def get_curr_state(self, gas_fees:float, rarityScore: int , current_price:float, config) -> np.ndarray:

        gas_discrete = discretize(gas_fees, config['gas_fees_params']['ceiling_gas_fees'], 
                                  config['gas_fees_params']['floor_gas_fees'], config['gas_fees_params']['n_bins'])
        
        seller_discrete_config = config['seller_discretization_params']
        rarity_score_discrete = discretize(rarityScore, seller_discrete_config['rarity_score']['max'],
                                             seller_discrete_config['rarity_score']['min'], seller_discrete_config['rarity_score']['n_bins'])
        curr_price_discrete = discretize(current_price, seller_discrete_config['curr_price']['max'],
                                                seller_discrete_config['curr_price']['min'], seller_discrete_config['curr_price']['n_bins'])
        
        buyer_discrete_config = config['buyer_discretization_params']
        available_funds_discrete = discretize(self.AvailableFunds, buyer_discrete_config['available_funds']['max'],
                                                buyer_discrete_config['available_funds']['min'], buyer_discrete_config['available_funds']['n_bins'])
        discrete_states = [gas_discrete, rarity_score_discrete, available_funds_discrete, curr_price_discrete]
        return np.array(discrete_states).astype(np.int8)

def calculate_seller_reward(seller:Seller, curr_gas_fees:float, transaction_occurred:bool, final_price:float=10)-> float:
    """Calculate the reward for the seller based on the transaction outcome."""
    if not transaction_occurred:
        # Reward the seller with a fraction of the current gas fees
        return -1e-5 * seller.nft.TimeListed  # 0.01% of the current gas fees as reward
    else:
        # Penalize the seller for not making a transaction
        return (final_price-seller.nft.BasePrice) - 1e-5 * seller.nft.TimeListed - 1e-3 * curr_gas_fees  - 1e-2 * seller.nft.RarityScore 

def calculate_buyer_reward(buyer_bid_price:float , curr_gas_fees, RarityScore, rarity_volume)-> float:
    resale_price = get_resale_price(RarityScore, rarity_volume)
    return (resale_price - buyer_bid_price) - 1e-3 * curr_gas_fees

def get_resale_price(RarityScore, rarity_volume):
    '''
    I want it as a function of rarityScore and the volume traded for that rarityScore...
    Volume traded can also be a simulation, like that of gas fees
    '''
    return 1e-5 * rarity_volume * RarityScore