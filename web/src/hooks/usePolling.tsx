"use client";

const usePolling = () => {
  const polling = async (data: Record<string, unknown>, path: string) => {
    console.log(data);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/v1/agents/${path}/`,
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
      if (responsedata.status_code !== 200) return null;
      if (responsedata.data) return responsedata.data;
      return null;
    } catch (err) {
      console.log(err);
      return null;
    }
  };

  return { polling };
};

export default usePolling;
