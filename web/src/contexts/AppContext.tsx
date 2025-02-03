"use client";
import { UserType, _DUMMY_USER } from "@/types";
import React, { useState } from "react";

type AppContextType = {
  userData: UserType;
  setuseDataHandler: (key: keyof UserType, value: string) => void;
};

const AppContext = React.createContext<AppContextType>({
  userData: _DUMMY_USER,
  setuseDataHandler: () => {},
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

  return (
    <AppContext.Provider
      value={{
        userData,
        setuseDataHandler: setuseDataHandler,
      }}
    >
      {props.children}
    </AppContext.Provider>
  );
};

export default AppContext;
