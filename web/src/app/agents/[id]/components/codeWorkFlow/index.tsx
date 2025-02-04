"use client";
import classes from "./index.module.css";
import CodeEditor from "./codeEditor";
import CodeExplorer from "./codeExplorer";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";

const CodeWorkFlow = () => {
  return (
    <div className={classes["container"]}>
      <ResizablePanelGroup direction="horizontal" className="rounded-md border">
        <ResizablePanel defaultSize={20} className="p-2">
          <CodeEditor />
        </ResizablePanel>
        <ResizableHandle />
        <ResizablePanel defaultSize={80} className="p-2">
          <CodeExplorer />
        </ResizablePanel>
      </ResizablePanelGroup>
    </div>
  );
};

export default CodeWorkFlow;
