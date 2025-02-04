import { Node, Position } from "@xyflow/react";

const initialNodes: Node[] = [
  {
    id: "1",
    type: "input",
    data: { label: "Master Agent" },
    position: { x: 300, y: 50 },
    sourcePosition: "bottom" as Position,
  },
  {
    id: "2",
    type: "new-agent",
    data: {
      id: "Agent 1",
      about: "Blockchain for fee payments",
      description:
        "Using blockchain for immutable and transparent fee payments.",
    },
    position: { x: 450, y: 150 },
  },
  {
    id: "3",
    type: "output",
    data: { label: "Create Code File" },
    position: { x: 300, y: 300 },
    targetPosition: "top" as Position,
  },
];

export default initialNodes;
