import { Edge } from "@xyflow/react";

const _GRAPH_EDGES = {
  head: ["agent_1_1_1", "agent_1_2_1", "agent_1_3_1"],
  agent_1_1_1: ["agent_2_1_1", "agent_2_1_2"],
  agent_1_2_1: ["agent_2_2_1"],
  agent_1_3_1: ["agent_2_3_1", "agent_2_3_2", "agent_2_3_3"],
  agent_2_1_1: ["tail_1"],
  agent_2_1_2: ["tail_2"],
  agent_2_2_1: ["tail_3"],
  agent_2_3_1: ["tail_4"],
  agent_2_3_2: ["tail_5"],
  agent_2_3_3: ["tail_6"],
};

const MakeGraphEdges: (graphEdges: {
  [key: string]: string[];
}) => Edge[] = (graphEdges: { [key: string]: string[] }) => {
  const edges = [];
  for (const parent in graphEdges) {
    for (const child of graphEdges[parent]) {
      edges.push({
        id: `edge__${parent}__${child}`,
        source: parent,
        target: child,
        animated: true,
        type: "custom-edge",
      });
    }
  }
  return edges;
};

const initialEdges = MakeGraphEdges(_GRAPH_EDGES);

export default initialEdges;

// layer_parentId_childId
