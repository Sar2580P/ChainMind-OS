import { Edge } from "@xyflow/react";
import { Node, Position } from "@xyflow/react";

const CreateNodeAndEdgesData = (data: {
  objectives: string[];
  brief_context_on_each_objective: string[];
  tech_experts_for_objectives: string[][];
}) => {
  console.log(data);
  const _GRAPH_EDGES: Record<string, string[]> = { head: [] };
  const _ALL_TAIL_ID: string[] = [];
  const _ALL_AGENT_ID: string[] = [];
  const all_agents = new Set<string>();
  const _AGENT_ID_AOUT_AND_DESC: Record<
    string,
    { about: string; description: string }
  > = {};

  const number_of_layer_1_agents = data.objectives.length;
  let tail_count = 0;
  for (let i = 0; i < number_of_layer_1_agents; i++) {
    const number_of_layer_2_agents = data.tech_experts_for_objectives[i].length;
    _GRAPH_EDGES["head"].push(`agent_1_${i + 1}_1`);

    all_agents.add(`agent_1_${i + 1}_1`);

    _AGENT_ID_AOUT_AND_DESC[`agent_1_${i + 1}_1`] = {
      about: data.objectives[i],
      description: data.brief_context_on_each_objective[i],
    };

    for (let j = 0; j < number_of_layer_2_agents; j++) {
      _GRAPH_EDGES[`agent_1_${i + 1}_1`] =
        _GRAPH_EDGES[`agent_1_${i + 1}_1`] || [];
      _GRAPH_EDGES[`agent_1_${i + 1}_1`].push(`agent_2_${i + 1}_${j + 1}`);

      _GRAPH_EDGES[`agent_2_${i + 1}_${j + 1}`] =
        _GRAPH_EDGES[`agent_2_${i + 1}_${j + 1}`] || [];
      _GRAPH_EDGES[`agent_2_${i + 1}_${j + 1}`].push(`tail_${++tail_count}`);

      all_agents.add(`agent_2_${i + 1}_${j + 1}`);

      _AGENT_ID_AOUT_AND_DESC[`agent_2_${i + 1}_${j + 1}`] = {
        about: data.tech_experts_for_objectives[i][j],
        description: "Ask Expert for help and create code file",
      };
    }
  }

  for (let i = 0; i < tail_count; i++) {
    _ALL_TAIL_ID.push(`tail_${i + 1}`);
  }

  all_agents.forEach((agent) => {
    _ALL_AGENT_ID.push(agent);
  });

  console.log(
    _GRAPH_EDGES,
    _ALL_TAIL_ID,
    _ALL_AGENT_ID,
    _AGENT_ID_AOUT_AND_DESC
  );
  return { _GRAPH_EDGES, _ALL_TAIL_ID, _ALL_AGENT_ID, _AGENT_ID_AOUT_AND_DESC };
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
  allAgentIds: string[],
  _AGENT_ID_AOUT_AND_DESC: Record<
    string,
    { about: string; description: string }
  >,
  agent_id: string
) => Node[] = (
  allTailIds: string[],
  allAgentIds: string[],
  _AGENT_ID_AOUT_AND_DESC: Record<
    string,
    { about: string; description: string }
  >,
  agent_id: string
) => {
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
          about: _AGENT_ID_AOUT_AND_DESC[nodeId].about,
          metadata: {
            description: _AGENT_ID_AOUT_AND_DESC[nodeId].description,
          },
          agent_id: agent_id,
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

const CreateNodeAndEdges = (
  data: {
    objectives: string[];
    brief_context_on_each_objective: string[];
    tech_experts_for_objectives: string[][];
  },
  agent_id: string
) => {
  const { _GRAPH_EDGES, _ALL_TAIL_ID, _ALL_AGENT_ID, _AGENT_ID_AOUT_AND_DESC } =
    CreateNodeAndEdgesData(data);
  const Edges = MakeGraphEdges(_GRAPH_EDGES);
  const Nodes = MakeGraphNodes(
    _ALL_TAIL_ID,
    _ALL_AGENT_ID,
    _AGENT_ID_AOUT_AND_DESC,
    agent_id
  );
  return { Edges, Nodes };
};

export { CreateNodeAndEdges };
