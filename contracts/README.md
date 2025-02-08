# ChainMindOS Smart Contract

The **ChainMindOS** smart contract is designed to manage AI agents on the Ethereum blockchain. It enables users to:

- Create AI agents
- Retrieve agent details
- Manage agent data efficiently

The contract operates on **Ethereum** and has been deployed on **Sepolia** and **Arbitrum Sepolia** test networks using **Hardhat**.

## Contract Details

### State Variables

- **`uint public aiAgentCount`**: Tracks the total number of AI agents.
- **`mapping(uint => AiAgent) public aiAgents`**: Maps each AI agent ID to its corresponding details.

### Structs

The contract uses the `AiAgent` struct to represent AI agents with the following properties:

- **`string id`**: Unique identifier for the AI agent.
- **`address owner`**: Ethereum address of the agent's owner.
- **`string[] agentObjectives`**: The objectives assigned to the AI agent.
- **`string[] briefContextOnEachObjective`**: Brief description of each objective.
- **`string[][] techExpertise`**: Technical expertise required for the objectives.
- **`string[][] files`**: Associated files related to the AI agent.
- **`string[][] instructions`**: Instructions for the AI agent.

### Functions

- **`function createAiAgent(...) public`**: Creates a new AI agent.
- **`function getAiAgentCount() public view returns (uint)`**: Returns the total number of AI agents.
- **`function getAllAiAgentOfUser() public view returns (AiAgent[] memory)`**: Returns all AI agents owned by the caller.
- **`function getAiAgentById(string memory _id) public view returns (AiAgent memory)`**: Retrieves an AI agent by its unique ID.
- **`function getAllAiAgents() public view returns (AiAgent[] memory)`**: Returns all AI agents.

## Deployment

The **ChainMindOS** smart contract has been deployed on:

- **Ethereum Sepolia Testnet** : [0xA9049312D8fA2F42555AdCc04343F1B54c84AEc0](https://sepolia.etherscan.io/address/0xA9049312D8fA2F42555AdCc04343F1B54c84AEc0)
- **Arbitrum Sepolia Testnet** : [0x9221146c6900f72d5bcB5ba578ff4A738bE1165E](https://sepolia.arbiscan.io/address/0x9221146c6900f72d5bcB5ba578ff4A738bE1165E)

To deploy the contract using **Hardhat**, follow these steps:

### Prerequisites

Ensure you have **Node.js**, **Hardhat**, and required dependencies installed.

```sh
npm install
```

### Deploying to Sepolia and Arbitrum Sepolia

Run the following commands to deploy to the respective test networks:

```sh
npx hardhat run scripts/deploy.js --network sepolia
npx hardhat run scripts/deploy.js --network arbitrumsepolia
```

## Testing

To ensure the contract functions correctly, write test cases using **Hardhat and Mocha**.

### Running Tests

To execute tests, use the following command:

```sh
npx hardhat test
```

This will compile the contracts and run all defined test cases.
