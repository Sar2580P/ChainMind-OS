import { useRef } from "react";

const useHandleTextAreaSize = () => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const handleTextAreaSize = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = Math.min(textarea.scrollHeight, 225) + "px";
    }
  };

  return { textareaRef, handleTextAreaSize };
};

export default useHandleTextAreaSize;
