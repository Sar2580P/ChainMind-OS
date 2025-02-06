"use client";
import classes from "./index.module.css";
import ChatWorkFlow from "./chatWorkFlow";
import CodeWorkFlow from "./codeWorkFlow";
import AgentWorkFlow from "./agentWorkFlow";
import AppContext from "@/contexts/AppContext";
import { IoIosArrowRoundUp } from "react-icons/io";
import { TbSwitchHorizontal } from "react-icons/tb";
import { useState, useContext, useEffect } from "react";

const AgentComponents = ({ id }: { id: string }) => {
  const { setNewAgentHandler } = useContext(AppContext);
  const [isAccessible, setIsAccessible] = useState(false);

  useEffect(() => {
    setNewAgentHandler(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className={classes["container"]}>
      <div className={`${classes["chat-code-container"]} scrollbar-hide`}>
        {isAccessible ? (
          <CodeWorkFlow agent_id={id} />
        ) : (
          <ChatWorkFlow agent_id={id} />
        )}
        <div className={classes["scroll-to-top"]}>
          <IoIosArrowRoundUp
            onClick={() => {
              window.scrollTo(0, 83);
            }}
          />
        </div>
        <TbSwitchHorizontal onClick={() => setIsAccessible(!isAccessible)} />
      </div>
      <div className={classes["agent-container"]}>
        <AgentWorkFlow agent_id={id} />
      </div>
    </div>
  );
};

export default AgentComponents;
