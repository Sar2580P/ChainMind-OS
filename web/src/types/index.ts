interface UserType {
  name: string;
  email: string;
  role: string;
}

const _DUMMY_USER: UserType = {
  name: "Shivam",
  email: "",
  role: "admin",
};

interface ChatType {
  id: string;
  isAgent: boolean;
  message: string;
  createdAt: string;
}

interface CodeType {
  id: string;
  isActive: boolean;
  language: string;
  fileName: string;
  code: string;
  path: string;
}

interface AgentDataTypes {
  agentId: string;
  chats: ChatType[];
  codes: CodeType[];
}

const _DUMMY_AGENT_DATA: AgentDataTypes[] = [];

interface DeployContractDataType {
  objectives: string[];
  brief_context_on_each_objective: string[];
  tech_experts_for_objectives: string[][];
  files: string[][];
  code_instructions: string[][];
}

export {
  type UserType,
  _DUMMY_USER,
  type ChatType,
  type CodeType,
  type AgentDataTypes,
  _DUMMY_AGENT_DATA,
  type DeployContractDataType,
};
