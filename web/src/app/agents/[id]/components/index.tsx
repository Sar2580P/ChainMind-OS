"use client";
import classes from "./index.module.css";
import ChatWorkFlow from "./chatWorkFlow";
import CodeWorkFlow from "./codeWorkFlow";
import AgentWorkFlow from "./agentWorkFlow";

const AgentComponents = ({ id }: { id: string }) => {
  const isAccessible = true;

  return (
    <div className={classes["container"]}>
      <div className={`${classes["chat-code-container"]} scrollbar-hide`}>
        {isAccessible ? (
          <CodeWorkFlow agent_id={id} />
        ) : (
          <ChatWorkFlow agent_id={id} />
        )}
      </div>
      <div className={classes["agent-container"]}>
        <AgentWorkFlow agent_id={id} />
      </div>
    </div>
  );
};

export default AgentComponents;
