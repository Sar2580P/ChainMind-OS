import classes from "./index.module.css";

const Footer = () => {
  return (
    <div className={classes["container"]}>
      <div className={classes["box"]}>
        <div className={classes["left"]}>
          Made with <span className={classes["heart"]}>&hearts;</span> by
          ChainMind
        </div>
        <div className={classes["right"]}>
          All rights reserved <span>&copy; 2025</span>
        </div>
      </div>
    </div>
  );
};

export default Footer;
