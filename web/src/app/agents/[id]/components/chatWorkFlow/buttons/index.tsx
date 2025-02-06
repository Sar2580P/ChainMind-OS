"use client";
import { Button } from "@/components/ui/button";
import { CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

const Buttons = ({ agent_id }: { agent_id: string }) => {
  return (
    <CardHeader className="flex flex-row align-middle justify-end sm:justify-between py-3">
      <div className="hidden sm:block">
        <CardTitle>
          Chat with Agent{" "}
          {agent_id.substring(0, 4) +
            "...." +
            agent_id.substring(agent_id.length - 4)}
        </CardTitle>
        <CardDescription>
          Chat with the agent to get more information about the work!
        </CardDescription>
      </div>
      <div className="flex flex-row space-x-2 text-gray-900">
        <Button onClick={() => {}} variant="outline">
          Deploy Agent
        </Button>
      </div>
    </CardHeader>
  );
};

export default Buttons;
