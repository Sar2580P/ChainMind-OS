"use client";
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { CardFooter } from "@/components/ui/card";
import LoadingComponent from "@/components/loading";

const AskQuestion = () => {
  const [askQuestionValue, setAskQuestionValue] = useState("");
  const [loading, setLoading] = useState(false);

  const handleEnter = () => {
    if (askQuestionValue.trim() === "") {
      return;
    }
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setAskQuestionValue("");
    }, 1000);
  };

  return (
    <CardFooter className="relative pb-3">
      <Input
        placeholder="Ask the agent about the work...."
        value={askQuestionValue}
        onChange={(e) => setAskQuestionValue(e.target.value)}
        id="chatWithAgent"
        disabled={loading}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleEnter();
          }
        }}
      />
      <div className="absolute right-12 top-2.5">
        {loading && (
          <LoadingComponent
            height="12px"
            size="8px"
            width="30px"
            alignItems="center"
          />
        )}
      </div>
    </CardFooter>
  );
};

export default AskQuestion;
