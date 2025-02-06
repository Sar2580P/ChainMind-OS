"use client";
import Chat from "../chat";
import { ChatType } from "@/types";
import AppContext from "@/contexts/AppContext";
import { CardContent } from "@/components/ui/card";
import usePostResponse from "@/hooks/usePostResponse";
import React, { useEffect, useRef, useContext, useMemo } from "react";

interface ChatsProps {
  agent_id: string;
}

const Chats = ({ agent_id }: ChatsProps) => {
  const { postResponse } = usePostResponse();
  const { agentDatas, setAgentDatasHandler } = useContext(AppContext);
  const chats = useMemo(
    () =>
      (agentDatas.find((agent) => agent.agentId === agent_id) || { chats: [] })
        ?.chats || [],
    [agentDatas, agent_id]
  );

  const chatContainerRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [chats]);

  useEffect(() => {
    const fetchChats = async () => {
      const response = await postResponse({ agent_id }, "get_chat_history");
      if (response) {
        setAgentDatasHandler(agent_id, "chats", response);
      }
    };
    fetchChats();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <CardContent className="space-y-2 h-full overflow-y-scroll scrollbar-hide pb-3">
      <div
        ref={chatContainerRef}
        className="overflow-y-auto h-full scrollbar-hide w-full"
      >
        {chats.map((chat: ChatType) => (
          <Chat key={chat.id} chat={chat} />
        ))}
      </div>
    </CardContent>
  );
};

export default Chats;
