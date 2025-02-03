"use client";
import { use } from "react";
import classes from "@/styles/page.module.css";

interface AgentIdPageProps {
  params: Promise<{ id: string }>;
}

const AgentIdPage: React.FC<AgentIdPageProps> = ({ params }) => {
  const { id } = use(params);

  return (
    <div className={classes["container"]}>
      Agent Id: {id}
      <div className={classes["box"]}>
        <div className={classes["left"]}></div>
        <div className={classes["right"]}></div>
      </div>
    </div>
  );
};

export default AgentIdPage;
