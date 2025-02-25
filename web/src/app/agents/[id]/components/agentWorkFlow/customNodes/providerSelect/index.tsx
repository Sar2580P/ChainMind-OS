"use client";
import { FaPlus } from "react-icons/fa6";
import classes from "./index.module.css";
import { useEffect, useRef } from "react";
import { useReactFlow } from "@xyflow/react";
import Providers from "../../defaultData/Providers";

export default function ProviderSelect() {
  const { setNodes } = useReactFlow();
  const detailsRef = useRef<HTMLDetailsElement>(null);

  const onProviderClick = ({
    type,
    id,
    about,
    metadata,
  }: {
    type: string;
    id: string;
    about: string;
    metadata: Record<string, string>;
  }) => {
    setNodes((prevNodes) => [
      ...prevNodes,
      {
        id: `${new Date().getTime().toString()}`,
        data: { id, about, metadata },
        type: type,
        position: {
          x: 10 + prevNodes.length * 30,
          y: 10 + prevNodes.length * 30,
        },
      },
    ]);
  };

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        detailsRef.current &&
        !detailsRef.current.contains(event.target as Node)
      ) {
        detailsRef.current.removeAttribute("open");
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div className={classes["provider-select-container"]}>
      <details ref={detailsRef}>
        <summary>
          <FaPlus size={16} />
        </summary>
        <ul>
          {Providers.map((provider , index) => (
            <li
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              onClick={() => onProviderClick(provider as any)}
              key={provider.type + index}
            >
              {provider.name}
            </li>
          ))}
        </ul>
      </details>
    </div>
  );
}
