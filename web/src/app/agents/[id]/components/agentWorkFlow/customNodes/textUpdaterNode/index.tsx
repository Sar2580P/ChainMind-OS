import classes from "./index.module.css";
import ProviderSelect from "../providerSelect";
import { useCallback, useEffect, useRef } from "react";
import { Handle, Position, useReactFlow } from "@xyflow/react";

const handleStyle = { top: 10 };

interface TextUpdaterNodeProps {
  id: string;
  data: {
    heading: string;
    value: string;
    placeholder: string;
  };
  isConnectable: boolean;
}

const TextUpdaterNode = ({ id, data, isConnectable }: TextUpdaterNodeProps) => {
  const { setNodes } = useReactFlow();
  const containerRef = useRef<HTMLDivElement>(null);

  const onChange = useCallback(
    (evt: React.ChangeEvent<HTMLInputElement>) => {
      setNodes((nodes) =>
        nodes.map((node) => {
          if (node.id === id) {
            return {
              ...node,
              data: {
                ...node.data,
                value: evt.target.value,
              },
            };
          }
          return node;
        })
      );
    },
    [id, setNodes]
  );

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
        position={Position.Left}
        isConnectable={isConnectable}
        style={handleStyle}
      />
      <h1>{data["heading"]}</h1>
      <div className={classes["box"]}>
        <input
          placeholder=" "
          onChange={onChange}
          id="text"
          name="text"
          value={data["value"]}
        />
        <label>
          <span>{data["placeholder"]}</span>
        </label>
      </div>
      <Handle
        type="source"
        position={Position.Right}
        isConnectable={isConnectable}
        style={handleStyle}
      />
      <div className={classes["provider-selector"]}>
        <ProviderSelect />
      </div>
    </div>
  );
};

export default TextUpdaterNode;
