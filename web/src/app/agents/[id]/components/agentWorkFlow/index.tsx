"use client";
import {
  useNodesState,
  useEdgesState,
  addEdge,
  ReactFlow,
  Controls,
  MiniMap,
  Background,
  Connection,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import CustomEdge from "./customEdge";
import { useReadContract } from "wagmi";
import classes from "./index.module.css";
import React, { useCallback } from "react";
import { useContext, useEffect } from "react";
import configData from "@/config/config.json";
import initialNodes from "./defaultData/Nodes";
import initialEdges from "./defaultData/Edges";
import AppContext from "@/contexts/AppContext";
import NewAgentNode from "./customNodes/newAgentNode";
import { CreateNodeAndEdges } from "@/hooks/useCreateNodeAndEdges";

const nodeTypes = {
  "new-agent": NewAgentNode,
};
const edgeTypes = {
  "custom-edge": CustomEdge,
};

let call_only_once: number = 1;

const AgentWorkFlow = ({ agent_id }: { agent_id: string }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const {
    agentCurrentNodeAndEdges,
    setAgentCurrentNodeAndEdgesHandler,
    setAgentDatasHandler,
  } = useContext(AppContext);

  const onConnect = useCallback(
    (connection: Connection) => {
      const edge = {
        ...connection,
        id: `${new Date().getTime().toString()}`,
        type: "custom-edge",
      };
      setEdges((prevEdges) => addEdge({ ...edge, animated: true }, prevEdges));
    },
    [setEdges]
  );

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

  useEffect(() => {
    if (agentCurrentNodeAndEdges.Nodes.length === 0) return;
    setNodes(agentCurrentNodeAndEdges.Nodes);
    setEdges(agentCurrentNodeAndEdges.Edges);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [agentCurrentNodeAndEdges.Nodes, agentCurrentNodeAndEdges.Edges]);

  const { data: agentDetails } = useReadContract({
    abi: configData.abi,
    address: configData.contractAddress.localhost as `0x${string}`,
    functionName: "getAiAgentById",
    args: [agent_id],
  }) as {
    data: {
      id: string;
      agentObjectives: string[];
      briefContextOnEachObjective: string[];
      techExpertise: string[][];
      files: string[][];
      instructions: string[][];
    };
  };
  if (agentDetails) {
    console.log("BloackChain_agentDetails", agentDetails);
    if (agentDetails.agentObjectives.length !== 0) {
      const { Nodes, Edges } = CreateNodeAndEdges(
        {
          objectives: agentDetails.agentObjectives,
          brief_context_on_each_objective:
            agentDetails.briefContextOnEachObjective,
          tech_experts_for_objectives: agentDetails.techExpertise,
        },
        agent_id
      );
      console.log("BloackChain_agentDetails", Nodes, Edges);
      if (call_only_once++ == 1) {
        setAgentCurrentNodeAndEdgesHandler(Nodes, Edges);
        const codeFiles = makeCodeArrayFromFiles(agentDetails.files[0]);
        setAgentDatasHandler(agent_id, "codes", codeFiles);
      }
    }
  }

  return (
    <div className={classes["container"]} key={agent_id}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        panOnScroll
        selectionOnDrag
        minZoom={0.5}
        maxZoom={4}
        defaultViewport={{
          zoom: 0.8,
          x: 50,
          y: 0,
        }}
      >
        <Controls />
        <MiniMap />
        <Background gap={16} size={2} />
      </ReactFlow>
    </div>
  );
};

export default AgentWorkFlow;
