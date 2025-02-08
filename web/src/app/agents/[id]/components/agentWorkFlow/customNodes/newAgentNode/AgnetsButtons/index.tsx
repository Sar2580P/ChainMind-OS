"use clinet";
import React from "react";
import { useContext, useState } from "react";
import AppContext from "@/contexts/AppContext";
import { Button } from "@/components/ui/button";
import LoadingComponent from "@/components/loading";
import usePostResponse from "@/hooks/usePostResponse";

const AgentsButtons = ({ id, agent_id }: { id: string; agent_id: string }) => {
  const [loading, setLoading] = useState({
    workPlanning: false,
    generateCode: false,
  });
  const { postResponse } = usePostResponse();
  const {
    agentCurrentNodeAndEdges,
    setAgentCurrentNodeAndEdgesHandler,
    setAgentDatasHandler,
    setDeployContractDataHandler,
  } = useContext(AppContext);
  const makeCodeArrayFromFiles = (files: string[]) => {
    return files.map((file) => {
      return {
        id: file,
        isActive: false,
        language: file.split(".").pop() || "sol",
        fileName: file,
        code: "",
        path: file,
      };
    });
  };

  const handleWorkPlanning = async () => {
    setLoading((loading) => ({ ...loading, workPlanning: true }));
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

      const codeFiles = makeCodeArrayFromFiles(response.files);
      const codeInstructions = response.code_instructions.map(
        (instruction: string) => {
          return instruction.substring(0, 45) + "...";
        }
      );
      setAgentDatasHandler(agent_id, "codes", codeFiles);
      setDeployContractDataHandler("files", [response.files]);
      setDeployContractDataHandler("code_instructions", [codeInstructions]);
    }
    setLoading((loading) => ({ ...loading, workPlanning: false }));
  };

  const handleGenerateCode = async () => {
    setLoading((loading) => ({ ...loading, generateCode: true }));
    const data = agentCurrentNodeAndEdges.Nodes.filter(
      (node) => node.id.toLowerCase() === id.toLowerCase()
    );
    const solution_code_design_list =
      data.length > 0 ? data[0].data.metadata : {};
    const response = await postResponse(
      { agent_id, solution_code_design_list },
      "leayer_3_generate_codebase"
    );
    setLoading((loading) => ({ ...loading, generateCode: false }));
    console.log(response);
  };

  return (
    <div className="flex justify-center align-middle gap-2 mt-2">
      <Button
        className="w-32"
        variant={"default"}
        onClick={handleWorkPlanning}
        style={{
          position: "relative",
        }}
        disabled={loading.workPlanning}
      >
        Work Planning
        <div className="absolute right-50 top-50">
          {loading.workPlanning && (
            <LoadingComponent
              height="20px"
              size="16px"
              width="50px"
              alignItems="center"
            />
          )}
        </div>
      </Button>
      <Button
        className="w-32"
        variant={"outline"}
        onClick={handleGenerateCode}
        style={{
          position: "relative",
        }}
        disabled={loading.generateCode}
      >
        Generate Code
        <div className="absolute right-50 top-50">
          {loading.generateCode && (
            <LoadingComponent
              height="20px"
              size="16px"
              width="50px"
              alignItems="center"
            />
          )}
        </div>
      </Button>
    </div>
  );
};

export default AgentsButtons;
