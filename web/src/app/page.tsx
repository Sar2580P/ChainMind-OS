import Intro from "@/components/intro";
import classes from "@/styles/page.module.css";

export default function Home() {
  return (
    <div className={classes["container"]}>
      <Intro />
      <div className={classes["box"]}>
        <div className={classes["left"]}></div>
        <div className={classes["right"]}></div>
      </div>
    </div>
  );
}
