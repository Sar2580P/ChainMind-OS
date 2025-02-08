use serde::{ Deserialize, Serialize };
use rand::prelude::*;
use std::collections::HashMap;
use ordered_float::OrderedFloat;
use rand::Rng;
use std::collections::{ HashSet, BinaryHeap };
use std::cmp::Reverse;

#[derive(Debug, Serialize, Deserialize)]
pub struct TrainParams {
    pub episode_length: u32,
    pub n_episodes: u32,
    pub epsilon: f64,
    pub alpha: f64,
    pub gamma: f64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct DiscretizationParams {
    pub min: f64,
    pub max: f64,
    pub n_bins: u32,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct SellerDiscretizationParams {
    pub curr_price: DiscretizationParams,
    pub rarity_score: DiscretizationParams,
    pub time_listed: DiscretizationParams,
    pub pricing_variability_level: DiscretizationParams,
    pub max_percentage_change: DiscretizationParams,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct BuyerDiscretizationParams {
    pub available_funds: DiscretizationParams,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct GasFeesParams {
    pub initial_gas_fees: f64,
    pub ceiling_gas_fees: f64,
    pub floor_gas_fees: f64,
    pub congestion_factor: f64,
    pub n_bins: u32,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct NFTVolumeParams {
    pub initial_nft_volumes: Vec<u32>,
    pub volatility: f64,
    pub shock_prob: f64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct BuyerConfig {
    pub buyer_id: u32,
    pub available_funds: u32,
    pub total_rewards_achieved: u32,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct NFTParams {
    pub nft_artwork_id: u32,
    pub base_price: u32,
    pub curr_price: u32,
    pub rarity_score: u32,
    pub time_listed: u32,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct NFTConfig {
    pub nft_params: NFTParams,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct SellerConfig {
    pub nft_config: NFTConfig,
    pub seller_id: u32,
    pub pricing_variability_level: u32,
    pub max_percentage_change: u32,
    pub reward: u32,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Config {
    pub train_params: TrainParams,
    pub action_count_buyer: u32,
    pub action_count_seller: u32,
    pub seller_discretization_params: SellerDiscretizationParams,
    pub buyer_discretization_params: BuyerDiscretizationParams,
    pub gas_fees_params: GasFeesParams,
    pub nft_volume_params: NFTVolumeParams,
    pub state_dim_sellers: Vec<u32>,
    pub state_dim_buyers: Vec<u32>,
    pub num_sellers: u32,
    pub num_buyers: u32,
    pub buyers_config: Vec<BuyerConfig>,
    pub sellers_config: Vec<SellerConfig>,
}

impl Config {
    pub fn new() -> Config {
        Config {
            train_params: TrainParams {
                episode_length: 50,
                n_episodes: 2,
                epsilon: 0.1,
                alpha: 0.1,
                gamma: 0.99,
            },
            action_count_buyer: 7,
            action_count_seller: 12,
            seller_discretization_params: SellerDiscretizationParams {
                curr_price: DiscretizationParams { min: 0.0, max: 100.0, n_bins: 5 },
                rarity_score: DiscretizationParams { min: 1.0, max: 5.0, n_bins: 5 },
                time_listed: DiscretizationParams { min: 0.0, max: 100.0, n_bins: 5 },
                pricing_variability_level: DiscretizationParams { min: 0.0, max: 5.0, n_bins: 5 },
                max_percentage_change: DiscretizationParams { min: 1.0, max: 20.0, n_bins: 5 },
            },
            buyer_discretization_params: BuyerDiscretizationParams {
                available_funds: DiscretizationParams { min: 0.0, max: 100.0, n_bins: 5 },
            },
            gas_fees_params: GasFeesParams {
                initial_gas_fees: 1.4,
                ceiling_gas_fees: 4.0,
                floor_gas_fees: 1.4,
                congestion_factor: 0.1,
                n_bins: 5,
            },
            nft_volume_params: NFTVolumeParams {
                initial_nft_volumes: vec![4000, 880, 10000, 800, 90],
                volatility: 0.07,
                shock_prob: 0.03,
            },
            state_dim_sellers: vec![5, 5, 5, 5],
            state_dim_buyers: vec![5, 5, 5, 5],
            num_sellers: 2,
            num_buyers: 2,
            buyers_config: vec![
                BuyerConfig {
                    buyer_id: 0,
                    available_funds: 57,
                    total_rewards_achieved: 0,
                },
                BuyerConfig {
                    buyer_id: 1,
                    available_funds: 86,
                    total_rewards_achieved: 0,
                }
            ],
            sellers_config: vec![
                SellerConfig {
                    nft_config: NFTConfig {
                        nft_params: NFTParams {
                            nft_artwork_id: 0,
                            base_price: 64,
                            curr_price: 64,
                            rarity_score: 3,
                            time_listed: 0,
                        },
                    },
                    seller_id: 0,
                    pricing_variability_level: 5,
                    max_percentage_change: 10,
                    reward: 0,
                },
                SellerConfig {
                    nft_config: NFTConfig {
                        nft_params: NFTParams {
                            nft_artwork_id: 1,
                            base_price: 78,
                            curr_price: 78,
                            rarity_score: 4,
                            time_listed: 0,
                        },
                    },
                    seller_id: 1,
                    pricing_variability_level: 5,
                    max_percentage_change: 10,
                    reward: 0,
                }
            ],
        }
    }
}

pub fn get_q_table_size_mb<T>(q_table: &[T]) -> f64 {
    (std::mem::size_of_val(q_table) as f64) / (1024.0 * 1024.0)
}

pub fn get_gas_fee(curr_price: f64, floor: f64, ceiling: f64, congestion_factor: f64) -> f64 {
    let mut rng = rand::thread_rng();
    let price_factor = ((curr_price - floor) / (ceiling - floor)).clamp(0.0, 1.0);
    let congestion: f64 = rng.gen_range(0.8..1.2) * congestion_factor;
    let volatility: f64 = rng.gen_range(-0.05..0.05);
    let base_fee = floor * 0.02;
    let dynamic_fee = price_factor * (ceiling * 0.05);
    let gas_fee = base_fee + dynamic_fee * congestion + dynamic_fee * volatility;
    (gas_fee.max(floor * 0.01) * 10_000.0).round() / 10_000.0
}

pub fn create_q_table(states_dim: &[usize], action_count: usize) -> Vec<Vec<i16>> {
    let state_space_size: usize = states_dim.iter().product();
    vec![vec![0; action_count]; state_space_size]
}

pub fn get_current_rarity_volume(
    curr_volumes: &Vec<f64>,
    volatility: f64,
    shock_prob: f64
) -> Vec<f64> {
    let mut rng = thread_rng();
    let sentiment_shift: f64 = rng.gen_range(0.9..=1.1);
    curr_volumes
        .iter()
        .map(|&vol| {
            let volume_fluctuation = rng.gen_range(1.0 - volatility..=1.0 + volatility);
            let trend_factor = rng.gen_range(0.95..=1.05);
            let shock_multiplier = if rng.gen::<f64>() < shock_prob {
                rng.gen_range(0.5..=1.5)
            } else {
                1.0
            };
            (vol * volume_fluctuation * trend_factor * sentiment_shift * shock_multiplier).max(0.0)
        })
        .collect()
}

pub fn discretize(value: f64, ceil_value: f64, floor_value: f64, num_levels: usize) -> usize {
    let normalized_value = (value - floor_value) / (ceil_value - floor_value);
    (normalized_value * (num_levels as f64)).clamp(0.0, (num_levels - 1) as f64) as usize
}

pub fn learn(
    q_table: &mut Vec<Vec<f64>>,
    prev_state: usize,
    action: usize,
    reward: f64,
    next_state: usize,
    next_action: usize,
    alpha: f64,
    gamma: f64
) {
    let q_current = q_table[prev_state][action];
    let q_next = q_table[next_state][next_action];
    q_table[prev_state][action] += alpha * (reward + gamma * q_next - q_current);
}

pub fn take_action(q_table: &Vec<Vec<f64>>, state: usize, epsilon: f64) -> usize {
    let mut rng = thread_rng();
    let num_actions = q_table[0].len();

    if rng.gen::<f64>() < epsilon {
        rng.gen_range(0..num_actions)
    } else {
        q_table[state]
            .iter()
            .enumerate()
            .max_by(|a, b| a.1.partial_cmp(b.1).unwrap())
            .map(|(idx, _)| idx)
            .unwrap_or(0)
    }
}

#[derive(Debug, Serialize, Deserialize)]
struct EpisodeStats {
    episode_num: usize,
    seller_rewards: HashMap<String, Vec<f64>>,
    buyer_rewards: HashMap<String, Vec<f64>>,
    gas_fees: Vec<f64>,
    rarity_volume_traded: Vec<Vec<f64>>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct NFTArtwork {
    nft_artwork_id: usize,
    base_price: f64,
    curr_price: f64,
    rarity_score: u8,
    time_listed: usize,
    seller_id: usize,
}

impl NFTArtwork {
    pub fn update_price(
        &mut self,
        new_price: f64,
        nft_market: &mut HashMap<String, Vec<NFTArtwork>>
    ) {
        let old_price_str = format!("{:.2}", self.curr_price);
        let new_price_str = format!("{:.2}", new_price);
        if let Some(nfts) = nft_market.get_mut(&old_price_str) {
            nfts.retain(|nft| nft.nft_artwork_id != self.nft_artwork_id);
            if nfts.is_empty() {
                nft_market.remove(&old_price_str);
            }
        }
        self.curr_price = new_price;
        nft_market.entry(new_price_str).or_insert_with(Vec::new).push(self.clone());
    }
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct Seller {
    seller_id: usize,
    nft: NFTArtwork,
    pricing_variability_level: usize,
    max_percentage_change: f64,
    reward: f64,
}

impl Seller {
    pub fn get_random_percentage(&self, idx: usize) -> f64 {
        assert!(idx < self.pricing_variability_level, "Invalid index for discretization.");

        let min_percent = 1.0 + (idx as f64) * 4.0;
        let max_percent = (min_percent + 3.0).min(self.max_percentage_change);

        rand::thread_rng().gen_range(min_percent..=max_percent)
    }

    pub fn increase_price(
        &mut self,
        idx: usize,
        nft_market: &mut HashMap<String, Vec<NFTArtwork>>
    ) {
        let percentage = self.get_random_percentage(idx);
        let new_price = (self.nft.curr_price * (1.0 + percentage / 100.0)).round();
        self.nft.update_price(new_price, nft_market);
    }

    pub fn decrease_price(
        &mut self,
        idx: usize,
        nft_market: &mut HashMap<String, Vec<NFTArtwork>>
    ) {
        let percentage = self.get_random_percentage(idx);
        let new_price = (self.nft.curr_price * (1.0 - percentage / 100.0)).round();
        self.nft.update_price(new_price, nft_market);
    }

    pub fn update_reward(&mut self, reward: f64) {
        self.reward += reward;
    }

    pub fn get_action_name(action: usize) -> (&'static str, usize) {
        match action {
            0..=4 => ("increment", action),
            5..=9 => ("decrement", action - 5),
            10 => ("hold", 1),
            11 => ("accept", 1),
            _ => panic!("Invalid action index provided."),
        }
    }
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct Buyer {
    buyer_id: usize,
    available_funds: f64,
    total_rewards_achieved: f64,
    nft_track: BinaryHeap<Reverse<(OrderedFloat<f64>, usize)>>, // Max-heap of NFTs as (-price, nft_id)
    nft_art_ids: HashSet<usize>,
}

impl Buyer {
    const MAX_PERCENTAGE_DECREASE: f64 = 10.0; // Class variable

    fn get_max_decrease() -> f64 {
        Self::MAX_PERCENTAGE_DECREASE
    }

    fn place_bid(nft_price: f64, decrease_level: usize) -> f64 {
        let max_decrease = Self::get_max_decrease();
        let min_percent = 1.0 + ((decrease_level as f64) * max_decrease) / 5.0;
        let max_percent = (min_percent + (max_decrease - 1.0) / 5.0).min(max_decrease);
        let percentage = rand::thread_rng().gen_range(min_percent..=max_percent);
        (nft_price * (1.0 - percentage / 100.0)).round()
    }

    fn get_action_name(action: usize) -> (&'static str, usize) {
        match action {
            0..=4 => ("place_bid", action),
            5 => ("hold", 1),
            6 => ("accept", 1),
            _ => panic!("Invalid action index provided."),
        }
    }
}

pub fn calculate_seller_reward(
    time_listed: f64,
    base_price: f64,
    rarity_score: f64,
    curr_gas_fees: f64,
    transaction_occurred: bool,
    final_price: f64
) -> f64 {
    if !transaction_occurred {
        return -1e-5 * time_listed;
    } else {
        return (
            final_price -
            base_price -
            1e-5 * time_listed -
            1e-3 * curr_gas_fees -
            1e-2 * rarity_score
        );
    }
}

pub fn calculate_buyer_reward(
    buyer_bid_price: f64,
    curr_gas_fees: f64,
    rarity_score: f64,
    rarity_volume: f64
) -> f64 {
    let resale_price = get_resale_price(rarity_score, rarity_volume);
    return resale_price - buyer_bid_price - 1e-3 * curr_gas_fees;
}

pub fn get_resale_price(rarity_score: f64, rarity_volume: f64) -> f64 {
    1e-5 * rarity_volume * rarity_score
}

fn main() {
    let config = Config::new();
    let _serialized = serde_json::to_string(&config).unwrap();
    println!("{}", "Code compiled successfully!");
}
