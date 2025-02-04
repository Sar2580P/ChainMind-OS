"use client";
import {
  EdgeLabelRenderer,
  getStraightPath,
  useReactFlow,
  BezierEdge,
} from "@xyflow/react";
import { Position } from "@xyflow/react";
import { TiDeleteOutline } from "react-icons/ti";

interface CustomEdgeProps {
  id: string;
  sourceX: number;
  sourceY: number;
  targetX: number;
  targetY: number;
  sourcePosition: string;
  targetPosition: string;
}

const CustomEdge = ({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
}: CustomEdgeProps) => {
  const { setEdges } = useReactFlow();
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [path, labelX, labelY] = getStraightPath({
    sourceX,
    sourceY,
    targetX,
    targetY,
  });

  return (
    <>
      <BezierEdge
        id={id}
        sourceX={sourceX}
        sourceY={sourceY}
        targetX={targetX}
        targetY={targetY}
        sourcePosition={sourcePosition as Position}
        targetPosition={targetPosition as Position}
      />
      <EdgeLabelRenderer>
        <div
          style={{
            position: "absolute",
            transform: `translate(-50%, -50%) translate(${labelX}px, ${labelY}px)`,
            pointerEvents: "all",
          }}
          className={" nodrag nopan"}
          onClick={() => setEdges((edges) => edges.filter((e) => e.id !== id))}
        >
          <TiDeleteOutline size={16} color="white" />
        </div>
      </EdgeLabelRenderer>
    </>
  );
};

export default CustomEdge;
