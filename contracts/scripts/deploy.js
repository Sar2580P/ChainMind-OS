const hre = require("hardhat");

async function main() {
  const ChainMindOS = await hre.ethers.deployContract("ChainMindOS");
  await ChainMindOS.waitForDeployment();
  console.log(ChainMindOS);
  const contractAddress = await ChainMindOS.getAddress();
  console.log(`Contract deployed to: ${contractAddress}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

// npx hardhat compile
// npx hardhat node
// npx hardhat run scripts/deploy.js --network localhost
