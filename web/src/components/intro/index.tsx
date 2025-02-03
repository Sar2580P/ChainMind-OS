import Link from "next/link";
import classes from "./index.module.css";

const Intro = () => {
  return (
    <div className={classes["container"]}>
      <div className={classes["box"]}>
        <h1>Revolutionizing the Future of Agents</h1>
        <p>
          The future of agents is here! Create your own agent and start your
          journey to the top.
        </p>
        <Link href="/agents/new">Create Agent </Link>
      </div>
    </div>
  );
};

export default Intro;
