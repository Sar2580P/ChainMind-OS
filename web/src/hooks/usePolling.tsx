"use client";
import { useState } from "react";

const usePolling = () => {
  const [loading, setLoading] = useState(false);
  const [isPolling, setIsPolling] = useState(true);

  const polling = async (data: Record<string, unknown>, path: string) => {
    if (!isPolling) return;

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
        return null;
      }

      setLoading(false);

      setTimeout(() => polling(data, path), 10000);

      return responsedata.data;
    } catch (err) {
      setLoading(false);
      console.log(err);
      return null;
    }
  };

  const startPolling = () => {
    setIsPolling(true);
  };

  const stopPolling = () => {
    setIsPolling(false);
  };

  return { polling, loading, startPolling, stopPolling };
};

export default usePolling;
