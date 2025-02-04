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

const _DUMMY_AGENT_DATA: AgentDataTypes[] = [
  {
    agentId: "new",
    chats: [
      {
        id: "1",
        question: "How to create a new file?",
        assistantAnswer: "You can use the touch command",
        createdAt: "04-02-2025",
      },
    ],
    codes: [
      {
        isActive: true,
        language: "sol",
        fileName: "contract.sol",
        code: "pragma solidity ^0.4.17;\n\ncontract Inbox {\n    string public message;\n\n    function setMessage(string newMessage) public {\n        message = newMessage;\n    }\n\n    function getMessage() public view returns (string) {\n        return message;\n    }\n}",
      },
      {
        isActive: false,
        language: "rust",
        fileName: "main.rs",
        code: 'fn main() {\n    println!("Hello, world!");\n}',
      },
    ],
  },
];

export {
  type UserType,
  _DUMMY_USER,
  type ChatType,
  type AgentDataTypes,
  _DUMMY_AGENT_DATA,
};
