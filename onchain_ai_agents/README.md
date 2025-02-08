# 🏆 **On-Chain NFT Market Simulation with Agentic AI**

## 📌 **Overview**

This project implements an **on-chain NFT market simulation** where autonomous agents (buyers and sellers) interact in a decentralized marketplace. The agents use **online reinforcement learning** (SARSA) to dynamically adjust their trading strategies based on past interactions. The **gas fees** are modeled as a **stochastic process**, adding realism to the market dynamics.

Unlike traditional AI models that rely on external LLM APIs, this simulation is **fully on-chain**, ensuring trustless, decentralized decision-making by agentic AI. The entire codebase is written in **Rust**, leveraging its efficiency and safety features for blockchain development.

---

## 🏛️ **Key Components**

### 🎭 **Agents**

- **Sellers**: List NFTs with attributes such as rarity, price, and time listed.
- **Buyers**: Evaluate and purchase NFTs based on their learned policies.
- **Learning**: Agents update their strategies **in real time** using SARSA reinforcement learning.

### 🎨 **NFT Model**

Each NFT is represented with multiple attributes:

- 🏆 **RarityScore**: Determines the uniqueness and desirability.
- 💰 **CurrPrice**: The current price set by the seller.
- ⏳ **TimeListed**: The duration the NFT has been available.
- 🔥 **BasePrice**: The initial listing price.

### ⛽ **Gas Fees as a Stochastic Process**

- **Gas fees** fluctuate randomly based on a predefined stochastic model.
- **Agents adjust** their bidding and listing strategies in response to gas fees, making the simulation more realistic.

---

## 📖 **SARSA Learning Algorithm**

Each agent updates its **Q-value** using the **SARSA (State-Action-Reward-State-Action) algorithm**:

<h3>🔄 SARSA Update Rule</h3>

<p>In our reinforcement learning implementation, we utilize the <b>SARSA (State-Action-Reward-State-Action)</b> algorithm, which updates the Q-value as follows:</p>

<p>
  <math xmlns="http://www.w3.org/1998/Math/MathML">
    <mi>Q</mi><mo>(</mo><mi>s</mi><mo>,</mo><mi>a</mi><mo>)</mo> 
    <mo>&#x2190;</mo>
    <mi>Q</mi><mo>(</mo><mi>s</mi><mo>,</mo><mi>a</mi><mo>)</mo>
    <mo>+</mo>
    <mi>&alpha;</mi> 
    <mo>[</mo>
    <mi>r</mi> <mo>+</mo> <mi>&gamma;</mi> <mi>Q</mi><mo>(</mo><mi>s'</mi><mo>,</mo><mi>a'</mi><mo>)</mo> 
    <mo>-</mo> 
    <mi>Q</mi><mo>(</mo><mi>s</mi><mo>,</mo><mi>a</mi><mo>)</mo> 
    <mo>]</mo>
  </math>
</p>

<h4>Where:</h4>
<ul>
  <li><b>Q(s,a)</b> → Current Q-value for state <i>s</i> and action <i>a</i></li>
  <li><b>&alpha;</b> → Learning rate</li>
  <li><b>r</b> → Reward received after taking action <i>a</i></li>
  <li><b>&gamma;</b> → Discount factor for future rewards</li>
  <li><b>Q(s',a')</b> → Q-value of the next state-action pair</li>
</ul>

<p>This equation ensures that the agent updates its policy based on the next action it selects, making SARSA an <b>on-policy</b> algorithm. 🚀</p>

Where:

- **s** = current state (e.g., NFT attributes, market conditions)
- **a** = chosen action (e.g., buying, listing price adjustment)
- **r** = reward received (e.g., profit/loss)
- **s'** = next state
- **a'** = next action chosen
- **α (alpha)** = learning rate
- **γ (gamma)** = discount factor for future rewards

---

## 🚀 **Features**

- ✅ **Decentralized & Fully On-Chain** – No reliance on external AI models.

- ✅ **Dynamic Agent Behavior** – Agents evolve their strategies over time.

- ✅ **Realistic Market Conditions** – Gas fees vary stochastically.

- ✅ **NFT Valuation Strategy** – Buyers and sellers evaluate NFTs based on learned policies.

- ✅ **Fully Implemented in Rust** – Ensures performance, safety, and seamless blockchain integration.

---

## 🔧 **Installation & Setup**

- Deploy the smart contracts on an EVM-compatible blockchain.

- Initialize agent parameters and NFT attributes.

- Run the simulation and observe the evolving market dynamics.

---

## 📊 **Future Enhancements**

- 🎯 Incorporating more complex agent strategies.

- 📈 Introducing more NFT attributes (e.g., historical trading data).

- 🌍 Enabling cross-chain NFT market interactions.

- 🤖 Exploring additional reinforcement learning algorithms.

---

## 🏁 **Conclusion**

This project pioneers an **on-chain, agent-based NFT market** where **self-learning AI** dynamically interacts within a decentralized ecosystem. By integrating **SARSA reinforcement learning** and **stochastic gas fee modeling**, we create an intelligent, evolving marketplace for NFTs. 🚀

With Rust powering the entire implementation, the system benefits from high performance, memory safety, and robust blockchain compatibility.
