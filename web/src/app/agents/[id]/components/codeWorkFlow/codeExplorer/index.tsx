"use client";
import { FaFile } from "react-icons/fa";
import classes from "./index.module.css";
import { FaFolder } from "react-icons/fa";
import { useState, useContext } from "react";
import { FaFolderOpen } from "react-icons/fa";
import AppContext from "@/contexts/AppContext";

interface FileNode {
  name: string;
  children?: FileNode[];
}

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
  const { agentDatas } = useContext(AppContext);
  const codes =
    agentDatas.find((agent) => agent.agentId === agent_id)?.codes || [];
  const all_paths = codes.map((code) => code.path);
  const makeFileTree = (paths: string[]) => {
    const root: FileNode = { name: "src" };
    paths.forEach((path) => {
      const pathArray = path.split(":");
      let current = root;
      pathArray.forEach((folder) => {
        const found = current.children?.find((child) => child.name === folder);
        if (!found) {
          const newFolder: FileNode = { name: folder };
          current.children = current.children || [];
          current.children.push(newFolder);
          current = newFolder;
        } else {
          current = found;
        }
      });
    });
    return root;
  };
  console.log(all_paths);
  const _FOLDER = makeFileTree([
    "contracts:interfaces:IOracle.sol",
    "contracts:Agent.sol",
    "scripts:deploy.ts",
    "scripts:index.ts",
    "test:Agent.test.ts",
    "package.json",
  ]);

  return (
    <div className={classes["container"]} key={agent_id}>
      <FolderExplorer node={_FOLDER} />
    </div>
  );
};

export default CodeExplorer;
