import AgentComponents from "./components";
import classes from "@/styles/page.module.css";

interface AgentIdPageProps {
  params: Promise<{ id: string }>;
}

const AgentIdPage: React.FC<AgentIdPageProps> = async ({ params }) => {
  const { id } = await params;

  return (
    <div className={classes["container"]}>
      <AgentComponents id={id} />
      <div className={classes["box"]}>
        <div className={classes["left"]}></div>
        <div className={classes["right"]}></div>
      </div>
    </div>
  );
};

export default AgentIdPage;
