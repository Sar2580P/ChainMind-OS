import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import classes from "./index.module.css";
import { useEffect, useRef } from "react";
import ProviderSelect from "../providerSelect";
import { Handle, Position, useReactFlow } from "@xyflow/react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

interface NewAgentNodeProps {
  id: string;
  data: {
    id: string;
    about: string;
    description: string;
  };
  isConnectable: boolean;
}

const NewAgentNode = ({ id, data, isConnectable }: NewAgentNodeProps) => {
  const { setNodes } = useReactFlow();
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (
        event.key === "Delete" &&
        containerRef.current &&
        containerRef.current.contains(document.activeElement)
      ) {
        setNodes((nodes) => nodes.filter((node) => node.id !== id));
      }
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [id, setNodes]);

  return (
    <div className={classes["container"]} ref={containerRef} tabIndex={0}>
      <Handle
        type="target"
        position={Position.Top}
        isConnectable={isConnectable}
      />
      <HoverCard>
        <HoverCardTrigger asChild>
          <div className={classes["box"]}></div>
        </HoverCardTrigger>
        <HoverCardContent className="w-80">
          <div className="flex justify-between space-x-4">
            <Avatar>
              <AvatarImage src="/robot/logo.png" />
              <AvatarFallback>AG</AvatarFallback>
            </Avatar>
            <div className="space-y-1">
              <h4 className="text-sm font-semibold">@{data["id"]}</h4>
              <div className="flex items-center">
                <span className="text-xs text-muted-foreground">
                  {data["about"]}
                </span>
              </div>
              <p className="text-sm">{data["description"]}</p>
            </div>
          </div>
        </HoverCardContent>
      </HoverCard>
      <Handle
        type="source"
        position={Position.Bottom}
        isConnectable={isConnectable}
      />
      <div className={classes["provider-selector"]}>
        <ProviderSelect />
      </div>
    </div>
  );
};

export default NewAgentNode;
