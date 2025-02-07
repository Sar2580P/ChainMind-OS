// SPDX-License-Identifier: MIT

pragma solidity ^0.8.8;

contract ChainMindOS {
    uint public aiAgentCount = 0;
    mapping(uint => AiAgent) public aiAgents;

    struct AiAgent {
        string id;
        address owner;
        string[] agentObjectives;
        string[] briefContextOnEachObjective;
        string[][] techExpertise;
        string[][] files;
        string[][] instructions;
    }

    function createAiAgent(
        string memory _id,
        string[] memory _agentObjectives,
        string[] memory _briefContextOnEachObjective,
        string[][] memory _techExpertise,
        string[][] memory _files,
        string[][] memory _instructions
    ) public {
        aiAgentCount++;
        aiAgents[aiAgentCount] = AiAgent(
            _id,
            msg.sender,
            _agentObjectives,
            _briefContextOnEachObjective,
            _techExpertise,
            _files,
            _instructions
        );
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

    function getAiAgentById(
        string memory _id
    ) public view returns (AiAgent memory) {
        for (uint i = 1; i <= aiAgentCount; i++) {
            if (
                keccak256(abi.encodePacked(aiAgents[i].id)) ==
                keccak256(abi.encodePacked(_id))
            ) {
                return aiAgents[i];
            }
        }
        return
            AiAgent(
                "",
                address(0),
                new string[](0),
                new string[](0),
                new string[][](0),
                new string[][](0),
                new string[][](0)
            );
    }

    function getAllAiAgents() public view returns (AiAgent[] memory) {
        AiAgent[] memory result = new AiAgent[](aiAgentCount);
        for (uint i = 1; i <= aiAgentCount; i++) {
            result[i - 1] = aiAgents[i];
        }
        return result;
    }
}
