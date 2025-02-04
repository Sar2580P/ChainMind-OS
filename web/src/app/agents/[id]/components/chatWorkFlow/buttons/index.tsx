"use client";
import { Button } from "@/components/ui/button";
import { CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

const Buttons = () => {
  return (
    <CardHeader className="flex flex-row align-middle justify-end sm:justify-between py-3">
      <div className="hidden sm:block">
        <CardTitle>Chat with Agent</CardTitle>
        <CardDescription>
          Chat with the agent to get more information about the work!
        </CardDescription>
      </div>
      <div className="flex flex-row space-x-2">
        <Button onClick={() => {}} variant="secondary">
          Agent 1
        </Button>
      </div>
    </CardHeader>
  );
};

export default Buttons;
