"use client";
import classes from "./index.module.css";
import ChatWorkFlow from "./chatWorkFlow";
import CodeWorkFlow from "./codeWorkFlow";
import AgentWorkFlow from "./agentWorkFlow";

const AgentComponents = ({ id }: { id: string }) => {
  console.log(id);
  const isAccessible = false;

  return (
    <div className={classes["container"]}>
      <div className={`${classes["chat-code-container"]} scrollbar-hide`}>
        {isAccessible ? <CodeWorkFlow /> : <ChatWorkFlow />}
      </div>
      <div className={classes["agent-container"]}>
        <AgentWorkFlow />
      </div>
    </div>
  );
};

export default AgentComponents;
