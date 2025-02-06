"use client";
import Chats from "./chats";
import Buttons from "./buttons";
import AskQuestion from "./askQuestion";
import { Card } from "@/components/ui/card";

const ChatWorkFlow = ({ agent_id }: { agent_id: string }) => {
  return (
    <Card
      className="flex flex-col"
      style={{
        height: "calc(100lvh)",
        backgroundColor: "transparent",
        color: "#efeee7",
        marginTop: "2px",
        borderRadius: "5px",
      }}
    >
      <Buttons agent_id={agent_id} />
      <Chats agent_id={agent_id} />
      <AskQuestion agent_id={agent_id} />
    </Card>
  );
};

export default ChatWorkFlow;
