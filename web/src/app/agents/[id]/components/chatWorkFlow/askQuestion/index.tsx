"use client";
import { v4 } from "uuid";
import { useRef, useState } from "react";
import { useContext } from "react";
import { IoIosSend } from "react-icons/io";
import usePolling from "@/hooks/usePolling";
import AppContext from "@/contexts/AppContext";
import { CardFooter } from "@/components/ui/card";
import LoadingComponent from "@/components/loading";
import { Textarea } from "@/components/ui/textarea";
import usePostResponse from "@/hooks/usePostResponse";
import useHandleTextAreaSize from "@/hooks/useHandleTextAreaSize";
import { CreateNodeAndEdges } from "@/hooks/useCreateNodeAndEdges";

const AskQuestion = ({ agent_id }: { agent_id: string }) => {
  const { polling } = usePolling();
  const { postResponse } = usePostResponse();
  const [loading, setLoading] = useState(false);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const {
    setAgentDatasHandler,
    setAgentCurrentNodeAndEdgesHandler,
    setDeployContractDataHandler,
  } = useContext(AppContext);
  const { textareaRef, handleTextAreaSize } = useHandleTextAreaSize();
  const [isLayer1ORFeedback, setIsLayer1ORFeedback] = useState(true);

  const setCurrentInputState = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    handleTextAreaSize();
    if (textareaRef.current) {
      textareaRef.current.value = e.target.value;
    }
  };

  const handleEnterLayer1 = async () => {
    if (!textareaRef.current) return;
    if (textareaRef.current.value === "") {
      return;
    }
    setLoading(true);
    const question_id = v4();
    const curr_user_question = textareaRef.current.value;
    textareaRef.current.value = "";
    setAgentDatasHandler(agent_id, "chats", [
      {
        id: question_id,
        isAgent: false,
        message: curr_user_question,
        createdAt: new Date().toISOString(),
      },
    ]);
    handleTextAreaSize();
    const response_layer_1_data = await postResponse(
      {
        new_agent_id: agent_id,
        USER_PROMPT: curr_user_question,
      },
      "layer_1_objective_identification"
    );
    if (response_layer_1_data) {
      const response_layer_1 = response_layer_1_data.agent_data;
      const markdown_text = response_layer_1_data.markdown_text;
      setDeployContractDataHandler("objectives", response_layer_1.objectives);
      setDeployContractDataHandler(
        "brief_context_on_each_objective",
        response_layer_1.brief_context_on_each_objective
      );
      setDeployContractDataHandler(
        "tech_experts_for_objectives",
        response_layer_1.tech_experts_for_objectives
      );
      const { Nodes, Edges } = CreateNodeAndEdges(response_layer_1, agent_id);
      setAgentCurrentNodeAndEdgesHandler(Nodes, Edges);
      const agent_answer_id = v4();
      setAgentDatasHandler(agent_id, "chats", [
        {
          id: agent_answer_id,
          isAgent: true,
          message: markdown_text,
          createdAt: new Date().toISOString(),
        },
      ]);
      setLoading(false);
      setIsLayer1ORFeedback(false);
      startPolling();
      const response_feedback = await postResponse(
        {
          agent_id: agent_id,
          user_objectives_json: response_layer_1,
        },
        "layer_feedback_objective_design"
      );
      console.log(response_feedback);
      if (response_feedback) {
        setIsLayer1ORFeedback(true);
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
          intervalRef.current = null;
        }
      }
    } else {
      setLoading(false);
    }
    console.log(response_layer_1);
  };

  const startPolling = () => {
    if (isLayer1ORFeedback) {
      intervalRef.current = setInterval(async () => {
        console.log("Polling");
        const response = await polling(
          {
            agent_id: agent_id,
          },
          "check_layer_feedback_objective_design"
        );
        console.log(response);
        if (response) {
          console.log(response);
          const question_id = v4();
          setAgentDatasHandler(agent_id, "chats", [
            {
              id: question_id,
              isAgent: true,
              message: response,
              createdAt: new Date().toISOString(),
            },
          ]);
        }
      }, 7000);
    } else if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  };

  const handleEnterFeedback = async () => {
    if (!textareaRef.current) return;
    if (textareaRef.current.value === "") {
      return;
    }
    setLoading(true);
    const question_id = v4();
    const curr_user_question = textareaRef.current.value;
    textareaRef.current.value = "";
    setAgentDatasHandler(agent_id, "chats", [
      {
        id: question_id,
        isAgent: false,
        message: curr_user_question,
        createdAt: new Date().toISOString(),
      },
    ]);
    handleTextAreaSize();
    await postResponse(
      {
        agent_id: agent_id,
        user_response: curr_user_question,
      },
      "check_user_response_layer_feedback_objective_design"
    );
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
            if (isLayer1ORFeedback) handleEnterLayer1();
            else handleEnterFeedback();
            handleTextAreaSize();
          }}
          className="cursor-pointer"
          color={isLayer1ORFeedback ? "#ffffff" : "#dc96da"}
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
