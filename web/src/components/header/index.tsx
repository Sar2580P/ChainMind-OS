"use client";
import Link from "next/link";
import classes from "./index.module.css";
import HomeIcon from "./components/HomeIcon";
import { usePathname } from "next/navigation";
import AgentIcon from "./components/AgentIcon";

const Header = () => {
  const path = usePathname().split("/")[1];

  return (
    <div className={classes["container"]}>
      <div className={classes["box"]}>
        <div className={classes["logo"]}>
          <p>
            Chain
            <span>Mind</span>
          </p>
        </div>
        <div className={classes["routes"]}>
          <Link className={`${classes["icons"]}`} href="/">
            <HomeIcon isActive={path == ""} />
            <span
              style={{
                color: path == "" ? "#66cdef" : "#efeee7",
              }}
            >
              Home
            </span>
          </Link>
          <Link className={`${classes["icons"]}`} href="/agents">
            <AgentIcon isActive={path == "agents"} />
            <span
              style={{
                color: path == "agents" ? "#66cdef" : "#efeee7",
              }}
            >
              Agents
            </span>
          </Link>
          <div className={`${classes["icons"]}`}>Connect Wallet</div>
        </div>
      </div>
    </div>
  );
};

export default Header;
