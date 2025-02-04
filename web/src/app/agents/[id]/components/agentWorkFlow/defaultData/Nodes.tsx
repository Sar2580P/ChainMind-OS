import { Node, Position } from "@xyflow/react";

const initialNodes: Node[] = [
  {
    id: "1",
    type: "input",
    data: { label: "Input Node" },
    position: { x: 50, y: 250 },
    sourcePosition: "right" as Position,
  },
  {
    id: "2",
    type: "text-updater",
    data: {
      value: "shivam6862",
      placeholder: "Enter your username",
      heading: "Write User Name",
    },
    position: { x: 300, y: 225 },
  },
  {
    id: "3",
    type: "output",
    data: { label: "Output Node" },
    position: { x: 550, y: 250 },
    targetPosition: "left" as Position,
  },
];

export default initialNodes;
