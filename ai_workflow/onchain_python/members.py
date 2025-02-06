from pydantic import BaseModel, Field
from sortedcontainers import SortedDict
from typing import Dict, Set
import random  # To simulate gas fee changes over time
import heapq
import random

NFT_MARKET: Dict[str, Set[BaseModel]] = {}

class NFTArtwork(BaseModel):
    nft_artwork_id: int
    BasePrice: float = Field(..., gt=0, description="Original listing price of the NFT.")
    CurrPrice: float = Field(..., gt=0, description="Current market price of the NFT.")
    RarityScore: int = Field(..., ge=1, le=5, description="NFT rarity level (1-5).")
    TimeListed: int = Field(..., ge=0, description="Number of time-steps the NFT has been listed.")
    SellerID: int = Field(..., description="ID of the seller currently owning this NFT.")

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
            NFT_MARKET[new_price_str] = set()
        NFT_MARKET[new_price_str].add(self)



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



class Buyer(BaseModel):
    BuyerID: int
    AvailableFunds: float = Field(..., ge=0, description="Total funds available for purchase.")
    total_rewards_achieved: float = Field(default=0.0, description="Total rewards the buyer has accumulated.")
    
    # Max-heap to store NFTs as (-price, nft_object) for efficient access to the most expensive NFTs
    nft_track_list: list = []  # List of tuples (-price, nft_object)

    def update_nft_track_list(self):
        """Update the track-list for affordable NFTs, maintaining it as a max-heap."""
        # Remove NFTs from track-list that are now out of the buyer's budget
        self.nft_track_list = [item for item in self.nft_track_list if item[0] <= -self.AvailableFunds]

        # Rebuild the heap by adding eligible NFTs that the buyer can afford
        for price, nft_set in NFT_MARKET.items():
            if price <= self.AvailableFunds:  # Check if the NFT is affordable
                for nft in nft_set:
                    heapq.heappush(self.nft_track_list, (-price, nft))  # Push each NFT with negated price for max-heap

        # Reheapify to maintain heap properties
        heapq.heapify(self.nft_track_list)

    def remove_nft_from_track_list(self, nft: NFTArtwork):
        """Remove an NFT from the track-list when it is bought or removed."""
        # Lazy removal by filtering out the NFT object from the heap
        self.nft_track_list = [item for item in self.nft_track_list if item[1] != nft]
        # Reheapify after removal to maintain heap properties
        heapq.heapify(self.nft_track_list)

    def buy_nft(self, nft: NFTArtwork, price: float, reward: float):
        """Buyer buys the NFT, decreases available funds, and updates total rewards."""
        if self.AvailableFunds >= price:
            # Decrease available funds after the purchase
            self.AvailableFunds -= price
            # Update total rewards
            self.total_rewards_achieved += reward
            # Remove NFT from the track-list since it was bought
            self.remove_nft_from_track_list(nft)
            # Also, remove the NFT from the global market listing
            NFT_MARKET[price].remove(nft)
            if not NFT_MARKET[price]:  # Clean up empty sets in nft_market
                del NFT_MARKET[price]
            return True  # Indicating successful purchase
        else:
            return False  # Not enough funds to buy the NFT

# Function to simulate gas fee changes over time
def get_gas_fees(curr_gas_fees:float):
    """Returns a simulated gas fee value (changes dynamically)."""
    return round(random.uniform(0.001, 0.02), 5)  # Simulated between 0.001 and 0.02 ETH
