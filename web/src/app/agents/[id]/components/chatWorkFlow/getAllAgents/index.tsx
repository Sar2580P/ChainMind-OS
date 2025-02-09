"use client";
import { cn } from "@/lib/utils";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import { useReadContract } from "wagmi";
import { useRouter } from "next/navigation";
import configData from "@/config/config.json";
import { Button } from "@/components/ui/button";
import { Check, ChevronsUpDown } from "lucide-react";

export function GetAllAgentprompt({ agent_id }: { agent_id: string }) {
  const router = useRouter();
  const { data: allAgentDetails } = useReadContract({
    abi: configData.abi,
    address: configData.contractAddress.arbitrumsepolia as `0x${string}`,
    functionName: "getAllAiAgents",
    args: [],
  }) as {
    data: {
      id: string;
      agentObjectives: string[];
      briefContextOnEachObjective: string[];
      techExpertise: string[][];
      files: string[][];
      instructions: string[][];
    }[];
  };
  const ai_agents_ids = Array.isArray(allAgentDetails)
    ? allAgentDetails.map((agent) => agent.id)
    : [];

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          className="w-[150px] justify-between text-zinc-900 pl-2 cursor-pointer"
        >
          All Ai Agents
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[150px] p-0">
        <Command>
          <CommandInput placeholder="Search ai agent..." />
          <CommandList>
            <CommandEmpty>No Ai Agent Deployed.</CommandEmpty>
            <CommandGroup>
              {ai_agents_ids.map((ai_agents_id, index) => (
                <CommandItem
                  key={ai_agents_id + index}
                  value={ai_agents_id}
                  onSelect={() => {
                    router.push(`/agents/${ai_agents_id}`);
                  }}
                >
                  <Check
                    className={cn(
                      "mr-2 h-4 w-4",
                      agent_id === ai_agents_id ? "opacity-100" : "opacity-0"
                    )}
                  />
                  {ai_agents_id.substring(0, 10)}...
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
