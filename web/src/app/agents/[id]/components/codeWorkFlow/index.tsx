"use client";
import classes from "./index.module.css";
import CodeEditor from "./codeEditor";
import CodeExplorer from "./codeExplorer";

const CodeWorkFlow = () => {
  return (
    <div className={classes["container"]}>
      <CodeEditor />
      <CodeExplorer />
    </div>
  );
};

export default CodeWorkFlow;
