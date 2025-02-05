"use client";
import "@xyflow/react/dist/style.css";
import CustomEdge from "./customEdge";
import classes from "./index.module.css";
import React, { useCallback } from "react";
import initialNodes from "./defaultData/Nodes";
import initialEdges from "./defaultData/Edges";
import NewAgentNode from "./customNodes/newAgentNode";
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

const nodeTypes = {
  "new-agent": NewAgentNode,
};
const edgeTypes = {
  "custom-edge": CustomEdge,
};

const AgentWorkFlow = ({ agent_id }: { agent_id: string }) => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

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
