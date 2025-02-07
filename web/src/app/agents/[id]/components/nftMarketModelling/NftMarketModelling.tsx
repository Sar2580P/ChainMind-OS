import LineChart from "./LineChart";
import { useEffect, useState } from "react";
import useGetResponse from "@/hooks/useGetResponse";

interface SellerRewards {
  [key: string]: number[];
}

interface BuyerRewards {
  [key: string]: number[];
}

interface EpisodeData {
  episode_num: number;
  seller_rewards: SellerRewards;
  buyer_rewards: BuyerRewards;
  gas_fees: number[];
  rarity_volume_traded: number[][];
}

const NftMarketModelling = () => {
  const [data, setData] = useState<EpisodeData[]>([]);
  const { getResponse } = useGetResponse();

  useEffect(() => {
    const fetchData = async () => {
      const data = await getResponse("nft_market_modelling");
      console.log(data);
      if (data) setData(data);
    };
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div
      className="flex justify-start items-center flex-col scrollbar-hide pt-0"
      style={{
        height: "100vh",
        width: "-webkit-fill-available",
        overflowY: "scroll",
        border: "1px solid #ffffff",
        borderRadius: "5px",
        backgroundColor: "transparent",
      }}
    >
      <div className="text-lg font-bold text-white p-0 text-center mb-1">
        NFT Market Modelling: Seller Rewards, Buyer Rewards, Gas Fees, Rarity
      </div>
      {data.map((d) => (
        <div key={d.episode_num} className="w-full">
          <LineChart title="Seller Rewards" dataset={d.seller_rewards} />
          <LineChart title="Buyer Rewards" dataset={d.buyer_rewards} />
          <LineChart title="Gas Fees" dataset={{ Gas_Fees: d.gas_fees }} />
          <LineChart
            title="Rarity Volume Traded"
            dataset={{
              ...d.rarity_volume_traded.reduce(
                (acc: { [key: number]: number[] }, curr, index) => {
                  acc[index] = curr;
                  return acc;
                },
                {}
              ),
            }}
          />
        </div>
      ))}
    </div>
  );
};

export default NftMarketModelling;
