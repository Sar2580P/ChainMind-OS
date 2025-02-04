"use client";
import { useState } from "react";
import { FaFile } from "react-icons/fa";
import classes from "./index.module.css";
import { FaFolder } from "react-icons/fa";
import { FaFolderOpen } from "react-icons/fa";

interface FileNode {
  name: string;
  children?: FileNode[];
}

const _FOLDER: FileNode = {
  name: "src",
  children: [
    {
      name: "contracts",
      children: [
        {
          name: "interfaces",
          children: [{ name: "IOracle.sol" }],
        },
        { name: "Agent.sol" },
      ],
    },
    {
      name: "scripts",
      children: [{ name: "deploy.ts" }, { name: "index.ts" }],
    },
    {
      name: "test",
      children: [{ name: "Agent.test.ts" }],
    },
    { name: "package.json" },
  ],
};

const FolderExplorer = ({ node }: { node: FileNode }) => {
  const [isOpen, setIsOpen] = useState(true);

  const toggleOpen = () => {
    if (node.children) {
      setIsOpen(!isOpen);
    }
  };

  return (
    <div className={classes["folder-item"]}>
      <div onClick={toggleOpen} className={classes["folder-name"]}>
        {node.children ? (
          isOpen ? (
            <FaFolderOpen color="#fccc77" />
          ) : (
            <FaFolder color="#f1d592" />
          )
        ) : (
          <FaFile color="#efeee7" />
        )}
        {node.name}
      </div>
      {isOpen && node.children && (
        <div className={classes["folder-children"]}>
          {node.children.map((child, index) => (
            <FolderExplorer key={index} node={child} />
          ))}
        </div>
      )}
    </div>
  );
};

const CodeExplorer = ({ agent_id }: { agent_id: string }) => {
  return (
    <div className={classes["container"]} key={agent_id}>
      <FolderExplorer node={_FOLDER} />
    </div>
  );
};

export default CodeExplorer;
