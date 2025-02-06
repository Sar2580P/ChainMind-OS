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
import classes from "./index.module.css";
import React, { useCallback } from "react";
import { useContext, useEffect } from "react";
import initialNodes from "./defaultData/Nodes";
import initialEdges from "./defaultData/Edges";
import AppContext from "@/contexts/AppContext";
import NewAgentNode from "./customNodes/newAgentNode";

const nodeTypes = {
  "new-agent": NewAgentNode,
};
const edgeTypes = {
  "custom-edge": CustomEdge,
};

const AgentWorkFlow = ({ agent_id }: { agent_id: string }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const { agentCurrentNodeAndEdges } = useContext(AppContext);

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

  useEffect(() => {
    if (agentCurrentNodeAndEdges.Nodes.length === 0) return;
    setNodes(agentCurrentNodeAndEdges.Nodes);
    setEdges(agentCurrentNodeAndEdges.Edges);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [agentCurrentNodeAndEdges.Nodes, agentCurrentNodeAndEdges.Edges]);

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
