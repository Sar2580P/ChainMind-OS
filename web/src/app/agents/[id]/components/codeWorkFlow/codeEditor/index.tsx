"use client";
import * as monaco from "monaco-editor";
import Editor from "@monaco-editor/react";
import AppContext from "@/contexts/AppContext";
import React, { useContext, useMemo, useEffect, useRef, useState } from "react";

const CodeEditor = ({ agent_id }: { agent_id: string }) => {
  const { agentDatas } = useContext(AppContext);
  const [isEditorReady, setIsEditorReady] = useState(false);
  const editorRef = useRef<monaco.editor.IStandaloneCodeEditor | null>(null);

  const code = useMemo(
    () =>
      (
        agentDatas.find((agent) => agent.agentId === agent_id) || { codes: [] }
      )?.codes.filter((code) => code.isActive) || [],
    [agentDatas, agent_id]
  );

  useEffect(() => {
    if (editorRef.current) {
      const editor = editorRef.current;
      const fullCode = code[0]?.code || "";
      let index = 0;
      const interval = setInterval(() => {
        if (index <= fullCode.length) {
          editor.setValue(fullCode.substring(0, index));
          index += 50;
        } else {
          clearInterval(interval);
        }
      }, 100);
      return () => clearInterval(interval);
    }
  }, [code, isEditorReady]);

  return (
    <Editor
      height="100vh"
      language={code[0]?.language || "sol"}
      theme="vs-dark"
      onMount={(editor) => {
        editorRef.current = editor;
        setIsEditorReady(true);
      }}
      loading={<div>Setting up your code editor...</div>}
    />
  );
};

export default CodeEditor;
