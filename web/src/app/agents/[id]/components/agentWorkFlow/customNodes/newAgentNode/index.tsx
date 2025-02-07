import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import classes from "./index.module.css";
import { useEffect, useRef } from "react";
import AgentsButtons from "./AgnetsButtons";
import ProviderSelect from "../providerSelect";
import { Handle, Position, useReactFlow } from "@xyflow/react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

interface NewAgentNodeProps {
  id: string;
  data: {
    id: string;
    about: string;
    metadata: Record<string, string>;
    agent_id: string;
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

  const layer_id = data["id"].split("_")[1];
  const images = [
    "/robot/robot-left.png",
    "/robot/robot-center.png",
    "/robot/robot-right.png",
  ];

  return (
    <div className={classes["container"]} ref={containerRef} tabIndex={0}>
      <Handle
        type="target"
        position={Position.Top}
        isConnectable={isConnectable}
      />
      <HoverCard>
        <HoverCardTrigger asChild>
          {layer_id == "1" ? (
            <div
              className={classes["url_fixed_box"]}
              style={{
                backgroundImage: `url(${
                  images[Math.floor(Math.random() * images.length)]
                })`,
              }}
            ></div>
          ) : (
            <div className={classes["box"]}></div>
          )}
        </HoverCardTrigger>
        <HoverCardContent
          style={
            layer_id == "1"
              ? {
                  width: "320px",
                }
              : {
                  width: "420px",
                }
          }
        >
          <div className="flex justify-start space-x-4">
            <Avatar>
              <AvatarImage src="/robot/logo.png" />
              <AvatarFallback>AG</AvatarFallback>
            </Avatar>
            <div className="space-y-1 mb-1">
              <h4 className="text-base font-semibold">@{data["id"]}</h4>
              <div className="flex items-center">
                <div className="text-base text-muted-foreground">
                  {data["about"]}
                </div>
              </div>
              <div className="flex flex-col space-y-1 justify-start align-top">
                {Object.keys(data["metadata"]).map((key, i) => (
                  <div
                    key={i}
                    className="flex items-start justify-start flex-col"
                  >
                    <div className="font-bold capitalize text-base">{key}</div>
                    <div className="text-xs text-muted-foreground pl-1">
                      {Array.isArray(data["metadata"][key])
                        ? data["metadata"][key].map((item, index) => (
                            <div
                              key={item}
                              className="text-sm pt-1"
                              style={{
                                wordBreak: "break-all",
                              }}
                            >
                              <span className="text-muted-foreground font-semibold">
                                {index + 1}.
                              </span>
                              {item}
                            </div>
                          ))
                        : data["metadata"][key]}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
          {layer_id == "2" && (
            <AgentsButtons id={data["id"]} agent_id={data["agent_id"]} />
          )}
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
