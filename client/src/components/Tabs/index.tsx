import { useRouter } from "next/router";
import React, { FC } from "react";

import styles from "./Tabs.module.scss";

interface TabProps {
  isActive: boolean;
  title: string;
  onClick: () => void;
}

const TabItem: FC<TabProps> = ({ title, onClick, isActive }) => {
  return (
    <button
    type="button"
      onClick={() => onClick()}
      className={isActive ? styles.activeTabCon : styles.tabCon}
    >
      {title}
    </button>
  );
};

interface TabsComponentProps {
  tabs: string[];
}

const Tabs: FC<TabsComponentProps> = ({ tabs }) => {
  const router = useRouter();
  const { push, query, pathname } = router;

  const routeToTab = (tabName: string) => {
    if (tabName === "all") return push(pathname, undefined, { shallow: true });

    push({ query: { ...query, listingType: tabName } }, undefined, { shallow: true });
  };

  return (
    <div className={styles.wrapper}>
      {tabs?.map((tab: string, index: number) => (
        <TabItem
          isActive={
            tab.toLowerCase() === query.listingType ||
            (tab === "All" && query.listingType === undefined)
          }
          onClick={() => routeToTab(tab.toLowerCase())}
          title={tab}
          key={index}
        />
      ))}
    </div>
  );
};

export default Tabs;
