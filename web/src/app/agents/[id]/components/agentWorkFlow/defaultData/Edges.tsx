import { Edge } from "@xyflow/react";

const _GRAPH_EDGES = {
  head: ["agent_1_1_1"],
  agent_1_1_1: ["agent_2_1_1"],
  agent_2_1_1: ["tail_1"],
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
