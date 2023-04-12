import Head from "next/head";
import Image from "next/image";
import { Inter } from "@next/font/google";
import styles from "@/styles/Home.module.scss";
import Tabs from "@/components/Tabs";
import Filter from "@/components/Filter/Filter";
import InfiniteListings from "@/components/InfiniteListings";
import Pagination from "@/components/Pagination";
import MainListings from "@/components/MainListing";
import useUser from "@/hooks/useUser";
import React from "react";
import { useRouter } from "next/router";
const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const { user } = useUser();
  const router = useRouter();

  // React.useEffect(() => {
  //   if (!user) router.push("/login");
  // }, []);
  return (
    <>
      <Head>
        <title>Create Next App</title>
        <meta name="description" content="Generated by create next app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <div className="container">
          {/* <h2>Hello</h2> */}
          {/* <Tabs tabs={["1", "2"]} /> */}
          {/* <Filter /> */}
          <div>
            {/* <InfiniteListings location="london" radius={10000000} /> */}
            {/* <Pagination /> */}
            {user?.name && <MainListings />}
          </div>
        </div>
      </main>
    </>
  );
}
