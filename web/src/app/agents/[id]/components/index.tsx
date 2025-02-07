"use client";
import classes from "./index.module.css";
import ChatWorkFlow from "./chatWorkFlow";
import CodeWorkFlow from "./codeWorkFlow";
import AgentWorkFlow from "./agentWorkFlow";
import AppContext from "@/contexts/AppContext";
import { IoIosArrowRoundUp } from "react-icons/io";
import { TbSwitchHorizontal } from "react-icons/tb";
import { useState, useContext, useEffect } from "react";
import NftMarketModelling from "./nftMarketModelling/NftMarketModelling";

const AgentComponents = ({ id }: { id: string }) => {
  const { setNewAgentHandler } = useContext(AppContext);
  const [isAccessible, setIsAccessible] = useState(0);

  useEffect(() => {
    setNewAgentHandler(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className={classes["container"]}>
      <div className={`${classes["chat-code-container"]} scrollbar-hide`}>
        {isAccessible == 0 ? (
          <ChatWorkFlow agent_id={id} />
        ) : isAccessible == 1 ? (
          <CodeWorkFlow agent_id={id} />
        ) : (
          <NftMarketModelling />
        )}
        <div className={classes["scroll-to-top"]}>
          <IoIosArrowRoundUp
            onClick={() => {
              window.scrollTo(0, 83);
            }}
          />
        </div>
        <TbSwitchHorizontal
          onClick={() => setIsAccessible((prev) => (prev + 1) % 3)}
        />
      </div>
      <div className={classes["agent-container"]}>
        <AgentWorkFlow agent_id={id} />
      </div>
    </div>
  );
};

export default AgentComponents;
