"use client";
import { ChatType } from "@/types";
import Markdown from "react-markdown";
import { Card, CardContent, CardDescription } from "@/components/ui/card";

interface ChatProps {
  chat: ChatType;
}

const Chat = ({ chat }: ChatProps) => {
  return (
    <Card key={chat.id} className={`pt-4 relative mb-4 bg-transparent`}>
      <CardContent className="pb-4 pt-1">
        <CardDescription className="p-2 mb-2 border border-gray-300 rounded text-sm">
          <span className="font-semibold text-gray-50">User</span>
          <Markdown className="text-gray-400">{chat.question}</Markdown>
        </CardDescription>
        <CardDescription className="p-2 mb-2 border border-gray-100 rounded text-sm relative">
          <span className="font-semibold text-gray-200">Assistant</span>{" "}
          <Markdown className="text-gray-400">{chat.assistantAnswer}</Markdown>
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
