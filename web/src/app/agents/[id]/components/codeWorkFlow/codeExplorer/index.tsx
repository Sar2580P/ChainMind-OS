"use client";
import { FaFile } from "react-icons/fa";
import classes from "./index.module.css";
import { FaFolder } from "react-icons/fa";
import { useState, useContext } from "react";
import { FaFolderOpen } from "react-icons/fa";
import AppContext from "@/contexts/AppContext";
import usePostResponse from "@/hooks/usePostResponse";

interface FileNode {
  name: string;
  children?: FileNode[];
}

const FolderExplorer = ({
  node,
  _parent,
  agent_id,
}: {
  node: FileNode;
  _parent: string;
  agent_id: string;
}) => {
  const { postResponse } = usePostResponse();
  const [isOpen, setIsOpen] = useState(true);
  const { updateCodehandler, agentDatas } = useContext(AppContext);
  console.log(agentDatas);

  const handleToggleAndCodeReview = async (_parent: string) => {
    if (node.children) {
      setIsOpen(!isOpen);
    } else {
      const codePath =
        _parent.split("#").slice(1).join("#").split(".")[0] + ".json";
      console.log(codePath);
      const response = await postResponse(
        { file_name: codePath, agent_id },
        "get_codebase_for_file"
      );
      const file_id = _parent.split("#").slice(1).join(":");
      const file_lang = _parent.split("#").slice(1).join("_").split(".")[1];
      console.log(response);
      console.log(_parent.split("#").slice(1).join(":"), agent_id);
      updateCodehandler(agent_id, file_id, file_lang, response);
    }
  };

  return (
    <div className={classes["folder-item"]}>
      <div
        onClick={() => {
          handleToggleAndCodeReview(_parent + node.name);
        }}
        className={classes["folder-name"]}
      >
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
            <FolderExplorer
              key={index}
              node={child}
              _parent={_parent + node.name + "#"}
              agent_id={agent_id}
            />
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
  const _FOLDER = makeFileTree(all_paths);

  return (
    <div className={classes["container"]} key={agent_id}>
      <FolderExplorer node={_FOLDER} _parent="" agent_id={agent_id} />
    </div>
  );
};

export default CodeExplorer;
