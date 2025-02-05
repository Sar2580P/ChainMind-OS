// SPDX-License-Identifier: MIT

pragma solidity ^0.8.8;

contract ChainMindOS {
    uint public aiAgentCount = 0;
    mapping(uint => AiAgent) public aiAgents;

    struct AiAgent {
        uint id;
        string name;
        address owner;
    }

    function createAiAgent(string memory _name) public {
        aiAgentCount++;
        aiAgents[aiAgentCount] = AiAgent(aiAgentCount, _name, msg.sender);
    }

    function getAiAgentCount() public view returns (uint) {
        return aiAgentCount;
    }

    function getAllAiAgentOfUser() public view returns (AiAgent[] memory) {
        AiAgent[] memory result = new AiAgent[](aiAgentCount);
        uint counter = 0;
        for (uint i = 1; i <= aiAgentCount; i++) {
            if (aiAgents[i].owner == msg.sender) {
                result[counter] = aiAgents[i];
                counter++;
            }
        }
        return result;
    }

    function updateAiAgentName(uint _id, string memory _name) public {
        AiAgent storage aiAgent = aiAgents[_id];
        require(
            aiAgent.owner == msg.sender,
            "You are not the owner of this AI Agent"
        );
        aiAgent.name = _name;
    }

    function getAiAgentById(uint _id) public view returns (AiAgent memory) {
        AiAgent memory aiAgent = aiAgents[_id];
        return aiAgent;
    }

    function getAllAiAgents() public view returns (AiAgent[] memory) {
        AiAgent[] memory result = new AiAgent[](aiAgentCount);
        for (uint i = 1; i <= aiAgentCount; i++) {
            result[i - 1] = aiAgents[i];
        }
        return result;
    }
}
