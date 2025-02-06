"use client";
import { useState } from "react";

const useGetResponse = () => {
  const [loading, setLoading] = useState(false);

  const getResponse = async (path: string) => {
    console.log(path);
    try {
      setLoading(true);
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/v1/agents/${path}`,
        {
          method: "GET",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
        }
      );
      const responsedata = await response.json();
      console.log(responsedata);
      setLoading(false);
      if (responsedata.status_code !== 200) {
        return null;
      }
      return responsedata.data;
    } catch (err) {
      console.log(err);
      setLoading(false);
      return null;
    }
  };
  return { getResponse, loading };
};

export default useGetResponse;
