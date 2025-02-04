"use client";
import classes from "./index.module.css";
import AskQuestion from "./askQuestion";
import Chats from "./chats";
import Buttons from "./buttons";

const ChatWorkFlow = () => {
  return (
    <div className={classes["container"]}>
      <AskQuestion />
      <Chats />
      <Buttons />
    </div>
  );
};

export default ChatWorkFlow;
