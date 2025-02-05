const hre = require("hardhat");

async function main() {
  const ChainMindOS = await hre.ethers.deployContract("ChainMindOS");
  await ChainMindOS.waitForDeployment();
  console.log(` deployed to ${ChainMindOS}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

// npx hardhat compile
// npx hardhat node
// npx hardhat run scripts/deploy.js --network localhost
