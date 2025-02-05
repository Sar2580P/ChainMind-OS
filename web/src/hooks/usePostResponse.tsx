"use client";
import { useState } from "react";
import { toast } from "sonner";

const usePostResponse = () => {
  const [loading, setLoading] = useState(false);

  const postResponse = async (data: Record<string, unknown>, path: string) => {
    console.log(data);
    try {
      setLoading(true);
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/v1/agent/${path}/`,
        {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        }
      );
      const responsedata = await response.json();
      console.log(responsedata);
      if (responsedata.status_code !== 200) {
        setLoading(false);
        toast("Failed to post response", {
          description: responsedata.message,
          action: {
            label: "Delete",
            onClick: () => console.log("Delete"),
          },
        });
        setTimeout(() => {
          toast.dismiss();
        }, 2000);
        return null;
      }
      setLoading(false);
      return responsedata.response;
    } catch (err) {
      setLoading(false);
      console.log(err);
      toast("Server Error", {
        description: "Failed to post response",
        action: {
          label: "Delete",
          onClick: () => console.log("Delete"),
        },
      });
      setTimeout(() => {
        toast.dismiss();
      }, 2000);
      return null;
    }
  };
  return { postResponse, loading };
};

export default usePostResponse;
