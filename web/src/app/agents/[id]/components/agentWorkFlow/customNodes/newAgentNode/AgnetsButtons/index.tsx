"use clinet";
import React from "react";
import { useContext } from "react";
import AppContext from "@/contexts/AppContext";
import usePostResponse from "@/hooks/usePostResponse";
import { Button } from "@/components/ui/button";

const AgentsButtons = ({ id, agent_id }: { id: string; agent_id: string }) => {
  const { postResponse } = usePostResponse();
  const { agentCurrentNodeAndEdges, setAgentCurrentNodeAndEdgesHandler } =
    useContext(AppContext);

  const handleWorkPlanning = async () => {
    const response = await postResponse(
      { id, agent_id },
      "layer_2_agent_work_planning"
    );
    if (response) {
      const updatedNodes = agentCurrentNodeAndEdges.Nodes.map((node) => {
        if (node.id.toLowerCase() === id.toLowerCase()) {
          return {
            ...node,
            data: {
              ...node.data,
              metadata: response,
            },
          };
        }
        return node;
      });
      setAgentCurrentNodeAndEdgesHandler(
        updatedNodes,
        agentCurrentNodeAndEdges.Edges
      );
    }
  };

  const handleGenerateCode = async () => {
    const data = agentCurrentNodeAndEdges.Nodes.filter(
      (node) => node.id.toLowerCase() === id.toLowerCase()
    );
    const solution_code_design_list =
      data.length > 0 ? data[0].data.metadata : {};
    const response = await postResponse(
      { agent_id, solution_code_design_list },
      "leayer_3_generate_codebase"
    );
    console.log(response);
  };

  return (
    <div className="flex justify-center align-middle gap-2 mt-2">
      <Button className="w-32" variant={"default"} onClick={handleWorkPlanning}>
        Work Planning
      </Button>
      <Button className="w-32" variant={"outline"} onClick={handleGenerateCode}>
        Generate Code
      </Button>
    </div>
  );
};

export default AgentsButtons;
