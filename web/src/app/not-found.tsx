import Link from "next/link";
import classes from "@/styles/page.module.css";

export default function NotFound() {
  return (
    <div className={classes.container}>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          color: "white",
          paddingTop: "3rem",
        }}
      >
        <h1>404 - Page Not Found</h1>
        <p>
          The page you are looking for might have been removed had its name
          changed or is temporarily unavailable.
        </p>
        <Link href="/">
          <div
            style={{
              backgroundColor: "var(--primary-color)",
              color: "white",
              padding: "0.5rem 1rem",
              borderRadius: "5px",
              cursor: "pointer",
              marginTop: "1rem",
            }}
          >
            Go to Home Page
          </div>
        </Link>
      </div>
      <div className={classes["box"]}>
        <div className={classes["left"]}></div>
        <div className={classes["right"]}></div>
      </div>
    </div>
  );
}
