"use client";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";
import CodeEditor from "./codeEditor";
import classes from "./index.module.css";
import CodeExplorer from "./codeExplorer";

const CodeWorkFlow: React.FC<{ agent_id: string }> = ({ agent_id }) => {
  return (
    <div className={classes["container"]}>
      <ResizablePanelGroup direction="horizontal" className="rounded-md border">
        <ResizablePanel defaultSize={20} className="p-2">
          <CodeExplorer agent_id={agent_id} />
        </ResizablePanel>
        <ResizableHandle />
        <ResizablePanel defaultSize={80} className="p-2">
          <CodeEditor agent_id={agent_id} />
        </ResizablePanel>
      </ResizablePanelGroup>
    </div>
  );
};

export default CodeWorkFlow;
