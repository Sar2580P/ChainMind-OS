"use client";
import { v4 } from "uuid";
import { useState } from "react";
import { useContext } from "react";
import { IoIosSend } from "react-icons/io";
import AppContext from "@/contexts/AppContext";
import { CardFooter } from "@/components/ui/card";
import LoadingComponent from "@/components/loading";
import { Textarea } from "@/components/ui/textarea";
import usePostResponse from "@/hooks/usePostResponse";
import useHandleTextAreaSize from "@/hooks/useHandleTextAreaSize";

const AskQuestion = ({ agent_id }: { agent_id: string }) => {
  const [loading, setLoading] = useState(false);
  const { postResponse } = usePostResponse();
  const { setAgentDatasHandler } = useContext(AppContext);
  const { textareaRef, handleTextAreaSize } = useHandleTextAreaSize();

  const setCurrentInputState = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    handleTextAreaSize();
    if (textareaRef.current) {
      textareaRef.current.value = e.target.value;
    }
  };

  const handleEnter = async () => {
    if (!textareaRef.current) return;
    if (textareaRef.current.value === "") {
      return;
    }
    setLoading(true);
    const question_id = v4();
    const curr_user_question = textareaRef.current.value;
    textareaRef.current.value = "";
    setAgentDatasHandler(
      agent_id,
      "chats",
      {
        id: question_id,
        question: curr_user_question,
        assistantAnswer: "Wait for the agent to respond",
        createdAt: new Date().toISOString(),
      },
      question_id
    );
    handleTextAreaSize();
    const response_layer_1 = await postResponse(
      {
        new_agent_id: agent_id,
        USER_PROMPT: curr_user_question,
      },
      "layer_1_objective_identification"
    );
    if (response_layer_1) {
      setAgentDatasHandler(
        agent_id,
        "chats",
        {
          id: question_id,
          question: curr_user_question,
          assistantAnswer:
            "Layer 1 Objective Identification had been sent and all the agent needs to do is to respond from the user's end",
          createdAt: new Date().toISOString(),
        },
        question_id
      );
      const response_feedback = await postResponse(
        {
          agent_id: agent_id,
          user_objectives_json: response_layer_1,
        },
        "layer_feedback_objective_design"
      );
      console.log(response_feedback);
    }
    console.log(response_layer_1);
    setLoading(false);
  };

  return (
    <CardFooter className="relative pb-3">
      <Textarea
        placeholder="Ask the agent about the work...."
        onChange={(e) => setCurrentInputState(e)}
        id="chatWithAgent"
        disabled={loading}
        rows={2}
        className="scrollbar-hide"
        ref={textareaRef}
      />
      <div className="absolute right-12 top-2.5">
        <IoIosSend
          size={30}
          onClick={() => {
            handleEnter();
            handleTextAreaSize();
          }}
          className="cursor-pointer"
        />
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
