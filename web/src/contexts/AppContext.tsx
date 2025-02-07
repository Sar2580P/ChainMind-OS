"use client";
import {
  UserType,
  _DUMMY_USER,
  AgentDataTypes,
  _DUMMY_AGENT_DATA,
  ChatType,
  CodeType,
  DeployContractDataType,
} from "@/types";
import React, { useState } from "react";
import { Edge, Node } from "@xyflow/react";

type AppContextType = {
  userData: UserType;
  setuseDataHandler: (key: keyof UserType, value: string) => void;

  agentDatas: AgentDataTypes[];
  setAgentDatasHandler: (
    agentId: string,
    key: "chats" | "codes",
    value: ChatType[] | CodeType[]
  ) => void;
  setNewAgentHandler: (agentId: string) => void;

  agentCurrentNodeAndEdges: { Nodes: Node[]; Edges: Edge[] };
  setAgentCurrentNodeAndEdgesHandler: (Nodes: Node[], Edges: Edge[]) => void;

  updateCodehandler: (
    agentId: string,
    codeId: string,
    language: string,
    code: string
  ) => void;

  deployContractData: DeployContractDataType;
  setDeployContractDataHandler: (
    key: keyof DeployContractDataType,
    value: unknown
  ) => void;
};

const AppContext = React.createContext<AppContextType>({
  userData: _DUMMY_USER,
  setuseDataHandler: () => {},

  agentDatas: _DUMMY_AGENT_DATA,
  setAgentDatasHandler: () => {},
  setNewAgentHandler: () => {},

  agentCurrentNodeAndEdges: { Nodes: [], Edges: [] },
  setAgentCurrentNodeAndEdgesHandler: () => {},

  updateCodehandler: () => {},
  deployContractData: {
    objectives: [],
    brief_context_on_each_objective: [],
    tech_experts_for_objectives: [],
    files: [],
    code_instructions: [],
  },
  setDeployContractDataHandler: () => {},
});

type Props = {
  children: React.ReactNode;
};

export const AppContextProvider: React.FC<Props> = (props) => {
  const [userData, setUserData] = useState(_DUMMY_USER);
  const setuseDataHandler = (key: keyof UserType, value: string) => {
    setUserData((prevState) => {
      return {
        ...prevState,
        [key]: value,
      };
    });
  };

  const [agentDatas, setAgentDatas] =
    useState<AgentDataTypes[]>(_DUMMY_AGENT_DATA);
  const setAgentDatasHandler = (
    agentId: string,
    key: "chats" | "codes",
    value: ChatType[] | CodeType[]
  ) => {
    setAgentDatas((prevState) => {
      return prevState.map((agent) => {
        if (agent.agentId === agentId) {
          return {
            ...agent,
            [key]: [...agent[key], ...value],
          };
        }
        return agent;
      });
    });
  };
  const setNewAgentHandler = (agentId: string) => {
    if (agentDatas.find((agent) => agent.agentId === agentId)) return;
    setAgentDatas((prevState) => {
      return [
        ...prevState,
        {
          agentId: agentId,
          chats: [],
          codes: [],
        },
      ];
    });
  };

  const [agentCurrentNodeAndEdges, setAgentCurrentNodeAndEdges] = useState<{
    Nodes: Node[];
    Edges: Edge[];
  }>({
    Nodes: [],
    Edges: [],
  });
  const setAgentCurrentNodeAndEdgesHandler = (Nodes: Node[], Edges: Edge[]) => {
    setAgentCurrentNodeAndEdges({
      Nodes: Nodes,
      Edges: Edges,
    });
  };

  const updateCodehandler = (
    agentId: string,
    codeId: string,
    language: string,
    code: string
  ) => {
    setAgentDatas((prevState) => {
      return prevState.map((agent) => {
        if (agent.agentId === agentId) {
          return {
            ...agent,
            codes: agent.codes.map((_code) => {
              console.log(_code.id, codeId);
              if (_code.id === codeId) {
                return {
                  ..._code,
                  code: code,
                  isActive: true,
                  language: language,
                };
              }
              return { ..._code, isActive: false };
            }),
          };
        }
        return agent;
      });
    });
  };

  const [deployContractData, setDeployContractData] =
    useState<DeployContractDataType>({
      objectives: [],
      brief_context_on_each_objective: [],
      tech_experts_for_objectives: [],
      files: [],
      code_instructions: [],
    });
  const setDeployContractDataHandler = (
    key: keyof DeployContractDataType,
    value: unknown
  ) => {
    setDeployContractData((prevState) => {
      return {
        ...prevState,
        [key]: value,
      };
    });
  };

  return (
    <AppContext.Provider
      value={{
        userData,
        setuseDataHandler: setuseDataHandler,

        agentDatas,
        setAgentDatasHandler: setAgentDatasHandler,
        setNewAgentHandler: setNewAgentHandler,

        agentCurrentNodeAndEdges,
        setAgentCurrentNodeAndEdgesHandler: setAgentCurrentNodeAndEdgesHandler,

        updateCodehandler: updateCodehandler,

        deployContractData,
        setDeployContractDataHandler: setDeployContractDataHandler,
      }}
    >
      {props.children}
    </AppContext.Provider>
  );
};

export default AppContext;
