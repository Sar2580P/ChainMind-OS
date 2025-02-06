import { Node, Position } from "@xyflow/react";
const _ALL_TAIL_ID = ["tail_1"];
const _ALL_AGENT_ID = ["agent_1_1_1", "agent_2_1_1"];

const groupAgentsByLayer = (allAgentIds: string[]) => {
  const layerMap: Record<number, string[]> = {};
  allAgentIds.forEach((agentId) => {
    const layer = parseInt(agentId.split("_")[1]);
    if (!layerMap[layer]) layerMap[layer] = [];
    layerMap[layer].push(agentId);
  });
  return layerMap;
};

const MakeGraphNodes: (
  allTailIds: string[],
  allAgentIds: string[]
) => Node[] = (allTailIds: string[], allAgentIds: string[]) => {
  const nodes = [];
  nodes.push({
    id: "head",
    type: "input",
    data: { label: "Master Agent" },
    position: { x: 400, y: 50 },
    sourcePosition: "bottom" as Position,
  });

  const layerMap = groupAgentsByLayer(allAgentIds);
  Object.keys(layerMap).forEach((layerStr) => {
    const layer = parseInt(layerStr);
    const agentsInLayer = layerMap[layer];
    const layerWidth = agentsInLayer.length * 170;
    agentsInLayer.forEach((nodeId, index) => {
      const x_cord = 500 - layerWidth / 2 + index * 170;
      nodes.push({
        id: nodeId,
        type: "new-agent",
        data: {
          id: nodeId.toUpperCase(),
          about: "Blockchain for fee payments",
          metadata: {
            description:
              "Using blockchain for immutable and transparent fee payments.",
          },
          agent_id: "new",
        },
        position: { x: x_cord, y: 150 + (layer - 1) * 200 },
      });
    });
  });

  allTailIds.forEach((tailId: string, index: number) => {
    nodes.push({
      id: `${tailId}`,
      type: "output",
      data: { label: "Create Code File" },
      position: { x: -100 + 170 * index, y: 550 },
      targetPosition: "top" as Position,
    });
  });
  return nodes;
};

const initialNodes = MakeGraphNodes(_ALL_TAIL_ID, _ALL_AGENT_ID);

export default initialNodes;
