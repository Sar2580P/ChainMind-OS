"use client";
import { useContext } from "react";
import { useWriteContract } from "wagmi";
import configData from "@/config/config.json";
import AppContext from "@/contexts/AppContext";
import { Button } from "@/components/ui/button";
import { CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

const Buttons = ({ agent_id }: { agent_id: string }) => {
  const { deployContractData } = useContext(AppContext);

  const { writeContractAsync: writeContractAsyncDeployAgent } =
    useWriteContract();
  const handleDeployAgent = async () => {
    console.log("Deploying agent");
    console.log("Address : ", configData.contractAddress.sepolia);
    console.log(deployContractData);
    const brief_context_on_each_objective =
      deployContractData.brief_context_on_each_objective.map((item) =>
        item.substring(0, 32)
      );
    console.log(
      "brief_context_on_each_objective_contract",
      brief_context_on_each_objective
    );
    await writeContractAsyncDeployAgent(
      {
        abi: configData.abi,
        address: configData.contractAddress.sepolia as `0x${string}`,
        functionName: "createAiAgent",
        args: [
          agent_id,
          deployContractData.objectives,
          brief_context_on_each_objective,
          deployContractData.tech_experts_for_objectives,
          deployContractData.files,
          deployContractData.code_instructions,
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
