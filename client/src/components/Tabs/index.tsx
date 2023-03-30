import { useRouter } from 'next/router';
import React, { FC } from 'react';

import styles from './Tabs.module.scss';

interface TabProps {
  isActive: boolean;
  title: string;
  onClick: (v: string) => void;
}

const TabItem: FC<TabProps> = ({ title, onClick, isActive }) => {
  return (
    <div
      onClick={() => onClick(title.toLowerCase())}
      className={isActive ? styles.activeTabCon : styles.tabCon}>
      {title}
    </div>
  );
};

interface TabsComponentProps {
  tabs: string[];
}

const Tabs: FC<TabsComponentProps> = ({ tabs }) => {
  const router = useRouter();
  const { push, query, pathname } = router;

  const onSelect = (v: string) => {
    if (v === 'all') return push(pathname, undefined, { shallow: true });
    push({ query: { ...query, listing: v } }, undefined, { shallow: true });
  };

  return (
    <div className={styles.wrapper}>
      {tabs?.map((tab: string, index: number) => (
        <TabItem
          isActive={
            tab.toLowerCase() === query.listing || (tab === 'All' && query.listing === undefined)
          }
          onClick={(v) => onSelect(v)}
          title={tab}
          key={index}
        />
      ))}
    </div>
  );
};

export default Tabs;
