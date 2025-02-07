"use client";
import { ChatType } from "@/types";
import Markdown from "react-markdown";
import { FaRobot } from "react-icons/fa";
import { FaRegUser } from "react-icons/fa";
import { Card, CardContent, CardDescription } from "@/components/ui/card";

interface ChatProps {
  chat: ChatType;
}

const Chat = ({ chat }: ChatProps) => {
  return (
    <Card key={chat.id} className={`p-2 relative m-0 bg-transparent mb-2`}>
      <CardContent className="p-0 pb-4 pt-1">
        <CardDescription className="p-0 m-0 text-sm relative flex gap-2">
          <span className="font-semibold text-gray-200">
            {chat.isAgent ? <FaRobot size={20} /> : <FaRegUser size={20} />}
          </span>{" "}
          <Markdown className="text-gray-50 text-base">{chat.message}</Markdown>
        </CardDescription>
        <div className="absolute bottom-1 right-2 text-xs font-bold text-gray-400">
          {new Date(chat.createdAt).toLocaleDateString("en-GB", {
            day: "2-digit",
            month: "2-digit",
            year: "2-digit",
          })}
        </div>
      </CardContent>
    </Card>
  );
};

export default Chat;
