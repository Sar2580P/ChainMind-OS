"use client";
import configData from "@/config/config.json";
import { Button } from "@/components/ui/button";
import { useReadContract, useWriteContract } from "wagmi";
import { CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

const Buttons = ({ agent_id }: { agent_id: string }) => {
  const { data: agentDetails } = useReadContract({
    abi: configData.abi,
    address: configData.contractAddress.localhost as `0x${string}`,
    functionName: "getAllAiAgents",
    args: [],
  });
  console.log("BloackChain_agentDetails", agentDetails);
  const { writeContractAsync: writeContractAsyncDeployAgent } =
    useWriteContract();
  const handleDeployAgent = async () => {
    await writeContractAsyncDeployAgent(
      {
        abi: configData.abi,
        address: configData.contractAddress.localhost as `0x${string}`,
        functionName: "createAiAgent",
        args: [
          agent_id,
          ["fee payments"],
          ["To ensure transparency and automation in fee payments"],
          ["DeFi_expert", "DAO_expert"],
          [["contracts:dao:dao.sol", "contracts:interfaces:idao.sol"]],
          [
            [
              "Create a DAO contract in contracts:dao:dao.sol...",
              "Implement the idao interface in contracts:inte...",
            ],
          ],
        ],
      },
      {
        onSuccess: () => {
          console.log("Agent deployed successfully");
        },
      }
    );
  };

  return (
    <CardHeader className="flex flex-row align-middle justify-end sm:justify-between py-3">
      <div className="hidden sm:block">
        <CardTitle>
          Chat with Agent{" "}
          {agent_id.substring(0, 4) +
            "...." +
            agent_id.substring(agent_id.length - 4)}
        </CardTitle>
        <CardDescription>
          Chat with the agent to get more information about the work!
        </CardDescription>
      </div>
      <div className="flex flex-row space-x-2 text-gray-900">
        <Button
          onClick={() => {
            handleDeployAgent();
          }}
          variant="outline"
        >
          Deploy Agent
        </Button>
      </div>
    </CardHeader>
  );
};

export default Buttons;
