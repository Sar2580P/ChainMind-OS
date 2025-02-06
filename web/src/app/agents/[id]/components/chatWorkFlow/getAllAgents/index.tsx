"use client";
import { cn } from "@/lib/utils";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import useGetResponse from "@/hooks/useGetResponse";
import { Check, ChevronsUpDown } from "lucide-react";

export function GetAllAgentprompt({ agent_id }: { agent_id: string }) {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const { getResponse } = useGetResponse();
  const [ai_agents_ids, setAiAgentsIds] = useState<string[]>([]);

  useEffect(() => {
    const fetchAiAgentsIds = async () => {
      const response = await getResponse("");
      if (response) setAiAgentsIds(response.agents);
    };
    fetchAiAgentsIds();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  console.log(ai_agents_ids);
  console.log("value");

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-[150px] justify-between text-zinc-900 pl-2 cursor-pointer"
        >
          {agent_id.substring(0, 10)}...
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[150px] p-0">
        <Command>
          <CommandInput placeholder="Search ai agent..." />
          <CommandList>
            <CommandEmpty>No Ai Agent found.</CommandEmpty>
            <CommandGroup>
              {ai_agents_ids.map((ai_agents_id) => (
                <CommandItem
                  key={ai_agents_id}
                  value={ai_agents_id}
                  onSelect={() => {
                    setOpen(false);
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
