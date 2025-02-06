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
  question: string;
  assistantAnswer: string;
  createdAt: string;
}

interface CodeType {
  id: string;
  isActive: boolean;
  language: string;
  fileName: string;
  code: string;
}

interface AgentDataTypes {
  agentId: string;
  chats: ChatType[];
  codes: CodeType[];
}

const _DUMMY_AGENT_DATA: AgentDataTypes[] = [];

export {
  type UserType,
  _DUMMY_USER,
  type ChatType,
  type CodeType,
  type AgentDataTypes,
  _DUMMY_AGENT_DATA,
};
