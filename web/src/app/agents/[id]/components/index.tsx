"use client";
import classes from "./index.module.css";
import ChatWorkFlow from "./chatWorkFlow";
import AgentWorkFlow from "./agentWorkFlow";
import CodeWorkFlow from "./codeWorkFlow";

const AgentComponents = ({ id }: { id: string }) => {
  console.log(id);

  return (
    <div className={classes["container"]}>
      <div className={`${classes["chat-code-container"]} scrollbar-hide`}>
        <ChatWorkFlow />
        <CodeWorkFlow />
      </div>
      <div className={classes["agent-container"]}>
        <AgentWorkFlow />
      </div>
    </div>
  );
};

export default AgentComponents;
