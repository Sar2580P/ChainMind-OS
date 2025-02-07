const {
  time,
  loadFixture,
} = require("@nomicfoundation/hardhat-toolbox/network-helpers");
const { anyValue } = require("@nomicfoundation/hardhat-chai-matchers/withArgs");
const { expect } = require("chai");

describe("ChainMindOS", function () {
  let ChainMindOS, chainMindOS, owner;

  beforeEach(async function () {
    ChainMindOS = await hre.ethers.deployContract("ChainMindOS");
    chainMindOS = await ChainMindOS.waitForDeployment();
    [owner] = await hre.ethers.getSigners();
  });

  it("should create an AI Agent", async function () {
    await chainMindOS.createAiAgent(
      "agent1",
      ["objective1"],
      ["context1"],
      [["expertise1"]],
      [["file1"]],
      [["instruction1"]]
    );

    const agent = await chainMindOS.aiAgents(1);
    expect(agent.id).to.equal("agent1");
    expect(agent.owner).to.equal(owner.address);
  });

  it("should return the correct AI Agent count", async function () {
    await chainMindOS.createAiAgent(
      "agent1",
      ["objective1"],
      ["context1"],
      [["expertise1"]],
      [["file1"]],
      [["instruction1"]]
    );

    const count = await chainMindOS.getAiAgentCount();
    expect(count).to.equal(1);
  });

  it("should return all AI Agents of a user", async function () {
    await chainMindOS.createAiAgent(
      "agent1",
      ["objective1"],
      ["context1"],
      [["expertise1"]],
      [["file1"]],
      [["instruction1"]]
    );

    const agents = await chainMindOS.getAllAiAgentOfUser();
    expect(agents.length).to.equal(1);
    expect(agents[0].id).to.equal("agent1");
  });

  it("should return an AI Agent by ID", async function () {
    await chainMindOS.createAiAgent(
      "agent1",
      ["objective1"],
      ["context1"],
      [["expertise1"]],
      [["file1"]],
      [["instruction1"]]
    );

    const agent = await chainMindOS.getAiAgentById("agent1");
    expect(agent.id).to.equal("agent1");
  });

  it("should return all AI Agents", async function () {
    await chainMindOS.createAiAgent(
      "agent1",
      ["objective1"],
      ["context1"],
      [["expertise1"]],
      [["file1"]],
      [["instruction1"]]
    );

    await chainMindOS.createAiAgent(
      "agent2",
      ["objective2"],
      ["context2"],
      [["expertise2"]],
      [["file2"]],
      [["instruction2"]]
    );

    const agents = await chainMindOS.getAllAiAgents();
    expect(agents.length).to.equal(2);
    expect(agents[0].id).to.equal("agent1");
    expect(agents[1].id).to.equal("agent2");
  });
});
