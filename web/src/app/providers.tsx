"use client";
import "@rainbow-me/rainbowkit/styles.css";
import { ReactNode } from "react";
import { WagmiProvider } from "wagmi";
import {
  getDefaultConfig,
  RainbowKitProvider,
  darkTheme,
} from "@rainbow-me/rainbowkit";
import {
  mainnet,
  polygon,
  optimism,
  arbitrum,
  base,
  sepolia,
  polygonMumbai,
  zora,
  filecoinCalibration,
  hardhat,
  goerli,
  arbitrumGoerli,
  fantomTestnet,
  optimismGoerli,
  avalancheFuji,
  moonbaseAlpha,
  celoAlfajores,
  mantleTestnet,
  arbitrumSepolia,
} from "wagmi/chains";
import { QueryClientProvider, QueryClient } from "@tanstack/react-query";

const config = getDefaultConfig({
  appName: "ChainMind",
  projectId: "ChainMind_123",
  chains: [
    mainnet,
    polygon,
    optimism,
    arbitrum,
    base,
    sepolia,
    polygonMumbai,
    zora,
    filecoinCalibration,
    hardhat,
    goerli,
    arbitrumGoerli,
    fantomTestnet,
    optimismGoerli,
    avalancheFuji,
    moonbaseAlpha,
    celoAlfajores,
    mantleTestnet,
    arbitrumSepolia,
  ],
  ssr: true,
});

const queryClient = new QueryClient();

export function Providers({ children }: { children: ReactNode }) {
  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        <RainbowKitProvider
          theme={darkTheme({
            accentColor:
              "linear-gradient(90deg,rgba(111, 255, 255, 0.6) 0.17%,rgba(102, 205, 239, 0.6) 99.46%)",
            accentColorForeground: "#efeee7",
            borderRadius: "small",
            fontStack: "system",
            overlayBlur: "small",
          })}
        >
          {children}
        </RainbowKitProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
}
