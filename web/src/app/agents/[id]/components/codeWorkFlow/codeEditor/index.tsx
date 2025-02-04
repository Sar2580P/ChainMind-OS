"use client";
import Editor from "@monaco-editor/react";
import AppContext from "@/contexts/AppContext";
import React, { useContext, useMemo } from "react";

const CodeEditor = ({ agent_id }: { agent_id: string }) => {
  const { agentDatas } = useContext(AppContext);
  const code = useMemo(
    () =>
      (
        agentDatas.find((agent) => agent.agentId === agent_id) || { codes: [] }
      )?.codes.filter((code) => code.isActive) || [],
    [agentDatas, agent_id]
  );

  return (
    <Editor
      height="100vh"
      defaultLanguage={code[0].language || "javascript"}
      defaultValue={code[0].code || ""}
      theme="vs-dark"
    />
  );
};

export default CodeEditor;
