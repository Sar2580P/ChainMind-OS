"use client";
import React from "react";
import classes from "@/styles/page.module.css";

const Error: React.FC = () => {
  return (
    <>
      <h1>Error</h1>
      <p>Something went wrong...</p>{" "}
      <div className={classes["box"]}>
        <div className={classes["left"]}></div>
        <div className={classes["right"]}></div>
      </div>
    </>
  );
};

export default Error;
