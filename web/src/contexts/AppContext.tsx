"use client";
import {
  UserType,
  _DUMMY_USER,
  AgentDataTypes,
  _DUMMY_AGENT_DATA,
} from "@/types";
import React, { useState } from "react";

type AppContextType = {
  userData: UserType;
  setuseDataHandler: (key: keyof UserType, value: string) => void;

  agentDatas: AgentDataTypes[];
  setAgentDatasHandler: (data: AgentDataTypes[]) => void;
};

const AppContext = React.createContext<AppContextType>({
  userData: _DUMMY_USER,
  setuseDataHandler: () => {},

  agentDatas: _DUMMY_AGENT_DATA,
  setAgentDatasHandler: () => {},
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
  const setAgentDatasHandler = (data: AgentDataTypes[]) => {
    setAgentDatas(data);
  };

  return (
    <AppContext.Provider
      value={{
        userData,
        setuseDataHandler: setuseDataHandler,

        agentDatas,
        setAgentDatasHandler: setAgentDatasHandler,
      }}
    >
      {props.children}
    </AppContext.Provider>
  );
};

export default AppContext;
