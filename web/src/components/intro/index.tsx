"use client";
import { v4 } from "uuid";
import Link from "next/link";
import classes from "./index.module.css";

const Intro = () => {
  const newAgentId = v4();
  return (
    <div className={classes["container"]}>
      <div className={classes["box"]}>
        <h1>Revolutionizing the Future of Agents</h1>
        <p>
          The future of agents is here! Create your own agent and start your
          journey to the top.
        </p>
        <Link href={`/agents/${newAgentId}`}>Create Agent </Link>
      </div>
    </div>
  );
};

export default Intro;
