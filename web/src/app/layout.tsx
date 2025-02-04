import "../styles/globals.css";
import type { Metadata } from "next";
import { Providers } from "./providers";
import { Inter } from "next/font/google";
import Header from "@/components/header";
import Footer from "@/components/footer";
import { AppContextProvider } from "@/contexts/AppContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "ChainMind",
  description: "Agentic Ethereum hackathon 2025, ChainMind",
  icons: ["/robot/logo.png"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scrollbar-hide">
      <body className={inter.className}>
        <AppContextProvider>
          <Providers>
            <Header />
            {children}
            <Footer />
          </Providers>
        </AppContextProvider>
      </body>
    </html>
  );
}
